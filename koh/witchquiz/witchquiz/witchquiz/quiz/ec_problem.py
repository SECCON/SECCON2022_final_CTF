from typing import Optional
import random
import pickle
import os
import numpy as np

class EC:
    def __init__(self, a=None, b=None):
        self.p = 1009
        self.field = [[0 for i in range(self.p)] for j in range(self.p)]

        self.a = random.randrange(1,self.p) if a is None else a
        self.b = random.randrange(1,self.p) if b is None else b

        # y^2 = x^3 + a*x + b
        self.points = []

        for x in range(self.p):
            for y in range(1, self.p):
                if (y*y) % self.p == (x*x*x + self.a * x + self.b) % self.p:
                    self.points.append((x,y))
                    self.points.append((x,self.p-y))
                    self.field[y][x] = 1
                    self.field[self.p - y][x] = 1

        self.x, self.y = self.points[random.randrange(0,len(self.points))]

        for p in self.points:
            x, y = p
            assert y*y % self.p == (x*x*x + self.a * x + self.b) % self.p
        
        assert self.y*self.y % self.p == (self.x*self.x*self.x + self.a * self.x + self.b) % self.p

    def get_answer(self, x, y):
        ans = [0] * (1009*1009)
        for p in self.points:
            ans[p[1] * self.p + p[0]] = 1

        for i in range(self.p):
            ans[i * self.p + x] = 1
            ans[y * self.p + i] = 1
        return ans 
    
    def next(self):
        phi = (3*self.x*self.x + self.a) * pow(2*self.y, -1, self.p)
        psi = (-3*self.x*self.x*self.x - self.a*self.x + 2 * self.y * self.y) * pow(2*self.y, -1, self.p)
        self.x = (phi * phi - 2 * self.x) % self.p
        self.y = (-phi * self.x - psi) % self.p
        assert self.y*self.y % self.p == (self.x*self.x*self.x + self.a * self.x + self.b) % self.p
    
class ECProblem:
    # __init__ is called only once at server startup. The answer is saved in a file so that the answer does not change.
    def __init__(self):
        server_ans_filename = "ec_problem.ans"

        if not os.path.isfile(server_ans_filename):
            with open(server_ans_filename, "wb") as f:
                curvepoints = []
###########################################################################################
#                                  ATTENSION                                              #
# This problem changes parameters and points every 480 ticks. Please be careful           #
###########################################################################################
                for i in range(3):
                    xys = []
                    ec = EC()
                    for tick in range(480):
                        xys.append((ec.x, ec.y))
                        ec.next()
                    curvepoints.append({"a":ec.a, "b":ec.b, "xys":xys})
                pickle.dump(curvepoints, f)

        with open(server_ans_filename, "rb") as f:
            self.curves = pickle.load(f)

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
        curve_index = ((tick-1)//480)
        curve = self.curves[curve_index]

        ec = EC(curve["a"], curve["b"])
        xys = curve["xys"]

        if your_answer == None:
            return 0

        expected = ec.get_answer(xys[tick-480*curve_index][0], xys[tick-480*curve_index][1])
        msize = min(len(your_answer), len(expected))
        l = np.array(your_answer[:msize])
        r = np.array(expected[:msize])
        cnt = np.count_nonzero(np.equal(l, r))
        
        ###########################################################################################
        #                                  ATTENSION                                              #
        # This problem changes parameters and points every 480 ticks. Please be careful           #
        ###########################################################################################
        return cnt * (((tick-1)//480) + 1)


