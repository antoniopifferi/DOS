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

# PARAMETERS
PathAnalysis='D:\\Beta\\Analysis\\Maybe\\'
DirFigure='Figure\\'
FileData='MAYm0000_ref01.txt'
FileTrim='Trim.txt'
FileComponents='Components2.txt'
PathFigure=PathAnalysis+DirFigure
#dictCol={'Mus': 'newMus', 'Mua': 'newMua'}

# LOAD COMPONENTS
Components=read_table(PathAnalysis+FileComponents)
Components.plot(x='Lambda')
yscale('log')
ylim([0,0.5]), title('Components'), xlabel('wavelength (nm)'), ylabel('specific absorption (cm-1)')
savefig(PathFigure+'Components.jpg')
show()

# LOAD DATA
data=read_table(PathAnalysis+FileData)
Trim=read_table(PathAnalysis+FileTrim)
data=merge(data,Trim)
#data=data.rename(columns=dictCol)

# PLOT DATA
for ip in data.Pos.unique():
    for ir in data.Rho.unique():
        table=data[(data.Det==data.Trim)&(data.Pos==ip)].pivot_table(['Mua','Mus'],index='Lambda',columns=['Sample','Meas'],aggfunc='mean')
        namefig='Mua_'+ip+'_'+str(ir)
        figure(namefig)
        plot(table.Mua)
        grid(True)
        title(ip+' - Rho='+str(ir))
        ylim([0,0.6]), legend(table.Mua), xlabel('wavelength (nm)'), ylabel('absorption (cm-1)')
        savefig(PathFigure+namefig+'.jpg')
        show()
        
        namefig='Mus_'+ip+'_'+str(ir)
        figure(namefig)
        plot(table.Mus)
        grid(True)
        title(ip+' - Rho='+str(ir))
        ylim([0,15.0]), legend(table.Mus), xlabel('wavelength (nm)'), ylabel('reduced scattering (cm-1)')
        savefig(PathFigure+namefig+'.jpg')
        show() 

        comp=Components[Components['Lambda'].isin(data.Lambda.unique())].values
        comp=delete(comp,0,1)
        aComp=linalg.lstsq(comp[2:],table.Mua[2:],rcond=None)[0]
        dfComp=DataFrame(data=aComp.transpose(),
                         columns=Components.columns[1:],
                         index=table.Mua.columns)
        dfComp['tHb']=dfComp['HHb']+dfComp['O2Hb']
        dfComp['SO2']=dfComp['O2Hb']/dfComp['tHb']
        dfComp = dfComp.applymap("{0:.2f}".format)
        print('SECTION ON '+ip+' - Rho='+str(ir))
        display(dfComp)
        dfComp.to_csv(PathFigure+namefig+'.csv')