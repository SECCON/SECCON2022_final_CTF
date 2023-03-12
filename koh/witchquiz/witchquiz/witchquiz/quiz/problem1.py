from .iproblem import IProblem
from typing import Optional

class Problem1(IProblem):
    def score(self, stage: int, answer: Optional[list[int]]) -> int:
        if answer == None:
            return 0

        cnt = 0
        for i in range(len(answer)):
            cnt += (1 if answer[i] == (i+1) else 0)
        return cnt