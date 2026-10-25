import cv2
import sounddevice as sd
import numpy as np
import threading
import time
from modules.vision_module import ClassroomVisionTracker
from modules.audio_module import ClassroomAudioTracker
from modules.agent_engine import ClassroomMultimodalAgent

# Global state sharing across separate threads
current_audio_energy = 0.0
current_audio_status = "Silent Classroom"

def main():
    global current_audio_energy, current_audio_status
    
    # Initialize all modules
    vision_tracker = ClassroomVisionTracker(frame_skip=3, presence_threshold_seconds=5)
    audio_tracker = ClassroomAudioTracker()
    agent = ClassroomMultimodalAgent()
    
    # Background audio worker function
    def mic_stream_loop():
        global current_audio_energy, current_audio_status
        def callback(indata, frames, time_info, status):
            global current_audio_energy, current_audio_status
            mono_data = indata[:, 0]
            current_audio_energy, current_audio_status = audio_tracker.analyze_audio_chunk(mono_data)
            
        with sd.InputStream(callback=callback, channels=1, 
                            samplerate=audio_tracker.sample_rate, blocksize=audio_tracker.block_size):
            while True:
                sd.sleep(100)

    # Launch Audio Processing on a separate thread to prevent webcam lag
    audio_thread = threading.Thread(target=mic_stream_loop, daemon=True)
    audio_thread.start()

    # Open Camera Stream with Warmup Retry Logic
    print("\nInitializing camera hardware...")
    cap = cv2.VideoCapture(0)
    time.sleep(1.5)  # Give Windows plenty of time to clear old hardware locks
    
    if not cap.isOpened():
        print("Camera index 0 failed. Trying index 1...")
        cap = cv2.VideoCapture(1)
        time.sleep(1.5)

    if not cap.isOpened():
        print("\n[ERROR] System could not open any webcam device.")
        print("Please check your camera privacy settings or close other camera apps.")
        return

    print("\n=======================================================")
    print("Launching Multimodal Agent Engine System Application...")
    print("Press 'q' inside the video canvas window to exit safely.")
    print("=======================================================\n")

    failed_frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            failed_frame_count += 1
            # If it fails 10 times consecutively, the hardware is frozen or locked by another app
            if failed_frame_count > 10:
                print("\n[ERROR] Camera hardware is not returning data frames.")
                print("Fix: Close any background apps using your camera, or restart VS Code to clear the port.")
                break
            time.sleep(0.1)
            continue
        
        # Reset failure counter on a successful frame read
        failed_frame_count = 0
            
        # 1. Process Visuals
        processed_frame, present_count = vision_tracker.process_frame(frame)
        
        # 2. Fuse Signals via the Agent
        engagement_score, dynamic_label = agent.calculate_engagement(
            present_count, current_audio_energy, current_audio_status
        )
        
        # 3. Draw Unified On-Screen Diagnostics Hud overlay
        cv2.rectangle(processed_frame, (5, 5), (420, 115), (0, 0, 0), -1) # Dark backdrop card
        cv2.putText(processed_frame, f"Attendance Count: {present_count}", (15, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(processed_frame, f"Audio Context: {current_audio_status}", (15, 55), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        cv2.putText(processed_frame, f"Engagement Score: {engagement_score}%", (15, 85), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(processed_frame, f"Status: {dynamic_label}", (15, 105), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow('Multimodal Classroom Intelligence Agent', processed_frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("System closed cleanly.")

if __name__ == "__main__":
    main()
