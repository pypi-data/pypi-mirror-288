# -*- coding: utf-8 -*-

import numpy as np
import scipy
import warnings

from pathlib import Path



rng = np.random.default_rng()

chainpath=Path(__file__).parent/ 'chain4b.txt'
flatchain=np.genfromtxt(chainpath.open())

uncpath=Path(__file__).parent/ 'ErrorsBigList.dat'
PrhoUnc=np.genfromtxt(uncpath.open())
PrhoUncsplines=scipy.interpolate.interp1d(PrhoUnc[:,0],PrhoUnc[:,1:],axis=0)

__all__=["get_Rsamp","get_Psamp","get_Psamp_Unc","Pressure","Radius",r"get_maxMtov",r"get_maxrhotov",
         r"get_MAP",r"MRcs_TOV",r"MR_sample"]


bfpath=Path(__file__).parent/ 'bf4b.txt'

bfs=np.genfromtxt(bfpath.open())
bestfits={"P":bfs[0], "rho":bfs[1], "r12":bfs[2], "M":bfs[3], "R":bfs[4]}


maxMtov=np.max(flatchain[:,3])
maxrhotov=np.max(flatchain[:,1])

#
clight=2.998e10
G=6.67e-8
rho0=2.8e14
Msun=1.988e33
RJ=clight/np.sqrt(G*rho0)/1.e5
MJ=rho0*(RJ*1.e5)**3/Msun
#

def get_maxMtov():
    """

    Returns
    -------
    The global maximal Mtov value in the current model.

    """
    
    return maxMtov

def get_maxrhotov():
    """
    

    Returns
    -------
    The global maximal rhotov value in the current model.

    """

    
    return maxrhotov


def get_MAP():
    """
    

    Returns
    -------
    Maximal aposteriori estimate for the current model (aka best-fit). 
    Output is a dictionary with the key names
    {"P", "rho", "r12", "M", "R"}.
    All parameters except r12 correspond to the TOV point.
    """
    return bestfits

def MR(m,rho):
    a= -0.492
    mu = np.sqrt(1-m)
    mu2=1-m
    c=0.8284271247461903
    return 1+mu*(a+c*rho) + mu2*(-2.-np.sqrt(2)*a+c*rho)

def Radius(M, mtov=bestfits["M"],rtov=bestfits["R"],r12=bestfits["r12"]):
    """
    Return NS radius R at a given M according to the universal expression (1) from the OSP24 paper.
    By default, the values of Mtov, Rtov, and r12 are set at their best-fit values for the current model.

    Parameters
    ----------
    M : NS mass (can be an array of masses) in units of solar masses
    
    mtov : optional, the default is the current best-fit value.
        TOV mass in units of Solar mass
    rtov : : optional, the default is the current best-fit value.
        TOV radius in km
    r12 : optional, the default is the current best-fit value.
        Radius of M=Mtov/2 mass NS relative to Rtov 

    Returns
    -------
    NS radius in km
    
    """
    if M> mtov:
        return None
    
    return rtov*MR(M/mtov,r12)




def get_Rsamp(M,Nsamp=1,get_weight=False):
    """
    Sample Nsamp NS radii at given M. If get_weight is True, 
    returns also the porbability that M<Mtov.

    Parameters
    ----------
    M : NS mass in the units of the Solar mass
    Nsamp : Number of samples. The default is 1.
    get_weight : To return the probability of M<Mtov

    Returns
    -------
    Radii samples (in km).
    If get_weight=True, returns a list of Radii sample and M<Mtov probability.

    """    

    
    sel=flatchain[:,3]>M
    chain_sel=rng.choice(flatchain[sel],size=Nsamp)

    Rs=chain_sel[:,4]*MR(M/chain_sel[:,3],chain_sel[:,2])
    if not(get_weight):
         return Rs
    else:
         return Rs,sel.sum()/len(flatchain)

def fddo(pmax,rhomax,vec):
    (a,b,c,d)=vec
    return c*(pmax**a)*(rhomax**b)+d

vecM=[1.4092,-1.3914,5.8621,0.27259]
vecR=[0.5182,-0.5937,2.744,-0.07410]
vecc=[0.764,-0.780,3.27,0.187]    
    
def gamma_ddo(pmax,rhomax):
    return fddo(pmax,rhomax,vecc)/fddo(pmax,rhomax,vecR)


def MRcs_TOV(Ptov,rhotov):
    """
    
    Universal correlations between the TOV NS star parameters according to Eq.(2) of the OSP24 paper.
    
    Parameters
    ----------
    Ptov : TOV pressure in CGS
    rhotov : TOV density in CGS

    Returns
    -------
    Array of Mtov (in Solar mass), Rtov (in km), sound speed in the center of the TOV star (in the speed of light)

    """
    rhonorm=rhotov/rho0
    Pnorm=Ptov/(rho0*clight**2)
    
    Mtov=MJ*Pnorm**1.5/rhonorm**2/fddo(Pnorm,rhonorm,vecM)
    
    Rtov=RJ*Pnorm**0.5/rhonorm/fddo(Pnorm,rhonorm,vecR)
    
    cstov=np.sqrt(Pnorm/rhonorm)*gamma_ddo(Pnorm,rhonorm)
    
    return np.array([Mtov, Rtov, cstov])
    

def relPhigh(relrho,pmax,rhomax):
    gamma=gamma_ddo(pmax,rhomax)
    zeta=np.sqrt(pmax/rhomax)*gamma
    a0=-0.392;b0=-0.869;b1=1.69;p=2.98
    
    return (relrho**(gamma**2-a0))/(1+a0*(1-relrho)+(b0+b1*zeta)*(1-relrho)**p)

def Pressure(rho,pmax=bestfits["P"],rhomax=bestfits["rho"],r12=bestfits["r12"]):
    """
    Return pressure P at a given density rho according to the universal expression (4) from the OSP24 paper.
    By default, the values of Ptov, rhotov, and r12 are set at their best-fit values for the current model.
    Parameters
    ----------
    rho : Density (can be array of densities) in units of rho0.
    pmax : optional, the default is the current best-fit value.
        TOV pressure in units of rho0 c^2
    rhomax : optional, the default is the current best-fit value.
        TOV density in units of rho0 
    r12 : optional, the default is the current best-fit value.
        Radius of M=Mtov/2 mass NS relative to Rtov 

    Returns
    -------
    None.

    """

    relrho=rho/rhomax
    Phigh=pmax*relPhigh(relrho,pmax,rhomax)

    u0=-61.2;u1=81.9; u2=-27.2; v=1.33

    return Phigh*np.exp((u0+u1*r12+u2*r12**2)*(np.exp(-v*rho)- np.exp(-v*rhomax)))

def get_Psamp(rho,Nsamp=1,get_weight=False):
    """
    Sample Nsamp pressure values (in units of rho0 c^2) at given density (in units of rho0). If get_weight is True, 
    returns also the porbability that rho<rhotov.

    Parameters
    ----------
    rho : density in the units of rho0.
    Nsamp : Number of samples. The default is 1.
    get_weight : To return the probability of rho<rhotov

    Returns
    -------
    Pressure samples (in rho0 c^2).
    If get_weight=True, returns a list of pressure sample and rho<rhotov probability.

    """    

    sel=flatchain[:,1]>rho
    chain_sel=rng.choice(flatchain[sel],size=Nsamp)
    Ps=Pressure(rho,chain_sel[:,0],chain_sel[:,1],chain_sel[:,2])
    
    if not(get_weight):    
        return Ps
    else:
        return Ps, sel.sum()/len(flatchain)

def get_Psamp_Unc(rho,Nsamp=1, get_weight=False):
    """
    Sample Nsamp pressure values (in units of rho0 c^2) at given density (in units of rho0) accounting for the uncertaities of the universal approximations.
    If get_weight is True, 
    returns also the porbability that rho<rhotov.

    Parameters
    ----------
    rho : density in the units of rho0.
    Nsamp : Number of samples. The default is 1.
    get_weight : To return the probability of rho<rhotov

    Returns
    -------
    Pressure samples (in rho0 c^2).
    If get_weight=True, returns a list of pressure sample and rho<rhotov probability.

    """       

    sel=flatchain[:,1]>rho
    chain_sel=rng.choice(flatchain[sel],size=Nsamp)
    Ps=Pressure(rho,chain_sel[:,0],chain_sel[:,1],chain_sel[:,2])
    
    relrhomaxes=(rho-1.)/(chain_sel[:,1]-1.)

  
    BoostUnc=np.apply_along_axis(rng.choice,1,PrhoUncsplines(relrhomaxes))
    Ps=Ps*(1+BoostUnc)

    if not(get_weight):    
        return Ps
    else:
        return Ps, sel.sum()/len(flatchain)



def MR_sample(nsamp=10000,maxMtov=None):
   """
    
    Generate nsamp samples from a posterior predictive density for a singe NS Mass and Radius.
    The sampling assumes uniform prior distribution of M between 1 Solar mass and maxMtov.
    If maxMtov not set, MR_sample employs global maximal Mtov value in the current chain.
    
    
    
    Parameters
    ----------
    nsamp : Optional, The Default is 10000.
        Number of samples generated.
    maxMtov :  Optional. The Default is None.
       Upper bound for the unimform M samplig. 
       If None, is set to the global maximal Mtov value in the current chain.

    Returns
    -------
    Numpy array Msamp*2 of masses ad radii.    

   """    
   if maxMtov==None: 
        maxMtov=np.max(flatchain[:,0])


   chain_sel=rng.choice(flatchain,size=nsamp)
   Ms=scipy.stats.uniform(1.,maxMtov).rvs(nsamp)

   sel=Ms<chain_sel[:,3]

   Rs=chain_sel[sel,4]*MR(Ms[sel]/chain_sel[sel,3],chain_sel[sel,2])


   return  np.transpose([Ms[sel],Rs])




