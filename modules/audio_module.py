import numpy as np
import sounddevice as sd
import time

class ClassroomAudioTracker:
    def __init__(self, sample_rate=16000, block_duration_ms=500):
        """
        Lightweight Offline Audio Module for Classroom Noise and Speech Activity Tracking.
        """
        self.sample_rate = sample_rate
        # Calculate how many audio samples are in our time block (e.g., 500ms chunks)
        self.block_size = int(sample_rate * (block_duration_ms / 1000.0))
        
        # Calibration baseline for background classroom noise
        self.noise_floor = 0.01 
        self.speech_threshold = 0.05

    def analyze_audio_chunk(self, audio_data):
        """
        Analyzes a chunk of audio to extract volume energy and classify activity.
        Runs entirely in-memory without saving audio files to disk for strict privacy.
        """
        if len(audio_data) == 0:
            return 0.0, "Silent"
            
        # Calculate Root Mean Square (RMS) to determine the absolute volume energy
        rms_energy = np.sqrt(np.mean(np.square(audio_data)))
        
        # Rule-based classification engine
        if rms_energy < self.noise_floor:
            activity_status = "Silent Classroom"
        elif rms_energy < self.speech_threshold:
            activity_status = "Ambient / Lecture Noise"
        else:
            activity_status = "Active Speech / Discussion Peak"
            
        return float(rms_energy), activity_status
