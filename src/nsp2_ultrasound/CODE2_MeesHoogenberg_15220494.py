import numpy as np
import csv
from scipy.signal import hilbert

class UltrasonicExperiment:

    def __init__(self, start, stop):

        self.start = int(start)
        self.stop = int(stop)
        self.all_amps = []
        self.all_times = []
        self.all_amps_water = []
        self.all_times_water = []
        self.amplitude_envelope_all = []
        self.adjusted_signals_all = []
        self.depth_object = []
        self.amplitude_envelope_all_water = []
        self.adjusted_signals_all_water = []
        self.positions = [i for i in np.arange(self.start, self.stop + 10, 10)] #mm
        self.positions_cm = [i / 10 for i in self.positions]
        self.depths = []
        self.depths_water = []
        self.samples = 500
        self.v_water = 1500 #m/s
        self.v_al = 6320 #m/s
        self.constant_water = (((1500 / 1000) * 100) / 2) 
        self.constant_al = (((6320 / 1000) * 100) / 2) 

    def scan(self, name):

        for i in self.positions:
            
            with open('data_'+str(name)+'/'+str(i)+'.000000.txt', 'r') as text_file, open('data_water/'+str(i)+'.000000.txt', 'r') as water_text_file:

                csv_input = csv.reader(text_file, delimiter = '\t')
                csv_input_water = csv.reader(water_text_file, delimiter = '\t')

                amp = []
                time = []
                amp_water = []
                time_water = []

                for cols, cols_water in zip(csv_input, csv_input_water):

                    time.append(float(cols[0]))
                    amp.append(float(cols[1]))
                    time_water.append(float(cols_water[0]))
                    amp_water.append(float(cols_water[1]))
        
            self.all_amps.append(amp)
            self.all_times.append(time)
            self.all_amps_water.append(amp_water)
            self.all_times_water.append(time_water)

        self.depths = [i * self.constant_water for i in self.all_times[0]] 
        self.depths_water = [i * self.constant_water for i in self.all_times_water[0]]

        for i in range(len(self.all_amps)):

            mean = np.mean(self.all_amps[i])
            mean_water = np.mean(self.all_amps_water[i])

            adjusted_signal = [j - mean for j in self.all_amps[i]]
            adjusted_signal_water = [j - mean_water for j in self.all_amps_water[i]]

            analytic_signal = hilbert(adjusted_signal)
            analytic_signal_water = hilbert(adjusted_signal_water)

            amplitude_envelope = np.abs(analytic_signal)
            amplitude_envelope_water = np.abs(analytic_signal_water)

            self.adjusted_signals_all.append(adjusted_signal)
            self.adjusted_signals_all_water.append(adjusted_signal_water)

            self.amplitude_envelope_all.append(amplitude_envelope)
            self.amplitude_envelope_all_water.append(amplitude_envelope_water)