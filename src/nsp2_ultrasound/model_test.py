
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
        self.times_object = []
        self.times_water = []
        self.amplitude_envelope_all_water = []
        self.adjusted_signals_all_water = []
        self.indexes_object = []
        self.indexes_water = []
        self.ranges = [i for i in np.arange(self.start, self.stop + 10, 10)] #mm
        self.samples = 500
        self.v_water = 1500 #m/s
        self.v_al = 6320 #m/s
        self.constant_water = (((1500 / 1000) * 100) / 2) 
        self.constant_al = (((6320 / 1000) * 100) / 2) 
        self.t_end_object = []
        self.t_start_object = []

    def scan(self, name):

        for i in self.ranges:
            
            with open('data_'+str(name)+'/'+str(i)+'.000000.txt', 'r') as text_file:

                csv_input = csv.reader(text_file, delimiter = '\t')
                
                amp = []
                time = []

                for cols in csv_input:

                    time.append(float(cols[0]))
                    amp.append(float(cols[1]))

            self.all_amps.append(amp)
            self.all_times.append(time)

        for i in range(len(self.all_amps)):

            value = np.mean(self.all_amps[i])
            adjusted_signal = [j - value for j in self.all_amps[i]]
            analytic_signal = hilbert(adjusted_signal)
            amplitude_envelope = np.abs(analytic_signal)
            self.adjusted_signals_all.append(adjusted_signal)
            self.amplitude_envelope_all.append(amplitude_envelope)

    def scan_water(self):

        for i in self.ranges:

            with open('data_water/'+str(i)+'.000000.txt', 'r') as water_text_file:

                csv_input = csv.reader(water_text_file, delimiter = '\t')
                
                amp_water = []
                time_water = []

                for cols in csv_input:

                    time_water.append(float(cols[0]))
                    amp_water.append(float(cols[1]))

            self.all_amps_water.append(amp_water)
            self.all_times_water.append(time_water)
        
        for i in range(len(self.all_amps_water)):

            value = np.mean(self.all_amps_water[i])
            adjusted_signal = [j - value for j in self.all_amps_water[i]]
            analytic_signal = hilbert(adjusted_signal)
            amplitude_envelope = np.abs(analytic_signal)
            self.adjusted_signals_all_water.append(adjusted_signal)
            self.amplitude_envelope_all_water.append(amplitude_envelope)

    def depth(self):
        
        for i in range(len(self.amplitude_envelope_all)):

            time_object = []
            time_water = []
            index_object = []
            index_water = []

            for j, k in zip(self.amplitude_envelope_all[i], self.amplitude_envelope_all_water[i]):

                if j > 5.0:

                    time_object.append(self.all_times[i][list(self.amplitude_envelope_all[i]).index(j)])
                    index_object.append(list(self.amplitude_envelope_all[i]).index(j))
                
                if k > 5.0:

                    time_water.append(self.all_times_water[i][list(self.amplitude_envelope_all_water[i]).index(k)])
                    index_water.append(list(self.amplitude_envelope_all_water[i]).index(k))

            self.times_object.append(time_object)
            self.indexes_object.append(index_object)
            self.times_water.append(time_water)
            self.indexes_water.append(index_water)

        for i in range(len(self.times_object)):
            
            if len(self.times_object[i]) == 0:
                
                pass
            
            else:

                t_start_signal = min(self.times_object[i])

                t_end_signal = max(self.times_object[i])

                self.t_start_object.append(t_start_signal)
                self.t_end_object.append(t_end_signal)
                d_object = (t_end_signal - t_start_signal) * self.constant_al
             
            if len(self.times_water[i]) == 0:

                pass

            else:

                t_start_water = min(self.times_water[i])

                t_end_water = max(self.times_water[i])

                d_water = (t_end_water - t_start_water) * self.constant_water

        depth = ((((t_start_signal) / 1000) * 1500) * 100) / 2

        print(d_water - d_object)
        print(len(self.indexes_object), len(self.indexes_water))
        print(f"start reflected signal = {t_start_signal} ms\nend reflected signal = {t_end_signal} ms")
        print(f"echo pulse width calculated = {t_start_signal} ms")
        print(f"echo pulse width actual = {(75 / 1000) * 1.5} ms")
        print(f"depth of object calculated = {depth} cm")