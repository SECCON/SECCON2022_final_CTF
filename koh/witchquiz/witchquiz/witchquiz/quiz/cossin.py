import math
import matplotlib.pyplot as plt
from typing import Optional
from . import cossin_secrets
from .iproblem import IProblem

class CosSin(IProblem):
    def score(self, stage: int, answer: Optional[list[int]]) -> int:
        if answer == None:
            return 0

        from .cossin_ans import ans

        cnt = 0
        for l, r in zip(answer, ans):
            cnt += (1 if l == r else 0)
        return cnt

def generator():
    def f(a,b,c,d,t):
        x = 0
        for i in range(len(a)):
            x += pow(math.cos(a[i]*t), c[i])
        y = 0
        for i in range(len(b)):
            y += pow(math.sin(b[i]*t), d[i])
        return x,y

    N = 1001*1001
    width = 1001
    height = 1001

    a = cossin_secrets.a
    b = cossin_secrets.b
    c = cossin_secrets.c
    d = cossin_secrets.d

    for values in a + b + c + d:
        assert values < 20

    xs = []
    ys = []
    x_size = 4.0/1000.0
    y_size = 4.0/1000.0
    field = [[0] * height] * width

    for t in range(100000):
        x, y = f(a,b,c,d,t*2*3.14/100000)
        xindex = int((x + 2.0)//x_size)
        yindex = int((y + 2.0)//y_size)
        field[yindex][xindex] += 1
        xs.append(xindex)
        ys.append(yindex)

    ans = []
    dy = [0,1,1,1,0,-1,-1,-1]
    dx = [1,1,0,-1,-1,-1,0,1]

    for i in range(len(field)):
        for j in range(len(field[i])):
            ans.append(field[i][j])
            if field[i][j] == 1:
                f = False
                for d in range(8):
                    if 0 < i + dy[d] and i + dy[d] < len(field) and 0 < j + dx[d] and j + dx[d] < len(field[i]):
                        if field[i+dy[d]][j+dx[d]] == 1:
                            f = True
                assert f
    
    return ans

if __name__ == '__main__':
    print(f"ans = {generator()}") # cossin_ans.py