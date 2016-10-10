#!/usr/bin/python3
from math import sqrt


class Handle():
    def __init__(self,time,steps,discount,sigma,target,barrier,sell=False):
        self.steps = steps
        self.timestep = time/steps
        self.endtime = time
        self.discount = discount
        self.p = (discount-sigma^2/2)/(2*sigma) * sqrt(self.timestep)
        self.coststep = sigma*sqrt(self.timestep)
        self.target = target
        self.barrier = barrier
        self.sell = sell
        self.buy = not self.sell
    def V(self,price,step_index=0):
        if price > self.barrier:
            return 0
        elif step_index == self.steps:
            if self.buy:
                return max(0, price - self.target)
            else:
                return min(0, price - self.target)
        else:
            return self.V(self.price+self.coststep,step_index + 1)*self.p + \
                   self.V(self.price+self.coststep)*(1-self.p)
        






