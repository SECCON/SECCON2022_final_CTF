from typing import Optional
import secrets
import pickle
import os

class LCG:
    def __init__(self, seed, m):
        self.a = 2
        self.seed = seed
        self.m = m

    def rand(self):
        self.seed = (self.seed * self.a) % self.m
        return self.seed

class RandomRotate:
    def __generator(self):
        N = 65536 # public
        ans = [(x+1) for x in range(N)]
        seed = int(secrets.token_hex(8), 16)
        m = 27652344047805921227 # public int(secrets.token_hex(16), 16) * 2 + 1
        lcg = LCG(seed, m)

        for i in range(N-1, 0, -1):
            j = lcg.rand() % i
            ans[i], ans[j] = ans[j], ans[i]
        
        rotate_sums = [0]
        for ticks in range(10000):
            rotate_sums.append((rotate_sums[-1] + (lcg.rand() % N)) % N)

        return ans, rotate_sums

    def __init__(self) -> None:
        # __init__ is called only once at server startup. The answer is saved in a file so that the answer does not change.
        server_ans_filename = "randomrotate.ans"

        if not os.path.isfile(server_ans_filename):
            ans, rotate_sums = self.__generator()
            with open(server_ans_filename, "wb") as f:
                pickle.dump({"answer": ans, "rotate_sums":rotate_sums}, f)

        with open(server_ans_filename, "rb") as f:
            data = pickle.load(f)
            self.ans = data["answer"]
            self.rotate_sums = data["rotate_sums"]

    def score(self, tick: int, answer: Optional[list[int]]) -> int:
        """
        Calculate scores for submitted answers
        
        Parameters
        ----------
        tick: int
            `tick` you given as request (1-indexed)
        given_answer : int
            `answer` you given as request
        """
        if answer == None:
            return 0

        rotate = self.rotate_sums[tick-1]
        ans = self.ans[rotate:] + self.ans[:rotate]

        cnt = 0
        for l, r in zip(answer, ans):
            cnt += (1 if l == r else 0)
        return cnt