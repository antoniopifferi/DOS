# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 15:04:54 2018

@author: Antonio
"""
from numpy import *
from scipy import *
from matplotlib.pyplot import *
from pandas import *

data=read_table('D:\Beta\Analysis\Maybe\MAYm0000.txt')
Trim=read_table('D:\Beta\Analysis\Maybe\Trim.txt')
data=merge(data,Trim)
for ir in data.Rho.unique():
    table=data[(data.Det==data.Trim) & (data.Material=='Phantom')].pivot_table(['Mua','Mus'],index='Lambda',columns=['Sample','Pos'],aggfunc='mean')
    figure('Mua'+str(ir))
    plot(table.Mua)
    ylim([0,0.4]), legend(table.Mua), title('Mua'+str(ir)), xlabel('wavelength (nm)'), ylabel('absorption (cm-1)')
    figure('Mus'+str(ir))
    plot(table.Mus)
    ylim([0,10.0]), legend(table.Mus), title('Mus'+str(ir)), xlabel('wavelength (nm)'), ylabel('reduced scattering (cm-1)')