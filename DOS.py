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
FileData='MAYm0023.txt'
FileTrim='trimMAYm0023.txt'
FileKey='keyMAYm0023.txt'
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

# LOAD DICT
#with open(PathAnalysis+FileLab) as f:
#  dcLab = dict(x.rstrip().split(None, 1) for x in f)
dataKey=read_table(PathAnalysis+FileKey)
dcKey=dict(zip(dataKey.Key, dataKey.Value))


# LOAD DATA
data=read_table(PathAnalysis+FileData)
data.rename(columns=dcKey,inplace=True)
Trim=read_table(PathAnalysis+FileTrim)
data=merge(data,Trim)
#data=data.rename(columns=dictCol)

# PLOT DATA
for iss in data.Subject.unique():
    for ip in data.Pos.unique():
        table=data[(data.Det==data.Trim)&(data.Accept=='OK')&(data.Subject==iss)&(data.Pos==ip)].pivot_table(['Mua','Mus'],index='Lambda',columns=['Rho'],aggfunc='mean')
#        namefig='Mua_'+ip+'_'+str(ir)
#        figure(namefig)
        figure()
        plot(table.Mua)
        grid(True)
#        title(ip+' - Rho='+str(ir))
        ylim([0,0.6]), legend(table.Mua), xlabel('wavelength (nm)'), ylabel('absorption (cm-1)')
#        savefig(PathFigure+namefig+'.jpg')
        show()
        
#        namefig='Mus_'+ip+'_'+str(ir)
#        figure(namefig)
#        plot(table.Mus)
#        grid(True)
#        title(ip+' - Rho='+str(ir))
#        ylim([0,15.0]), legend(table.Mus), xlabel('wavelength (nm)'), ylabel('reduced scattering (cm-1)')
#        savefig(PathFigure+namefig+'.jpg')
#        show() 

table=data[(data.Det==data.Trim)&(data.Accept=='OK')].pivot_table(['Mua','Mus'],index='Lambda',columns=['Subject','Pos','Rho'],aggfunc='mean')
comp=Components[Components['Lambda'].isin(data.Lambda.unique())].values
comp=delete(comp,0,1)
aComp=linalg.lstsq(comp[2:],table.Mua[2:],rcond=None)[0]
dfComp=DataFrame(data=aComp.transpose(),
                 columns=Components.columns[1:],
                 index=table.Mua.columns)
dfComp['tHb']=dfComp['HHb']+dfComp['O2Hb']
dfComp['SO2']=dfComp['O2Hb']/dfComp['tHb']
dfComp['Tot']=dfComp['Lipid']+dfComp['H2O']+dfComp['Collagen']
dfComp = dfComp.applymap("{0:.2f}".format)
# print('SECTION ON '+ip+' - Rho='+str(ir))
display(dfComp)
print(dfComp.to_string())
# dfComp.to_csv(PathFigure+namefig+'.csv')