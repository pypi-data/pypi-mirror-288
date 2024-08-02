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
    

    def __init__(self, entries, sampling_rate, channel_ids):
        """
        Initializes the EPTemplate with the number of entries, sampling rate, and channel IDs.

        Args:
            entries (int): The number of entries.
            sampling_rate (int): The sampling rate in Hz.
            channel_ids (list of str): The list of channel IDs.
        """
        self.entries = entries
        self.sampling_rate = sampling_rate
        self.channel_ids = channel_ids
        self.signals = {channel_id: [] for channel_id in channel_ids}
        self.noise_sigma = None


    def add_noise(self, sigma):
        """
        Toggles on Gaussian noise with the specified standard deviation.

        Args:
            sigma (float): The standard deviation for the Gaussian noise.

        Returns:
            EPTemplate: The instance itself to allow method chaining.
        """
        self.noise_sigma = sigma
        return self


    def add_ep(self, A, B, C, delay, delay_std=None, channels=None):
        """
        Adds a specific evoked potential to certain channels.

        Args:
            A (float): The amplitude of the EP.
            B (float): The frequency factor of the EP.
            C (float): The damping factor of the EP.
            delay (float): The time delay until the pulse is triggered.
            delay_std (float, optional): The standard deviation of the delay (default is None).
            channels (list of str, optional): The list of channel IDs to add this function. If None, adds to all channels.

        Returns:
            EPTemplate: The instance itself to allow method chaining.
        """
        # Generate a random delay shift if delay_std is provided
        if delay_std:
            delay_shift = np.random.normal(0, delay_std)
            delay += delay_shift

        def ep_function(t):
            delayed_t = t - delay
            return A * np.sin(B * delayed_t) * np.exp(C * delayed_t) if delayed_t > 0 else 0

        target_channels = channels if channels else self.channel_ids
        for channel in target_channels:
            if channel not in self.channel_ids:
                raise ValueError(f"Channel {channel} not specified in constructor.")
            self.signals[channel].append(lambda t, func=ep_function: func(t))
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
                signal += np.vectorize(func)(t)
            if self.noise_sigma:
                signal += np.random.normal(0, self.noise_sigma, size=signal.shape)
            generated_signals[channel] = signal
        return generated_signals
    

    def serialize(self, path):
        """
        Serialize the generated signals to a TSV file.

        Args:
            path (str): The file path to save the TSV file.
        """
        signals = self.generate_signals()
        with open(path, 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            writer.writerow(self.channel_ids)
            for i in range(self.entries):
                row = [f"{signals[ch][i]:.15f}" for ch in self.channel_ids]
                writer.writerow(row)


ep_template = EPTemplate(
    entries=1000,
    sampling_rate=1000,
    channel_ids=["ch1", "ch2"]
)

# Add Gaussian noise with a standard deviation of 0.1
ep_template.add_noise(sigma=0.1)

# Add an evoked potential to channel "ch1"
ep_template.add_ep(
    A=1.0,
    B=20.0,
    C=-5.0,
    delay=0.1,
    delay_std=0.02,
    channels=["ch1"]
)

# Add a sinusoidal function to channel "ch2"
ep_template.add_sinusoidal(
    amplitude=0.5,
    frequency=5.0,
    phase=0,
    channels=["ch2"]
)

# Generate the signals
signals = ep_template.generate_signals()

# Print the generated signals for verification
print("Generated Signals:")
for channel, signal in signals.items():
    print(f"{channel}: {signal[:10]}")  # Print first 10 samples for each channel

# Serialize the signals to a TSV file
output_path = "generated_signals_2.tsv"
ep_template.serialize(path=output_path)

print(f"Signals serialized to {output_path}")