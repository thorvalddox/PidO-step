#!/usr/bin/python3
from math import sqrt,fabs


class Handle():
    def __init__(self,time,steps,discount,sigma,target,barrier,sell=False):
        self.steps = steps
        self.timestep = time/steps
        self.endtime = time
        self.discount = discount
        self.p = (discount-sigma**2/2)/(2*sigma) * sqrt(self.timestep) + 0.5
        self.coststep = sigma*sqrt(self.timestep)
        self.target = target
        self.barrier = barrier
        self.sell = sell
        self.buy = not self.sell
    def V(self,value=0,step_index=0):
        """
            A function that generates the value of an option,
            value: the current value of the stock -the value the stock has on time zero
            step_index: The current step, time=step_index*self.timestep
        """
        if value > self.barrier:
            return 0
        elif step_index == self.steps:
            if self.buy:
                return max(0, value - self.target)
            else:
                return min(0, value - self.target)
        else:
            return self.V(value+self.coststep,step_index + 1)*self.p + \
                   self.V(value-self.coststep,step_index + 1)*(1-self.p)

    def draw_tree(self):
        for i in range(-self.steps,self.steps+1):
            print("    "*abs(i) + "  ".join("{:+06.2f}".format(self.V(-i*self.coststep,s)) \
                                            for s in range(abs(i),self.steps+1,2)))


def get_number(text,default=0,type_=float):
    if default:
        showtext = "{} ({}): ".format(text,default)
    else:
        showtext = "{}: ".format(text)
    try:
        return type_(input(showtext))
    except ValueError:
        if default:
            print("The number you provided was invalid")
            print("The default value of {} will be used".format(default))
            return default
        else:
            print("The number you provided was invalid")
            return get_number(text,0,type_)




if __name__ == "__main__":
    h = Handle(get_number("time"),
               get_number("steps",10,int),
               get_number("discount",0.05),
               get_number("sigma"),
               get_number("target - current stock price"),
               get_number("barrier",float("inf")))
    print("the change to go up is: ",h.p)
    print("the price of an option is:",h.V())
    h.draw_tree()






