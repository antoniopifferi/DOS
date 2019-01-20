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
FileLab='keyMAYm0000.txt'
FileSet='LambdaSetPaolaMod.txt'
FileComponents='Components0.txt'
PathFigure=PathAnalysis+DirFigure
LabelLambdaSet=('L51','L27','L17','L13','L11')
#dictCol={'Mus': 'newMus', 'Mua': 'newMua'}

# SELECT KEYS
Key1='Subject'
Key2='Task'

# LOAD COMPONENTS
Components=read_table(PathAnalysis+FileComponents)
LambdaSet=read_table(PathAnalysis+FileSet)
LambdaSet=LambdaSet.fillna(-1).astype(np.int64)
Components.plot(x='Lambda')
yscale('log')
ylim([0,0.5]), title('Components'), xlabel('wavelength (nm)'), ylabel('specific absorption (cm-1)')
savefig(PathFigure+'Components.jpg')
show()

# LOAD DICT
with open(PathAnalysis+FileLab) as f:
  dcLab = dict(x.rstrip().split(None, 1) for x in f)

# LOAD DATA
data=read_table(PathAnalysis+FileData)
data.rename(columns=dcLab,inplace=True)
Trim=read_table(PathAnalysis+FileTrim)
data=merge(data,Trim)
#data=data.rename(columns=dictCol)

compAll=DataFrame()
# PLOT DATA
for ip in data.Task.unique():
    for il in LabelLambdaSet:
#    for ir in data.Rho.unique():
        ir=il #dangerous!!!!
        iLambda=LambdaSet[il]
        table=data[(data.Det==data.Trim)&(data.Task==ip)&(data.Lambda.isin(iLambda))].pivot_table(['Mua','Mus'],index='Lambda',columns=['Task','Subject','Rho','Meas'],aggfunc='mean')
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
        
        table.to_csv(PathFigure+namefig+'S.csv')
        
        comp=Components[Components['Lambda'].isin(iLambda)].values
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
        dfComp['LambdaSet']=il
        compAll=compAll.append(dfComp)
        
writer = ExcelWriter('reportAdd.xlsx')
#compAll.to_excel(writer, 'Sheet1_{}_{}'.format(row_index, col_index))
compAll.ffill(inplace=True)
compAll.to_excel(writer)
writer.save()