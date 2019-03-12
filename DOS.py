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
SHOW_TABLE=False
PLOT_COMP=False
#Task='Abdomen'
Task='Muscle'
Opt=['Mua','Mus']
YLIM={'Mua':[0,0.5],'Mus':[0,20]}
YLABEL={'Mua':'absorption (cm-1)','Mus':'reduced scattering (cm-1)'}
COMP_LIST=['HHb','O2Hb','tHb','SO2','Lipid','H2O','Coll','Tot']

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
    FileDataSpect='MAYm0023_Spect.txt'
    FileTrim='trimMAYm0023.txt'
    FileKey='keyMAYm0023.txt'
    FIRST_LAMBDA=0
else:
    FileData='MAYm0024.txt'
    FileTrim='trimMAYm0024.txt'
    FileKey='keyMAYm0024.txt'
    FIRST_LAMBDA=2
    
#FileComponents='Components2.txt'
#FileComponents='ComponentsNoColl.txt'
FileComponents='ComponentsNoBkg.txt'
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

# CALCULATE COMPONENTS
table=filtData.pivot_table(Opt,index='Lambda',columns=['Subject','Meas','Rho'],aggfunc='mean')
comp=Components[Components['Lambda'].isin(filtData.Lambda.unique())].values
comp=delete(comp,0,1)
aComp=linalg.lstsq(comp[FIRST_LAMBDA:],table.Mua[FIRST_LAMBDA:],rcond=None)[0] #[0] to extract m-coeff in lstsq
dfComp=DataFrame(data=aComp.transpose(),columns=Components.columns[1:],index=table.Mua.columns)
dfComp['tHb']=dfComp['HHb']+dfComp['O2Hb']
dfComp['SO2']=dfComp['O2Hb']/dfComp['tHb']
dfComp['Tot']=dfComp['Lipid']+dfComp['H2O']+dfComp['Coll']
dfComp['FitComp']='LambdaFit'
filtData=merge(filtData,dfComp,on=['Subject','Meas','Rho'])

# LOAD SPECT DATA
rawDataSpect=read_table(PathAnalysis+FileDataSpect)
rawDataSpect.drop_duplicates(inplace=True)
#filtData=merge(filtData,rawDataSpect,on=['Subject','Meas','Rho','FitComp'],how='left')
filtData=concat([filtData,rawDataSpect])

# CALCULATE DERIVED COMPONENTS
filtData['tHb']=filtData['HHb']+filtData['O2Hb']
filtData['SO2']=filtData['O2Hb']/filtData['tHb']
filtData['Tot']=filtData['Lipid']+filtData['H2O']+filtData['Coll']



# PLOT SINGLE
if PLOT_SINGLE:
    for iss in filtData.Subject.unique():
        for im in filtData.Meas.unique():
            age=filtData[(filtData.Subject==iss)&(filtData.Meas==im)].Age.unique()
            thick=filtData[(filtData.Subject==iss)&(filtData.Meas==im)].Thickness.unique()
            bmi=filtData[(filtData.Subject==iss)&(filtData.Meas==im)].BMI.unique()
            fig=figure(figsize=cm2inch(40, 15))
            table=filtData[(filtData.Subject==iss)&(filtData.Meas==im)].pivot_table(Opt,index='Lambda',columns=['Rho'],aggfunc='mean')
            for io in Opt:
                fig.add_subplot(1,2,1+Opt.index(io))
                plot(table[io])
                ylim(YLIM[io]), legend(table[io]), xlabel('wavelength (nm)'), ylabel(YLABEL[io])
                #title('Subject #'+str(iss)+' - Meas='+str(im))
                title('#'+str(iss)+'-Age='+str(age)+'-BMI='+str(bmi)+'-Thk='+str(thick)+'-Meas='+str(im))
                grid(True)
    show()

if PLOT_MULTI:
    for io in Opt:
        for iss in filtData.Subject.unique():
            fig=figure(figsize=cm2inch(40, 15))
            Rho=list(filtData.Rho.unique())
            for ir in Rho:
                age=filtData[(filtData.Subject==iss)&(filtData.Rho==ir)].Age.unique()
#                thick=0.2*sum(filtData[(filtData.Subject==iss)&(filtData.Rho==ir)].Thickness.unique())
                bmi=filtData[(filtData.Subject==iss)&(filtData.Rho==ir)].BMI.unique()
                table=filtData[(filtData.Subject==iss)&(filtData.Rho==ir)].pivot_table(Opt,index='Lambda',columns=['Meas'],aggfunc='mean')
                fig.add_subplot(1,len(Rho),1+Rho.index(ir))
                plot(table[io])
                ylim(YLIM[io]), legend(table[io]), xlabel('wavelength (nm)'), ylabel(YLABEL[io])
                #title('#'+str(iss)+'-Age='+str(age)+'-BMI='+str(bmi)+'-Thk='+str(thick)+' - Rho='+str(ir))
                title('#'+str(iss)+'-Age='+str(age)+'-BMI='+str(bmi)+' - Rho='+str(ir))
                grid(True)
    show()


# Show Components
pandas.options.display.max_columns = None
pandas.options.display.max_rows = None
pandas.options.display.max_colwidth = 10
pandas.options.display.width = None
pandas.options.display.precision = 2
#with pandas.option_context('display.multi_sparse', False):
display(dfComp)
dfComp = dfComp.reset_index()
dfComp.to_csv(PathAnalysis+'dfComp.csv', index=False)
#dfComp.T.plot(subplots=True,layout=[10,40],figsize=[20,10])

# Show Components from filtData
table=filtData[filtData.FitComp=='LambdaFit'].pivot_table(index=['Subject','Rho'],columns=['SO2','H2O'],aggfunc='mean')
#display(filtData)

# PLOT COMPONENTS
filtData[COMP_LIST].fillna(0)
for ifc in filtData.FitComp.unique():
    for ic in COMP_LIST:
        table=filtData[filtData.FitComp==ifc].pivot_table(ic,index='Meas',columns=['Rho','Subject'],aggfunc='mean')
        numRho=len(filtData.Rho.unique())
        numSubject=len(filtData.Subject.unique())
        table.plot(subplots=True,layout=[numRho,numSubject],sharex=True,sharey=True,title=ic+', '+ifc)
        subplots_adjust(wspace=0, hspace=0)
