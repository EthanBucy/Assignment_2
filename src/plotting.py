import os
import csv
import math
from typing import List, Tuple
import matplotlib.pyplot as plt

def load_summary(path: str) -> Tuple[List[int], List[float], List[float]]:
    n, rt, ops = [], [], []
    with open(path) as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            n.append(int(row[0])); rt.append(float(row[1])); ops.append(float(row[2]))
    return n, rt, ops

def plot_runtime_with_on3(ns: List[int], rts: List[float], out_path: str):
    # scale k * n^3 to pass through first non-trivial point
    k = rts[0] / (ns[0]**3)
    theor = [k * (n**3) for n in ns]

    plt.figure()
    plt.plot(ns, rts, marker="o", label="Measured runtime")
    plt.plot(ns, theor, marker="o", linestyle="--", label="k·n^3")
    plt.xlabel("Array size n")
    plt.ylabel("Runtime (s)")
    plt.title("ThreeSum brute force: runtime vs n")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)

def plot_ops(ns: List[int], ops: List[float], out_path: str):
    plt.figure()
    plt.plot(ns, ops, marker="o", label="Measured ops")
    # theoretical C(n,3)
    theor = [n*(n-1)*(n-2)/6 for n in ns]
    plt.plot(ns, theor, marker="o", linestyle="--", label="C(n,3)")
    plt.xlabel("Array size n")
    plt.ylabel("Operation count")
    plt.title("ThreeSum brute force: operations vs n")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)

def main():
    os.makedirs("results/figures", exist_ok=True)
    ns, rts, ops = load_summary("results/summary.csv")
    plot_runtime_with_on3(ns, rts, "results/figures/runtime_vs_n.png")
    plot_ops(ns, ops, "results/figures/ops_vs_n.png")

if __name__ == "__main__":
    main()
