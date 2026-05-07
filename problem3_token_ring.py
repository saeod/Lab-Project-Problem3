# CCS 482 - Lab Project
# Problem 3: Token Ring Mutual Exclusion
# 3 processes (P1, P2, P3) sharing one printer

import threading
import time
import random

NUM_PROCESSES = 3
PRINT_ROUNDS  = 2

token_holder = [0]        # P1 holds the token first
token_lock   = threading.Lock()
printer_lock = threading.Lock()


def process(pid):
    name = f"P{pid + 1}"

    for i in range(PRINT_ROUNDS):

        # wait until this process gets the token
        while True:
            with token_lock:
                if token_holder[0] == pid:
                    break
            time.sleep(0.05)

        # got the token -> enter critical section
        with printer_lock:
            print(f"{name} is printing (round {i + 1})")
            time.sleep(random.uniform(0.5, 1.0))
            print(f"{name} finished printing")

        # pass token to next process
        with token_lock:
            token_holder[0] = (pid + 1) % NUM_PROCESSES

        time.sleep(0.1)


if __name__ == "__main__":
    threads = []

    for i in range(NUM_PROCESSES):
        t = threading.Thread(target=process, args=(i,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("all processes done")