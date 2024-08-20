#!/bin/env/python3 
import numpy as np

class BioSignalPluxDevice():
    def __init__(self, nADC=16, VCC=3):
        self.nADC = nADC # Resolution of the A/D converter
        self.vcc = VCC # Operating voltage
        self.nFac = 2**self.nADC # Factor, precomputed


    def __del__(self):
        pass


    def tf_EDA(self, x, clip=False):
        """Transfer function for the EDA. Implementation according to Sensor Data Sheet EMG 0309202. The signal is valid in: 

        ..math:
            0 \micro s \leq 0 \leq 25 \micro s

        Args:
            x (_type_): Input raw value
            clip (bool, optional): Enables clipping in given interval. Defaults to False.

        Returns:
            float: Returns eda (in Microsiemens)
        """
        eda_ms = np.divide(np.divide(x, self.nFac) * self.vcc , 0.12)
        
        if clip:
            eda_ms = np.clip(eda_ms, 0, 25)

        return eda_ms

    
    def tf_EEG(self, x, clip=False):
        """Transfer function for the EEG. Implementation according to Sensor Data Sheet EEG. The signal is valid in: 

        ..math:
            -37.5 \micro V \leq 0 \leq 37.5 \micro V

        Args:
            x (_type_): Input raw value
            clip (bool, optional): Enables clipping in given interval. Defaults to False.

        Returns:EEG
            float: Returns EEG (in Microvolt)
        """
        # 41_782 = G_eeg = Sensor gain 
        eeg_mv = np.divide((np.divide(x, self.nFac) -0.5 )* self.vcc , 41782) * 1e6

        if clip:
            eeg_mv = np.clip(eeg_mv, -37.5, 37.5)

        return eeg_mv


    def tf_EMG(self, x, clip=False):
        """Transfer function for the EMG. Implementation according to Sensor Data Sheet EMG. 
        
        The signal is valid in: 

        ..math:
            -1.5 mV \leq 0 \leq 1.5 mV

        Args:
            x (_type_): Input raw value
            clip (bool, optional): Enables clipping in given interval. Defaults to False.

        Returns:
            float: Returns EMG (in Millivolt)
        """
        # 1_000 = G_EMG = Sensor gain 
        emg_mv = (np.divide(x, self.nFac) -0.5 )* self.vcc 

        if clip:
            emg_mv = np.clip(emg_mv, -1.5, 1.5)

        return emg_mv


    def tf_ECG(self, x, clip=False):
        """Transfer function for the ECG. Implementation according to Sensor Data Sheet ECG 10082020. 
        
        The signal is valid in: 

        ..math:
            -*1.47 mV \leq 0 \leq 1.47 mV

        Args:
            x (_type_): Input raw value
            clip (bool, optional): Enables clipping in given interval. Defaults to False.

        Returns:
            float: Returns ECG (in Millivolt)
        """
        # 1_019 = Sensor gain from data sheet
        ecg_mv = np.divide((np.divide(x, self.nFac) -0.5 )* self.vcc , 1_019) * 1_000

        if clip:
            ecg_mv = np.clip(ecg_mv, -1.47, 1.47)

        return ecg_mv
