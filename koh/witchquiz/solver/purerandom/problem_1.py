from typing import Optional
import secrets
import os
import pickle

class PureRandom:
    # This function is called at server startup to fix the answer.
    def __init__(self) -> None:
        server_ans_filename = "purerandom.ans"

        if not os.path.isfile(server_ans_filename):
            ans = []
            for _ in range(540):
                ans.append(int(secrets.token_hex(1), 16) % 2)
            with open(server_ans_filename, "wb") as f:
                pickle.dump(ans, f)

        with open(server_ans_filename, "rb") as f:
            self.ans = pickle.load(f)


    def score(self, tick: int, given_answer: Optional[list[int]]) -> int:
        """
        Calculate scores for submitted answers
        
        Parameters
        ----------
        tick: int
            `tick` you given as request (1-indexed)
        given_answer : int
            `answer` you given as request
        """
        if given_answer == None:
            return 0

        cnt = 0
        # note: Answer may change depending on tick
        for l, r in zip(given_answer, [tick] + self.ans):
            cnt += (1 if l == r else 0)

        # note: The evaluation method may change depending on the problem
        if len(given_answer) == 0 or given_answer[0] != [tick]:
            return 0
        return cnt
