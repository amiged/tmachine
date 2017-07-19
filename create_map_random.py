#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime as dt
import random

a = dt.date(2005, 12, 21)
b = dt.date(2017, 7, 17)
#a = dt.date(2008, 12, 28)
#b = dt.date(2017, 7, 18)
n_day = int((b-a).days)
n_week = int(n_day / 7)

for iw in range(n_week):
    for i in range(7):
        n_commit = random.randint(1, 4)
        print (n_commit, end='')
    print ('')
