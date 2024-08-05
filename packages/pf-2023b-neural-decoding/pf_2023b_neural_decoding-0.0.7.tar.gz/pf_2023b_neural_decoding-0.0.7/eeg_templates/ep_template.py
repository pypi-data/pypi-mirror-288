import numpy as np
import csv


class EPTemplate:
    """
    A class to construct an evoked potential (EP) template with various signal components.

    Attributes:
        entries (int): The number of entries.
        sampling_rate (int): The sampling rate in Hz.
        channel_ids (list): A list of channel IDs (strings).
        signals (dict): A dictionary where keys are channel IDs and values are lists of functions.
        noise_sigma (float): The standard deviation of the Gaussian noise (None if not added).
    """
    

    def __init__(self, time, sampling_rate, channel_ids):
        """
        Initializes the EPTemplate with the number of entries, sampling rate, and channel IDs.

        Args:
            entries (int): The number of entries.
            sampling_rate (int): The sampling rate in Hz.
            channel_ids (list of str): The list of channel IDs.
        """
        self.entries = time * sampling_rate
        self.sampling_rate = sampling_rate
        self.channel_ids = channel_ids
        self.signals = {channel_id: [] for channel_id in channel_ids}
        self.noise_power = None
        self.normalized_pulse_function = self.calculate_normalized_pulse_function()

    def calculate_normalized_pulse_function(self):
        """
        Pre-calculates a normalized pulse function which is not shifted and normalized.
        """
        A = 1
        B = 100
        C = -30
        t = np.linspace(0, 0.2, 1000)
        values = A * np.sin(B * t) * np.exp(C * t)
        max_val = np.max(values)
        return lambda t: (A * np.sin(B * t) * np.exp(C * t)) / max_val

    def add_noise(self, power):
        """
        Toggles on Gaussian noise with the specified standard deviation.

        Args:
            power (float): The power for the Gaussian noise.

        Returns:
            EPTemplate: The instance itself to allow method chaining.
        """
        self.noise_power = power
        return self


    def add_ep(self, max_peak, delay, delay_std=None, channels=None):
        """
        Adds a specific evoked potential to certain channels.

        Args:
            max_peak (float): The maximum peak of the EP.
            delay (float): The time delay until the pulse is triggered.
            delay_std (float, optional): Standard deviation of the delay distribution. If None, no variability is applied.
            channels (list of str, optional): The list of channel IDs to add this function. If None, adds to all channels.

        Returns:
            EPTemplate: The instance itself to allow method chaining.
        """
        target_channels = channels if channels else self.channel_ids

        for channel in target_channels:
            if channel not in self.channel_ids:
                raise ValueError(f"Channel {channel} not specified in constructor.")
            
            if delay_std is not None:
                # Sample a delay delta from a normal distribution
                delay_delta = np.random.normal(0, delay_std)
            else:
                # No variability in delay
                delay_delta = 0
            
            adjusted_delay = delay + delay_delta
            normalized_pulse = self.normalized_pulse_function

            def adjusted_ep_function(t, max_peak=max_peak, delay=adjusted_delay):
                delayed_t = t - delay
                return max_peak * normalized_pulse(delayed_t) if delayed_t > 0 else 0

            # Ensure the function uses the specific adjusted_delay for this channel
            self.signals[channel].append(lambda t, func=adjusted_ep_function: func(t))
        
        return self

    def add_sinusoidal(self, amplitude, frequency, phase, channels=None):
        """
        Adds a sinusoidal function to the specified channels.

        Args:
            amplitude (float): The amplitude of the sinusoidal function.
            frequency (float): The frequency of the sinusoidal function.
            phase (float): The phase shift of the sinusoidal function.
            channels (list of str, optional): The list of channel IDs to add this function. If None, adds to all channels.

        Returns:
            EPTemplate: The instance itself to allow method chaining.
        """
        def sinusoidal_function(t):
            return amplitude * np.sin(2 * np.pi * frequency * t + phase)

        target_channels = channels if channels else self.channel_ids
        for channel in target_channels:
            if channel not in self.channel_ids:
                raise ValueError(f"Channel {channel} not specified in constructor.")
            self.signals[channel].append(lambda t, func=sinusoidal_function: func(t))
        return self


    def generate_signals(self):
        """
        Generates the signal for each channel by summing all the functions added.

        Returns:
            dict: A dictionary with channel IDs as keys and generated signal arrays as values.
        """
        t = np.arange(self.entries) / self.sampling_rate
        generated_signals = {}
        for channel, functions in self.signals.items():
            signal = np.zeros_like(t)
            for func in functions:
                signal += np.array([func(ti) for ti in t], dtype=np.float64)
            if self.noise_power:
                signal += self.noise_power*np.random.normal(0, 1, size=signal.shape)
            generated_signals[channel] = signal
        return generated_signals
    

    def serialize(self, path, headers=False):
        """
        Serialize the generated signals to a TSV file.

        Args:
            path (str): The file path to save the TSV file.
        """
        signals = self.generate_signals()
        with open(path, 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            if headers: 
                writer.writerow(self.channel_ids)
            for i in range(self.entries):
                row = [f"{signals[ch][i]:.15f}" for ch in self.channel_ids]
                writer.writerow(row)