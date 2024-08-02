import numpy as np

class EPTemplate: 

    def __init__(self, entries=125, sampling_freq=250, freq_ary=np.zeros(16), amp_ary=np.zeros(16), phase_ary=np.zeros(16)): 
        """
        Args:
            ticks_in_samples (int): Number of time stamps in sample units (seconds * sampling rate).
            sampling_freq (int): Sampling frequency in Hz. It determines the time separation between ticks
            freq_ary (np.ndarray): Array of frequencies.
            amp_ary (np.ndarray): Array of amplitudes.
            phase_ary (np.ndarray): Array of phases in radians
        """
        self.entries = entries 
        self.sampling_freq = sampling_freq
        self.freq_ary = freq_ary
        self.amp_ary = amp_ary 
        self.phase_ary = phase_ary 

        # Noise functions 
        self.additive_noise_fun = lambda : 0
        self.additive_fun_generators = [] 



    def create_template(self, output_path): 
        """
        Args:
            output_path (str): Path to the output file
        """
                
        t = np.linspace(0, (self.entries - 1) , self.entries, endpoint=False) / self.sampling_freq
        sine_wave_data = np.zeros((self.entries, len(self.freq_ary)))
    
        
        for i in range(len(self.freq_ary)):
            current_sine_wave = self.amp_ary[i] * np.sin(2 * np.pi * self.freq_ary[i] * t + self.phase_ary[i])

            additive_funs_for_channel = [afg() for afg in self.additive_fun_generators]

            for af in additive_funs_for_channel: 
                current_sine_wave += np.array([af(x) for x in t])

            additive_noise = np.array([self.additive_noise_fun() for _ in range(self.entries)])
            sine_wave_data[:, i] = current_sine_wave + additive_noise
    
        sine_wave_data_with_stamp = np.column_stack((np.arange(1, len(t)+1), sine_wave_data))
        np.savetxt(output_path, sine_wave_data_with_stamp, delimiter='\t', comments='', fmt='%.4f')


    def set_additive_noise(self, additive_noise_fun): 
        """
        This method sets the additive noise for the sinusoidal function.

        Args:
            additive_noise_fun (function _ -> float): 
                A function that generates random samples representing the noise to be added to the sinusoidal function. 
        """
        self.additive_noise_fun = additive_noise_fun

    
    def add_additive_fun_generator(self, additive_fun_generator): 
        """
        This method allows to add another function that is added to the main sinusoidal wave 
        Args:
            additive_noise_fun (function float -> float): 
                A function that generates random samples representing the noise to be added to the sinusoidal function. 
        """
        self.additive_fun_generators.append(additive_fun_generator)

