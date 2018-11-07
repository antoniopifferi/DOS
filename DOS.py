# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 15:04:54 2018

@author: Antonio
"""

from numpy import *
from scipy import *
from matplotlib.pyplot import *
from pandas import *

#NameCol={}
#NameColkey=['FileSystName','FileDataNameVar','Mua0Opt','VarMus0Opt','Lab01','Lab02','Lab03','ForwardGeomHybridDetX','Lab04','Lab05','VarShiftOpt','Lab06','Lab07','Lab08']
#NameColval=['Syst','Data','Mua','Mus','Lambda','Rho','Volunteer','fRho','TypeFit','Age','Shift','Thickness','Void1','Code']
#for key, val in zip(NameColkey,NameColval):
#    NameCol[key]=val
data=read_table('D:\Beta\Analysis\Maybe\MAYm0000.txt')
Trim=read_table('D:\Beta\Analysis\Maybe\Trim.txt')
data=merge(data,Trim)
#for key, val in zip(NameColkey,NameColval):
for ir in data.Rho.unique():
    table=data[(data.Det==data.Trim) & (data.Material=='Phantom')].pivot_table(['Mua','Mus'],index='Lambda',columns='Sample',aggfunc='mean')
    figure('Mua'+str(ir))
    plot(table.Mua)
    ylim([0,0.4]), legend(table.Mua), title('Mua'+str(ir))
    figure('Mus'+str(ir))
    plot(table.Mus)
    ylim([0,10.0]), legend(table.Mus), title('Mus'+str(ir))