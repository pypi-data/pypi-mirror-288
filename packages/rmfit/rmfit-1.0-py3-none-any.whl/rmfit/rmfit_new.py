import numpy as np
import pandas as pd
from corner import corner
import pyde
import pyde.de
import matplotlib.pyplot as plt
import emcee
import batman
import astropy.constants as aconst
import radvel
from .priors import PriorSet, UP, NP, JP, FP
from .likelihood import ll_normal_ev_py
from . import stats_help
from . import utils

class LPFunction(object):
    def __init__(self,x,y,yerr,file_priors):
        
    
        
    def compute_rm_model(self,pv,times=None):
        """
        Computes the RM model (excluding RV)
        
        INPUT:
            pv    - a list of parameters (only parameters that are being varied)
            times - times (optional), array of timestamps 
        
        OUTPUT:
            rm - the rm model evaluated at 'times' if supplied, otherwise 
                      defaults to original data timestamps
        """
        T0     =self.get_value(pv,'t0_p1')
        P      =self.get_value(pv,'P_p1')
        lam    =self.get_value(pv,'lam_p1')
        vsini  =self.get_value(pv,'vsini') 
        ii     =self.get_value(pv,'inc_p1')
        rprs   =self.get_value(pv,'p_p1')
        aRs    =self.get_value(pv,'a_p1')
        u1     =self.get_value(pv,'u1')
        #u2     =self.get_value(pv,'u2')
        gamma  =self.get_value(pv,'gamma')
        beta   =self.get_value(pv,'vbeta')
        #sigma  =self.get_value(pv,'sigma')
        sigma  =vsini /1.31 # assume sigma is vsini/1.31 (see Hirano et al. 2010, 2011)
        e      =self.get_value(pv,'ecc_p1')
        omega  =self.get_value(pv,'omega_p1')
        exptime=self.get_value(pv,'exptime')/86400. # exptime in days
        if times is None:
            times = self.data["x"]
        self.RH = RMHirano(lam,vsini,P,T0,aRs,ii,rprs,e,omega,[u1],beta,
                            sigma,supersample_factor=7,exp_time=exptime,limb_dark='linear')
        self.rm = self.RH.evaluate(times)
        return self.rm

        
                    
    def __call__(self,pv):
        y_model = self.compute_total_model(pv)
        # Return the log-likelihood
        log_of_priors = self.ps_vary.c_log_prior(pv)
        log_of_model  = ll_normal_ev_py(self.data["x"], y_model, self.data['error'])
        log_ln = log_of_priors + log_of_model
        return log_ln

class RMFit(object):
    
    
    def minimize_PyDE(self,npop=100,de_iter=200,mc_iter=1000,mcmc=True,threads=8,maximize=True,plot_priors=True,sample_ball=False,k=None,n=None):
        """
        Minimize using the PyDE
        
        NOTES:
        https://github.com/hpparvi/PyDE
        """
        centers = np.array(self.lpf.ps_vary.centers)
        print("Running PyDE Optimizer")
        self.de = pyde.de.DiffEvol(self.lpf, self.lpf.ps_vary.bounds, npop, maximize=maximize) # we want to maximize the likelihood
        self.min_pv, self.min_pv_lnval = self.de.optimize(ngen=de_iter)
        print("Optimized using PyDE")
        print("Final parameters:")
        self.print_param_diagnostics(self.min_pv)
        #self.lpf.ps.plot_all(figsize=(6,4),pv=self.min_pv)
        print("LogPost value:",-1*self.min_pv_lnval)
        self.lnl_max  = -1*self.min_pv_lnval-self.lpf.ps_vary.c_log_prior(self.min_pv)
        print("LnL value:",self.lnl_max)
        print("Log priors",self.lpf.ps_vary.c_log_prior(self.min_pv))
        if k is not None and n is not None:
            print("BIC:",stats_help.bic_from_likelihood(self.lnl_max,k,n))
            print("AIC:",stats_help.aic(k,self.lnl_max))
        if mcmc:
            print("Running MCMC")
            self.sampler = emcee.EnsembleSampler(npop, self.lpf.ps_vary.ndim, self.lpf,threads=threads)
            #pb = ipywidgets.IntProgress(max=mc_iter/50)
            #display(pb)
            #val = 0
            print("MCMC iterations=",mc_iter)
            for i,c in enumerate(self.sampler.sample(self.de.population,iterations=mc_iter)):
                print(i,end=" ")
                #if i%50 == 0:
                    #val+=50.
                    #pb.value += 1
            print("Finished MCMC")
            self.min_pv_mcmc = self.get_mean_values_mcmc_posteriors().medvals.values
    
    
    
    def plot_lc(self,pv,times=None):
        """
        Plot the light curve for a given set of parameters pv
        
        INPUT:
        pv - an array containing a sample draw of the parameters defined in self.lpf.ps
        
        EXAMPLE:
        
        """
        self.scaled_flux   = self.lpf.data["y"]
        self.model_trend   = self.lpf.compute_total_model(pv)
        self.residual      = self.scaled_flux - self.model_trend
        try:
            self.scaled_error  = self.lpf.data["error"]#/pv[self.lpf.number_pv_baseline]
        except Exception as e:
            self.scaled_error = pv[self.lpf.number_pv_error]#/pv[self.lpf.number_pv_baseline]
        
        nrows = 2
        self.fig, self.ax = plt.subplots(nrows=nrows,sharex=True,figsize=(10,6),
                                         gridspec_kw={'height_ratios': [5, 2]})
        self.ax[0].errorbar(self.lpf.data["x"],self.scaled_flux,yerr=self.scaled_error,
                elinewidth=1,lw=0,alpha=1,capsize=5,mew=1,marker="o",barsabove=True,markersize=8,
                            label="Data with trend")
        self.ax[0].plot(self.lpf.data["x"],self.model_trend,label="Model with trend",color='crimson')
        #self.ax[1].errorbar(self.lpf.data["time"],self.scaled_flux_no_trend,yerr=self.scaled_error,elinewidth=0.3,lw=0,alpha=0.5,marker="o",markersize=4,label="Data, no trend")
        #self.ax[1].plot(self.lpf.data["time"],self.model_no_trend,label="Model no trend")
        self.ax[1].errorbar(self.lpf.data["x"],self.residual,yerr=self.scaled_error,
                elinewidth=1,lw=0,alpha=1,capsize=5,mew=1,marker="o",barsabove=True,markersize=8,
                            label="residual, std="+str(np.std(self.residual)))
        #self.ax[2].plot(self.lpf.data["x"],self.residual,label="residual, std="+str(np.std(self.residual)),lw=0,marker="o",ms=3)
        [self.ax[i].minorticks_on() for i in range(nrows)]
        [self.ax[i].legend(loc="lower left",fontsize=8) for i in range(nrows)]
        self.ax[-1].set_xlabel("Time (BJD)",labelpad=2)
        [self.ax[i].set_ylabel("RV [m/s]",labelpad=2) for i in range(nrows)]
        self.ax[0].set_title("RM Effect")
        self.fig.subplots_adjust(wspace=0.05,hspace=0.05)




    
    def Xp(self,times):
        lam, w, i = np.deg2rad(self.lam), np.deg2rad(self.w), np.deg2rad(self.i)
        f = self.true_anomaly(times)
        r = self.aRs*(1.-self.e**2.)/(1.+self.e*np.cos(f)) # distance
        # Working for lam = 0, 180., i = 90.
        # x = -r*np.cos(f+w)*np.cos(lam)
        # Working for lam = 0, 180., i = 90., why positive sign on the other one? - due to rotation matrix
        x = -r*np.cos(f+w)*np.cos(lam) + r*np.sin(lam)*np.sin(f+w)*np.cos(i)
        return x

    def evaluate(self,times,base_error=0.):
        sigma = self.sigma
        beta = self.beta
        X = self.Xp(times)
        F = 1.-self.calc_transit(times)
        vp = X*self.Omega*np.sin(self.iS)*self.rstar*aconst.R_sun.value/1000.
        v = -1000.*vp*F*((2.*beta**2.+2.*sigma**2)/(2.*beta**2+sigma**2))**(3./2.) * (1.-(vp**2.)/(2.*beta**2+sigma**2) + (vp**4.)/(2.*(2.*beta**2+sigma**2)**2.))
        #v = -1000.*vp*F*((2.*beta**2.+2.*sigma**2)/(2.*beta**2+sigma**2))**(3./2.) * (1.-(vp**2.)/(2.*beta**2+sigma**2))# + (vp**4.)/(2.*(2.*beta**2+sigma**2)**2.))
        # For diagnostics
        self.vp = vp
        self.X = X
        self.F = F
        if base_error >0:
            return v + np.random.normal(loc=0.,scale=base_error,size=len(v))
        else:
            return v

def true_anomaly(time,T0,P,aRs,inc,ecc,omega):
    params = batman.TransitParams()
    params.t0 = T0                           #time of inferior conjunction
    params.per = P                           #orbital period
    params.rp = 0.1                          #planet radius (in units of stellar radii)
    params.a = aRs                           #semi-major axis (in units of stellar radii)
    params.inc = inc                         #orbital inclination (in degrees)
    params.ecc = ecc                         #eccentricity
    params.w = omega                         #longitude of periastron (in degrees)
    params.u = [0.3,0.3]                     #limb darkening coefficients [u1, u2]
    params.limb_dark = "quadratic"           #limb darkening model
    m = batman.TransitModel(params, time)    #initializes model
    return m.get_true_anomaly()

def planet_XYZ_position(time,T0,P,aRs,inc,ecc,omega):
    f = true_anomaly(time,T0,P,aRs,inc,ecc,omega) # true anomaly in radiance
    omega = np.deg2rad(omega)
    inc = np.deg2rad(inc)
    r = aRs*(1.-ecc**2.)/(1.+ecc*np.cos(f)) # distance
    X = -r*np.cos(omega+f)
    Y = -r*np.sin(omega+f)*np.cos(inc)
    Z = r*np.sin(omega+f)*np.sin(inc)
    return X, Y, Z

def get_rv_curve(times_jd,P,tc,e,omega,K):
    t_peri = radvel.orbit.timetrans_to_timeperi(tc=tc,per=P,ecc=e,omega=np.deg2rad(omega))
    rvs = radvel.kepler.rv_drive(times_jd,[P,t_peri,e,np.deg2rad(omega),K])
    return rvs
