from typing import Optional
import secrets
import os
import pickle
import numpy as np

class PureRandom:
    def __init__(self) -> None:
        # __init__ is called only once at server startup. The answer is saved in a file so that the answer does not change.
        server_ans_filename = "purerandom.ans"

        if not os.path.isfile(server_ans_filename):
            ans = []
            for _ in range(540):
                ans.append(int(secrets.token_hex(1), 16) % 2)
            with open(server_ans_filename, "wb") as f:
                pickle.dump(ans, f)

        with open(server_ans_filename, "rb") as f:
            self.ans = pickle.load(f)


    def score(self, tick: int, your_answer: Optional[list[int]]) -> int:
        """
        Calculate scores for submitted answers
        
        Parameters
        ----------
        tick: int
            `tick` you given as request (1-indexed)
        your_answer : int
            `answer` you given as request
        """
        if your_answer == None:
            return 0

        cnt = 0
        
        # note: Answer may change depending on tick

        ll = your_answer
        rr = [tick] + self.ans
        msize = min(len(ll), len(rr))
        l = np.array(ll[:msize])
        r = np.array(rr[:msize])
        cnt = np.count_nonzero(np.equal(l, r))

        # note: The evaluation method may change depending on the problem
        if len(your_answer) == 0 or your_answer[0] != tick:
            return 0
        return cnt