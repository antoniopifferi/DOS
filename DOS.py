# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 15:04:54 2018

@author: Antonio
"""
from numpy import *
from scipy import *
from matplotlib.pyplot import *
from pandas import *
close('all')

# OPTIONS
PLOT_SINGLE=False
PLOT_MULTI=False
SHOW_TABLE=True
PLOT_COMP=True
#Task='Abdomen'
Task='Muscle'
Opt=['Mua','Mus']
YLIM={'Mua':[0,0.7],'Mus':[0,20]}
YLABEL={'Mua':'absorption (cm-1)','Mus':'reduced scattering (cm-1)'}

# CONVERSION FUNCTION
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

# PARAMETERS
PathAnalysis='D:\\Beta\\Analysis\\Maybe\\'
DirFigure='Figure\\'
if Task=='Muscle':
    FileData='MAYm0023.txt'
    FileTrim='trimMAYm0023.txt'
    FileKey='keyMAYm0023.txt'
    FIRST_LAMBDA=0
else:
    FileData='MAYm0024.txt'
    FileTrim='trimMAYm0024.txt'
    FileKey='keyMAYm0024.txt'
    FIRST_LAMBDA=2
    
FileComponents='Components2.txt'
PathFigure=PathAnalysis+DirFigure

# LOAD COMPONENTS
Components=read_table(PathAnalysis+FileComponents)
Components.plot(x='Lambda')
yscale('log')
ylim([0,0.5]), title('Components'), xlabel('wavelength (nm)'), ylabel('specific absorption (cm-1)')
savefig(PathFigure+'Components.jpg')
show()

# LOAD DICT
dataKey=read_table(PathAnalysis+FileKey)
dcKey=dict(zip(dataKey.Key, dataKey.Value))

# LOAD AND FILTER DATA
rawData=read_table(PathAnalysis+FileData)
rawData.rename(columns=dcKey,inplace=True)
Trim=read_table(PathAnalysis+FileTrim)
rawData=merge(rawData,Trim)
filtData=rawData[(rawData.Det==rawData.Trim)&(rawData.Accept=='OK')]

# PLOT SINGLE
if PLOT_SINGLE:
    for iss in filtData.Subject.unique():
        for im in filtData.Meas.unique():
            fig=figure(figsize=cm2inch(40, 15))
            table=filtData[(filtData.Subject==iss)&(filtData.Meas==im)].pivot_table(Opt,index='Lambda',columns=['Rho'],aggfunc='mean')
            for io in Opt:
                fig.add_subplot(1,2,1+Opt.index(io))
                plot(table[io])
                ylim(YLIM[io]), legend(table[io]), xlabel('wavelength (nm)'), ylabel(YLABEL[io])
                title('Subject #'+str(iss)+' - Meas='+str(im))
                grid(True)
    show()

if PLOT_MULTI:
    for io in Opt:
        for iss in filtData.Subject.unique():
            fig=figure(figsize=cm2inch(40, 15))
            Rho=list(filtData.Rho.unique())
            for ir in Rho:
                table=filtData[(filtData.Subject==iss)&(filtData.Rho==ir)].pivot_table(Opt,index='Lambda',columns=['Meas'],aggfunc='mean')
                fig.add_subplot(1,len(Rho),1+Rho.index(ir))
                plot(table[io])
                ylim(YLIM[io]), legend(table[io]), xlabel('wavelength (nm)'), ylabel(YLABEL[io])
                title('Subject #'+str(iss)+' - Rho='+str(ir))
                grid(True)
    show()


table=filtData.pivot_table(Opt,index='Lambda',columns=['Subject','Rho','Meas'],aggfunc='mean')
comp=Components[Components['Lambda'].isin(filtData.Lambda.unique())].values
comp=delete(comp,0,1)
aComp=linalg.lstsq(comp[FIRST_LAMBDA:],table.Mua[FIRST_LAMBDA:],rcond=None)[0]
dfComp=DataFrame(data=aComp.transpose(),columns=Components.columns[1:],index=table.Mua.columns)
dfComp['tHb']=dfComp['HHb']+dfComp['O2Hb']
dfComp['SO2']=dfComp['O2Hb']/dfComp['tHb']
dfComp['Tot']=dfComp['Lipid']+dfComp['H2O']+dfComp['Coll']

pandas.options.display.max_columns = None
pandas.options.display.max_rows = None
pandas.options.display.max_colwidth = 10
pandas.options.display.width = None
pandas.options.display.precision = 2
display(dfComp)