import sounddevice as sd
import numpy as np
from modules.audio_module import ClassroomAudioTracker

def main():
    tracker = ClassroomAudioTracker()
    print("Starting Mic Stream Analysis... Speak into your mic to test.")
    print("Press Ctrl + C in the terminal window to quit.")
    
    # Callback function required by sounddevice to process stream blocks on the fly
    def audio_callback(indata, frames, time_info, status):
        # Flatten the multi-channel mic input down to a single channel
        mono_data = indata[:, 0]
        energy, status_label = tracker.analyze_audio_chunk(mono_data)
        
        # Print a dynamic visual audio meter in your console
        meter = "#" * int(energy * 200)
        print(f"Energy: {energy:.4f} | {status_label:<30} {meter}")

    # Start recording stream cleanly in-memory
    with sd.InputStream(callback=audio_callback, channels=1, 
                        samplerate=tracker.sample_rate, blocksize=tracker.block_size):
        while True:
            sd.sleep(100)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAudio monitoring stream stopped cleanly.")
