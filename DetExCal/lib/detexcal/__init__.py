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
 
        snr = []
        Int_signal =[] 
        Int_photnoise =[] 
        Int_bgnd =[] 
        Int_DCurent =[] 
        Int_readnoise =[] 
        Total_noise = []

        """       
        RN = np.sqrt((self.readnoise**2)*self.npix)
 
        for i in np.atleast_1d(np.array(self.time)):
            SI  = self.signal*self.gain*i #*0.29#one pixel, collects about 29% of the total light
            SG  = np.sqrt(SI)
            BG  = np.sqrt(self.bgnd*self.npix*i)
            DC  = np.sqrt(self.DCurent*self.npix*i)
            TOT = np.sqrt( SG**2 + BG**2 + DC**2 + RN**2 )


            snr.append(SI / TOT)   

            Int_signal.append(SI)
            Int_photnoise.append(SG)  
            Int_bgnd.append(BG)
            Int_DCurent.append(DC)
            Int_readnoise.append(RN)
            Total_noise.append(TOT)
            
        self.snr = np.array(snr)
        self.IntSignal = np.array(Int_signal)
        self.IntPhotonNoise =np.array(Int_photnoise) 
        self.IntBackground =np.array(Int_bgnd)
        self.IntDCurent =np.array(Int_DCurent) 
        self.IntReadNoise =np.array(Int_readnoise) 
        self.TotalNoise = np.array(Total_noise)
        """

        RN = (self.readnoise**2)

        for i in np.atleast_1d(np.array(self.time)):
            SI  = self.signal*self.gain*i *0.027#one pixel, collects about 29% of the total light
            SG  = np.sqrt(SI)
            BG  = self.bgnd*i*0.027
            DC  = self.DCurent*i
            TOT = np.sqrt( SI + (BG + DC + RN)*self.npix)


            snr.append(SI / TOT)   
    
            Int_signal.append(SI)
            Int_photnoise.append(SG)  
            Int_bgnd.append(BG)
            Int_DCurent.append(DC)
            Int_readnoise.append(RN)
            Total_noise.append(TOT)
            
        self.snr = np.array(snr)
        self.IntSignal = np.array(Int_signal)
        self.IntPhotonNoise =np.array(Int_photnoise) 
        self.IntBackground =np.array(Int_bgnd)
        self.IntDCurent =np.array(Int_DCurent) 
        self.IntReadNoise =np.array(Int_readnoise) 
        self.TotalNoise = np.array(Total_noise)

        return 


    def ccd_SNR_vs_mag(self):
 
        RN = self.readnoise**2
        snr = []
        Int_signal =[] 
        Int_photnoise =[] 
        Int_bgnd =[] 
        Int_DCurent =[] 
        Int_readnoise =[] 
        Total_noise = []

        BG = self.bgnd*self.time
        DC = self.DCurent*self.time

        for mag in np.atleast_1d(np.array(self.mag)):
            flux = self.magnitude_to_flux(mag) #airmass?
            signal  = flux*self.aperture*(self.throughput)*(self.bandwidth)*(self.quant_eff)

            SI = signal*self.gain*self.time
            SG  = np.sqrt(SI)
            TOT = np.sqrt( SI + (BG + DC + RN)*self.npix)
            
            snr.append(SI / TOT)   

            Int_signal.append(SI)
            Int_photnoise.append(SG)  
            Int_bgnd.append(BG)
            Int_DCurent.append(DC)
            Int_readnoise.append(RN)
            Total_noise.append(TOT)

        self.snr = np.array(snr)
        self.IntSignal = np.array(Int_signal)
        self.IntPhotonNoise =np.array(Int_photnoise) 
        self.IntBackground =np.array(Int_bgnd)
        self.IntDCurent =np.array(Int_DCurent) 
        self.IntReadNoise =np.array(Int_readnoise) 
        self.TotalNoise = np.array(Total_noise)

        return 

  















 
