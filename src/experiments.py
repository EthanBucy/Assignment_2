import os
import csv
import statistics
import time
from typing import List, Dict
from threesum import three_sum_bruteforce
from datasets import random_distinct_array


SIZES = [50, 100, 200, 400, 800]
TRIALS = 10

def run_once(n: int, force_solution: bool, seed_base: int) -> Dict:
    import random
    random.seed(seed_base + n + (1 if force_solution else 0))
    A = random_distinct_array(n)
    if force_solution:
        a, b, c = A[0], A[1], A[2]
        t = a + b + c
    else:
        t = 3 * (10**7)

    t0 = time.perf_counter()
    found, trip, ops = three_sum_bruteforce(A, t, return_triplet=True)
    t1 = time.perf_counter()
    return {
        "n": n,
        "forced_solution": int(force_solution),
        "found": int(found),
        "ops": ops,
        "runtime_s": t1 - t0
    }

def main():
    os.makedirs("results/figures", exist_ok=True)
    rows = []
    for n in SIZES:
        for force_solution in (True, False):
            for trial in range(TRIALS):
                rec = run_once(n, force_solution, seed_base=12345 + trial)
                rows.append(rec)

    # write raw
    with open("results/runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["n","forced_solution","found","ops","runtime_s"])
        w.writeheader()
        w.writerows(rows)

    # summarize by n (combine solvable and unsolvable; also report each separately)
    def summarize(filter_fn):
        out = []
        for n in SIZES:
            vals = [r for r in rows if r["n"] == n and filter_fn(r)]
            rt = [r["runtime_s"] for r in vals]
            op = [r["ops"] for r in vals]
            out.append({
                "n": n,
                "trials": len(vals),
                "avg_runtime_s": statistics.fmean(rt),
                "stdev_runtime_s": statistics.pstdev(rt),
                "avg_ops": statistics.fmean(op)
            })
        return out

    all_summary   = summarize(lambda r: True)
    yes_summary   = summarize(lambda r: r["forced_solution"] == 1)
    no_summary    = summarize(lambda r: r["forced_solution"] == 0)

    # compute growth ratios for 'all_summary'
    def add_ratios(summ):
        by_n = {d["n"]: d for d in summ}
        for a,b in [(100,200),(200,400),(400,800)]:
            if a in by_n and b in by_n:
                by_n[b]["runtime_ratio_vs_prev"] = by_n[b]["avg_runtime_s"] / by_n[a]["avg_runtime_s"]
                by_n[b]["ops_ratio_vs_prev"]     = by_n[b]["avg_ops"] / by_n[a]["avg_ops"]
        return list(by_n.values())

    all_summary = add_ratios(all_summary)

    # write summaries
    def write_summary(name, data):
        os.makedirs("results", exist_ok=True)
        if not data:
            return
        # union of all keys so every row fits the header
        keys = sorted({k for d in data for k in d.keys()})
        with open(f"results/summary_{name}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for d in data:
                # ensure missing keys don’t crash
                w.writerow({k: d.get(k, "") for k in keys})


    write_summary("all", all_summary)
    write_summary("solvable", yes_summary)
    write_summary("unsolvable", no_summary)

    # compact table for the report
    with open("results/summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Array Size","Avg Runtime (s)","Avg Ops"])
        for d in sorted(all_summary, key=lambda x: x["n"]):
            w.writerow([d["n"], f"{d['avg_runtime_s']:.6f}", int(d["avg_ops"])])

if __name__ == "__main__":
    main()
