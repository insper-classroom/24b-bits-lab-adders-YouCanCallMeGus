#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    @always_comb
    def comb():
        soma.next = a^b
        carry.next = a and b

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for _ in range(3)]
    haList = [None for i in range(2)]
    haList[0] = halfAdder(a,b,s[0],s[1])
    haList[1] = halfAdder(c,s[0],soma,s[2])
    

    @always_comb
    def comb():
        carry.next = s[1] | s[2]

    return instances()


@block
def adder2bits(x, y, soma, carry):
    s = Signal(bool(0))
    half = halfAdder(x[0],y[0],soma[0],s)
    full = fullAdder(x[1],y[1],s,soma[1],carry)
    return instances()


@block
def adder(x, y, soma, carry):
    n = len(x)
    s = [Signal(bool(0)) for _ in range(n)]
    faList = [None for i in range(n)]
    faList[0] = halfAdder(x[0],y[0],soma[0],s[0])
    for i in range(1,n-1):
        faList[i] = fullAdder(x[i],y[i],s[i-1],soma[i],s[i])
    faList[n-1] = fullAdder(x[n-1],y[n-1],s[n-1],soma[n-1],carry)

    @always_comb
    def comb():
        carry.next = s[n-2] | s[n-1]

    return instances()
