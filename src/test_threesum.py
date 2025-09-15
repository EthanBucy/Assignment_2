from threesum import three_sum_bruteforce, InputError



def run():
    # 1: example true
    A = [3,7,1,2,8,4,5]; t = 13
    ok, trip, ops = three_sum_bruteforce(A, t)
    assert ok is True and sum(trip) == t

    # 2: example false
    A = [1,2,3,4]; t = 15
    ok, trip, _ = three_sum_bruteforce(A, t)
    assert ok is False and trip is None

    # 3: negatives
    A = [-5, -1, 2, 3, 9]; t = 1   # -5, -1, 7 no; -5, 2, 4 no; -1,2,0 no; -5,3,3 no; false
    ok, _, _ = three_sum_bruteforce(A, t)
    assert ok is False

    # 4: target zero
    A = [-2, -1, 1, 2, 3]; t = 0   # -2, -1, 3
    ok, trip, _ = three_sum_bruteforce(A, t)
    assert ok is True and sum(trip) == 0

    # 5: large values
    A = [10**6, -10**6, 5, 7, 11, -12]; t = 6  # -12, 7, 11
    ok, trip, _ = three_sum_bruteforce(A, t)
    assert ok is True and sum(trip) == t

    # 6: input validation
    try:
        three_sum_bruteforce([1,2], 0)
        assert False
    except InputError:
        pass

if __name__ == "__main__":
    run()
    print("OK")
