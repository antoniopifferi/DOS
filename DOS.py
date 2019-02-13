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
SHOW_SINGLE=True
SHOW_TABLE=True
Opt=['Mua','Mus']
YLIM={'Mua':[0,0.5],'Mus':[0,20]}
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
FileData='MAYm0023.txt'
FileTrim='trimMAYm0023.txt'
FileKey='keyMAYm0023.txt'
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
if SHOW_SINGLE:
    for iss in filtData.Subject.unique():
        for ip in filtData.Pos.unique():
            fig=figure(figsize=cm2inch(40, 15))
            table=filtData[(filtData.Subject==iss)&(filtData.Pos==ip)].pivot_table(Opt,index='Lambda',columns=['Rho'],aggfunc='mean')
            for io in Opt:
                fig.add_subplot(1,2,1+Opt.index(io))
                plot(table[io])
                ylim(YLIM[io]), legend(table[io]), xlabel('wavelength (nm)'), ylabel(YLABEL[io])
                title('Subject #'+str(iss)+' - Pos='+str(ip))
                grid(True)
show()
        
table=filtData.pivot_table(Opt,index='Lambda',columns=['Subject','Pos','Rho'],aggfunc='mean')
comp=Components[Components['Lambda'].isin(filtData.Lambda.unique())].values
comp=delete(comp,0,1)
aComp=linalg.lstsq(comp[2:],table.Mua[2:],rcond=None)[0]
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