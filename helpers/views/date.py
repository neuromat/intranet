# -*- coding: utf-8 -*-
import datetime


def now_plus_thirty():
    date = datetime.datetime.now() + datetime.timedelta(days=30)
    date = date.strftime("%Y%m%d %H:%M:%S")
    date = datetime.datetime.strptime(date, '%Y%m%d %H:%M:%S').date()
    return date


def now_plus_five_years():
    date = datetime.datetime.now() + datetime.timedelta(days=5*365)
    date = date.strftime("%Y%m%d %H:%M:%S")
    date = datetime.datetime.strptime(date, '%Y%m%d %H:%M:%S').date()
    return date
