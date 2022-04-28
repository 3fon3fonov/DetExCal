#!/usr/bin/python3

##
 
 
from __future__ import print_function


import sys, os
import numpy as np
#sys.path.insert(0, '../lib')
sys.path.append('./lib/detexcal/')
 

class getSNR:


    def __init__(self,signal=1,bgnd=0,readnoise=0,DCurent=0,npix=1,time=1,gain=1,mag=0,aperture = 1,throughput = 1,bandwidth=0.55,quant_eff=1 ):
    
    
        self.signal=signal
        self.bgnd=bgnd
        self.readnoise=readnoise
        self.DCurent=DCurent
        self.npix=npix
        self.time=time
        self.gain=gain
        self.mag=mag
        self.aperture = aperture
        self.throughput = throughput
        self.bandwidth = bandwidth 
        self.quant_eff = quant_eff

        self.snr = []
        self.IntSignal =[] 
        self.IntPhotonNoise =[] 
        self.IntBackground =[] 
        self.IntDCurent =[] 
        self.IntReadNoise =[] 
        self.TotalNoise = []


    def magnitude_to_flux(self,magnitude):
        return 9.6e10*(10**(-magnitude/2.5))  # phot. /(um m^2 sec)
 
    def ccd_SNR_vs_time(self):
        """
        CCD equation. Gain is ignorred for now.
        """
 
        RN = (self.readnoise**2)*self.npix
        snr = []
        Int_signal =[] 
        Int_photnoise =[] 
        Int_bgnd =[] 
        Int_DCurent =[] 
        Int_readnoise =[] 
        Total_noise = []
        
        for i in np.atleast_1d(np.array(self.time)):
            SI = self.signal*self.gain*i
            BG = self.bgnd*self.npix*i
            DC = self.DCurent*self.npix*i

            snr.append(SI / (np.sqrt( SI + BG + DC + RN )))   
    
            Int_signal.append(SI)
            Int_photnoise.append(np.sqrt(SI))  
            Int_bgnd.append(np.sqrt(BG))
            Int_DCurent.append(np.sqrt(DC))
            Int_readnoise.append(np.sqrt(RN))
            Total_noise.append( np.sqrt( SI + BG + DC + RN ))
            
        self.snr = np.array(snr)
        self.IntSignal = np.array(Int_signal)
        self.IntPhotonNoise =np.array(Int_photnoise) 
        self.IntBackground =np.array(Int_bgnd)
        self.IntDCurent =np.array(Int_DCurent) 
        self.IntReadNoise =np.array(Int_readnoise) 
        self.TotalNoise = np.array(Total_noise)

        return 


    def ccd_SNR_vs_mag(self):
 
        RN = (self.readnoise**2)*self.npix
        snr = []
        Int_signal =[] 
        Int_photnoise =[] 
        Int_bgnd =[] 
        Int_DCurent =[] 
        Int_readnoise =[] 
        Total_noise = []

        BG = self.bgnd*self.npix*self.time
        DC = self.DCurent*self.npix*self.time

        for mag in np.atleast_1d(np.array(self.mag)):
            flux = self.magnitude_to_flux(mag) #airmass?
            signal  = flux*(np.pi*self.aperture**2)*(self.throughput)*(self.bandwidth)*(self.quant_eff)

            SI = signal*self.gain*self.time
            snr.append(SI / (np.sqrt( SI + BG + DC + RN ))) 

            Int_signal.append(SI)
            Int_photnoise.append(np.sqrt(SI))  
            Int_bgnd.append(np.sqrt(BG))
            Int_DCurent.append(np.sqrt(DC))
            Int_readnoise.append(np.sqrt(RN))
            Total_noise.append( np.sqrt( SI + BG + DC + RN ))   

        self.snr = np.array(snr)
        self.IntSignal = np.array(Int_signal)
        self.IntPhotonNoise =np.array(Int_photnoise) 
        self.IntBackground =np.array(Int_bgnd)
        self.IntDCurent =np.array(Int_DCurent) 
        self.IntReadNoise =np.array(Int_readnoise) 
        self.TotalNoise = np.array(Total_noise)

        return 

  















 
