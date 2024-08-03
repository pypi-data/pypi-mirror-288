#__author__ = "magnelPy"
# stochVar module within magnelPy.
# Provides standard formatting and simple functionality (PDF,CDF,inverseCDF) for stochastic variables.
# Call as >> from magnelPy import stochVar as sv
# note: help functionality of functions is incomplete


#--------------------------------------------------------------------------------------------------------
# Standard formatting stochastic variables
#--------------------------------------------------------------------------------------------------------

####################
## MODULE IMPORTS ##
####################

import numpy as np
import scipy as sp
from magnelPy import statFunc as sf

##############
## FUNCTION ##
##############

def createStochVar(name='',dist=None,mean=None,std=None,dim='[-]',comment='',theta1=None,theta2=None):
	""" Creates standard format (Dict) for stochastic variable
	Parameters
	----------		
	name : string
		name of the stochastic variable;
		default: ''
	dist : string
		distribution type; 
		options: 'normal';'lognormal';'mixedlognormal';'gumbel';'deterministic';'beta';'gamma';'uniform';'weibull';'lognormal_truncated'
		default: None
	mean : float
		mean value;
		default: None
	std : float
		standard deviation;
		default: None
	dim : string
		dimension;
	comment : string
		option to add notes to variable
	theta1 : float
		additional parameter - distribution specific
		default: None
		application: {beta:alpha; uniform:a; lognormal_truncated:b; }
	theta2 : float
		additional parameter - distribution specific
		default: None
		application: {beta:beta; uniform:b}

	Returns
	-------
	out : Dict
		standard format for stochastic variables

	Note
	----		
	- Specific distributions do not require the mean to be set, e.g., 'uniform'

	Example use
	-----------
	from magnelPy import stochVar as sv
	mX = 2; sX = 1; distX = 'lognormal' # parameters for variable X: lognormal distribution with mean 2 and stdev 1
	X = sv.createStochVar('X',distX,mX,sX) # creates stochVar X
	# evaluate 95% quantile value
	quant = 0.95
	print("{:.2f}".format(sv.Finvx(X,quant)))
	>>> 3.89	

	"""
	return {'name':name,'dist':dist,'dim':dim,'m':mean,'s':std,'info':comment,'theta1':theta1,'theta2':theta2}

def fx(varDict,xArray,SW_log=False):
	DistType=varDict['dist']
	if DistType=='normal':
		return sf.f_Normal(xArray,varDict['m'],varDict['s'],SW_log)
	if DistType=='lognormal':
		return sf.f_Lognormal(xArray,varDict['m'],varDict['s'],SW_log)
	if DistType=='mixedlognormal':
		return sf.f_MixedLN(xArray,varDict['mi'],varDict['si'],varDict['Pi'],SW_log)
	if DistType=='gumbel':
		return sf.f_Gumbel(xArray,varDict['m'],varDict['s'],SW_log)
	if DistType=='beta':
		return sf.f_Beta(xArray,varDict['m'],varDict['s'],varDict['theta1'],varDict['theta2'],SW_log)
	if DistType=='gamma':
		return sf.f_Gamma(xArray,varDict['m'],varDict['s'],SW_log)
	if DistType=='uniform':
		return sf.f_Uniform(xArray,varDict['theta1'],varDict['theta2'],SW_log)
	if DistType=='weibull':
		return sf.f_Weibull(xArray,varDict['m'],varDict['s'],SW_log)
	if DistType=='lognormal_truncated':
		return sf.f_Lognormal_truncated(xArray,varDict['m'],varDict['s'],varDict['theta1'],SW_log)

def Fx(varDict,xArray):
	DistType=varDict['dist']
	if DistType=='normal':
		return sf.F_Normal(xArray,varDict['m'],varDict['s'])
	if DistType=='lognormal':
		return sf.F_Lognormal(xArray,varDict['m'],varDict['s'])
	if DistType=='mixedlognormal':
		return sf.F_MixedLN(xArray,varDict['mi'],varDict['si'],varDict['Pi'])
	if DistType=='gumbel':
		return sf.F_Gumbel(xArray,varDict['m'],varDict['s'])
	if DistType=='beta':
		return sf.F_Beta(xArray,varDict['m'],varDict['s'],varDict['theta1'],varDict['theta2'])
	if DistType=='gamma':
		return sf.F_Gamma(xArray,varDict['m'],varDict['s'])
	if DistType=='uniform':
		return sf.F_Uniform(xArray,varDict['theta1'],varDict['theta2'])
	if DistType=='weibull':
		return sf.F_Weibull(xArray,varDict['m'],varDict['s'])
	if DistType=='lognormal_truncated':
		return sf.F_Lognormal_truncated(xArray,varDict['m'],varDict['s'],varDict['theta1'])

def Finvx(varDict,rArray):
	DistType=varDict['dist']
	if DistType=='normal':
		return sf.Finv_Normal(rArray,varDict['m'],varDict['s'])
	if DistType=='lognormal':
		return sf.Finv_Lognormal(rArray,varDict['m'],varDict['s'])
	if DistType=='mixedlognormal':
		return sf.Finv_MixedLN(rArray,varDict['mi'],varDict['si'],varDict['Pi'])
	if DistType=='gumbel':
		return sf.Finv_Gumbel(rArray,varDict['m'],varDict['s'])
	if DistType=='beta':
		return sf.Finv_Beta(rArray,varDict['m'],varDict['s'],varDict['theta1'],varDict['theta2'])
	if DistType=='gamma':
		return sf.Finv_Gamma(rArray,varDict['m'],varDict['s'])
	if DistType=='uniform':
		return sf.Finv_Uniform(rArray,varDict['theta1'],varDict['theta2'])
	if DistType=='weibull':
		return sf.Finv_Weibull(rArray,varDict['m'],varDict['s'])
	if DistType=='lognormal_truncated':
		return sf.Finv_Lognormal_truncated(rArray,varDict['m'],varDict['s'],varDict['theta1'])

## RF transformation ##
#######################

def RF_fxN_FxN(x,muN,sigN):
    uN=(x-muN)/sigN
    FxN=sf.F_Normal(uN,0,1)
    fxN=1/sigN*sf.f_Normal(uN,0,1)
    return FxN,fxN

def RF_deviation(parN,x,varDict):
    muN=parN[0];sigN=parN[1]
    fxx=fx(varDict,x); Fxx=Fx(varDict,x)
    FxN,fxN=RF_fxN_FxN(x,muN,sigN)
    return Fxx-FxN,fxx-fxN

def RF_muN_sigN_solver(x,varDict):
    out=sp.optimize.fsolve(RF_deviation,[varDict['m'],varDict['s']],args=(x,varDict))
    muN=out[0];sigN=out[1]
    return muN,sigN

def RF_transform(x,varDict):
    muN,sigN=RF_muN_sigN_solver(x,varDict)
    return (x-muN)/sigN,muN,sigN

    
##################
## AUX FUNCTION ##
##################


#########################
## STAND ALONE - DEBUG ##
#########################

if __name__ == "__main__":

	rebar = 0.01  #rebar diameter [m]
	dist = 0.1  #distance between rebars [m]
	w = 1.    #slab width [m]	

	As=createStochVar(dist='normal',mean=0.25*(np.pi)*rebar**2*(w/dist)*1.02,std=0.02*0.25*(np.pi)*rebar**2*(w/dist)*1.02,dim='[m2]',name='As [m2]')
	fck=30; Vfc=0.15 # [MPa]; [-]
	fc=createStochVar(dist='lognormal',mean=fck/(1-2*Vfc),std=fck/(1-2*Vfc)*Vfc,dim='[MPa]',name='fc20 [MPa]')

	StochVarDict={'As':As,'fc':fc}

	nameList=[StochVarDict[key]['name'] for key in StochVarDict.keys()]

	print(StochVarDict.keys())    
