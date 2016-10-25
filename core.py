#!/usr/bin/python3
from math import sqrt,fabs,exp
import matplotlib as plt
import matplotlib.pyplot as pyplot
from itertools import chain,count


class Handle():
    def __init__(self, time, steps, interest, volatility, current_stock_price, target, \
                 barrier_top, barrier_bottom, call=True, american=False):
        self.steps = steps
        self.timestep = time/steps
        self.endtime = time
        self.discount = interest
        self.volatility = volatility
        self.p = (interest - volatility ** 2 / 2) / (2 * volatility) * sqrt(self.timestep) + 0.5 # course notes (1.32)
        self.coststep = volatility * sqrt(self.timestep)
        self.strike = target
        self.current = current_stock_price
        self.top = barrier_top
        self.bottom = barrier_bottom
        self.call = call
        self.american = american
        self.Vdict = {} #stores inbetween V values for optimalisation
        self.single_step_discount = exp(-interest*self.timestep)
    @property
    def european(self):
        return not self.american
    @property
    def put(self):
        return not self.call
    def V(self, x_index=0, step_index=0):
        """
            A function that generates the value of an option,
            x_index: the current value of x = x_index * self.coststep
            step_index: The current step, time=step_index*self.timestep
        """
        logreturn = x_index * self.coststep
        value = self.current * exp(logreturn)
        if not(self.bottom < value < self.top):
            #outside of barriers, options becomes worthless
            return 0
        elif step_index == self.steps:
            return self.exchange_value(value)
        elif (x_index, step_index) in self.Vdict:
             return self.Vdict[x_index, step_index]
        else:
            ret = self.single_step_discount * \
                  (self.V(x_index + 1, step_index + 1) * self.p + \
                  self.V(x_index - 1, step_index + 1) * (1 - self.p))
            if self.american:
                #option can be exchanged immediatly
                ret = max(ret,self.exchange_value(value))
            self.Vdict[x_index, step_index] = ret
            return float(ret)

    def reset_V(self):
        self.Vdict = {}

    def exchange_value(self,stockvalue):
        """
            This function returns the value of the option if it would be exchanged immedialty,
            if the stock value is equal to stockvalue
        """
        if self.call:
            return max(0, stockvalue - self.strike)
        else:
            return max(0, self.strike - stockvalue)
    def change_strike(self, newtarget):
        self.strike = newtarget
        self.reset_V()

    def swap_cp(self):
        self.call = not self.call

    def swap_ae(self):
        self.american = not self.american

    def draw_tree(self,target):
        self.change_strike(target)

        for i in range(-self.steps,self.steps+1):
            print("    "*abs(i) + "  ".join("{:+06.2f}".format(self.V(-i,s)) \
                                            for s in range(abs(i),self.steps+1,2)))
    def get_price(self,target):
        self.change_strike(target)
        return self.V(0,0)



def get_number(text,default=0,type_=float):
    if default:
        showtext = "{} ({}): ".format(text,default)
    else:
        showtext = "{}: ".format(text)
    while True:
        try:
            return type_(input(showtext))
        except ValueError:
            if default:
                print("The number you provided was invalid")
                print("The default value of {} will be used".format(default))
                return default
            else:
                print("The number you provided was invalid")


def get_index(text,letters):
    showtext = "{} ({}): ".format(text, "/".join(letters))
    while True:
        answer = input(showtext)
        if not answer:
            print("The answer you provided was invalid")
            continue
        first = answer[0].lower()
        if first in letters:
            return letters.index(first)
        else:
            print("The answer you provided was invalid")

def get_bool(text,letters):
    return not get_index(text,letters)



def defaultlegend():
    for i in count():
        yield "function {}".format(i)


def pltfunc(functions,start,end,steps,filename,legends=...):
    colors = "rgbcmyk"
    xrange = [i*(end-start)/steps+start for i in range(steps)]
    plargs = chain(*((xrange,[func(x) for x in xrange],colors[i%7]) for i,func in enumerate(functions)))
    pyplot.plot(*plargs)
    pyplot.xlabel(r"strike price")
    pyplot.ylabel(r"option price")
    if legends==...:
        legends = defaultlegend()
    if legends is not None:
        pyplot.legend(legends)
    pyplot.savefig(filename)
    pyplot.close()


def get_pricing_function(volatility,call=True,american=False):
    h= Handle(1,20,0.05,volatility,1,1,1.5,0.5,call,american)
    return h.get_price


def plot_pricing_function(filename,volatility,call=True,american=False):
    f = get_pricing_function(volatility,call,american)
    pltfunc((f,), 0, 2, 100,filename,None)

def plot_pricing_functions(filename, volatility_dict, call=True, american=False):
    f = (get_pricing_function(v, call, american) for v in volatility_dict.values())
    pltfunc(f, 0, 2, 100, filename,volatility_dict.keys())


def ex_a():
    h = Handle(get_number("time",1),
               get_number("steps",20,int),
               get_number("interest",0.05),
               get_number("volatility",0.3),
               get_number("current stock price",1),
               get_number("strike price",1),
               get_number("barrier: up and out",float("inf")),
               get_number("barrier: down and out", float("-inf")),
               get_bool("call/put","cp"),
               get_bool("american/european", "ae"))
    print("the change to go up is: ",h.p)
    print("the price of an option is:",h.V())
    h.draw_tree(h.strike)



def ex_b():
    situations = {"standard":0.3,"relaxed":0.1,"volatile":1}
    for ae in ("european","american"):
        for call_put in ("call","put"):
            for name,vol in situations.items():
                filename = "options_{}_{}_{}".format(ae,call_put,name)
                plot_pricing_function(filename,vol,call_put=="call",ae[0]=="a")
            plot_pricing_functions("options_{}_{}".format(ae,call_put),situations,call_put=="call",ae[0]=="a")


if __name__=="__main__":
    print("""Welcome to my solution to the asignment of path integrals in quantum mechanics
    If you select \'a\', The program will let you plug in a set of parameters and
    calculate the correct option price. If you select \'b\', It will generate a
    bunch of graphs representing the different situations. These are saved in the
    same folder as this program runs in. The bonus question is included in both
    the parameter program and the graphs.

    Inputting parameters work as follows:
    if you get something like: option (x/y): you have to type x or y
    if you get something like: value (1.5): you have to give a numerical value
    If you give an invalid value or leave it empty, the default value between the
    parentheses will be used. This also supports 'inf' and '-inf'""")


    if get_bool("assigment","ab"):
        ex_a()
    else:
        ex_b()




