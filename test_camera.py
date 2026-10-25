import cv2
import sys
from modules.vision_module import ClassroomVisionTracker

def main():
    tracker = ClassroomVisionTracker(frame_skip=3, presence_threshold_seconds=5)
    
    # Try opening the default webcam
    cap = cv2.VideoCapture(0)
    
    # Alternative fallback if index 0 drops out instantly
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)

    print("Starting Video Feed... Press 'q' inside the window to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("\n[Warning] Webcam connection lost or frame dropped.")
            print("Ensure no other application (Zoom, Teams, etc.) is using your webcam.")
            break
            
        processed_frame, present_count = tracker.process_frame(frame)
        
        cv2.putText(processed_frame, f"Total Present: {present_count}", (10, 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        
        cv2.imshow('Classroom Intelligence System - Vision Test', processed_frame)
        
        # Adding a 30ms window delay to keep the window open properly
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("Camera stream closed cleanly.")

if __name__ == "__main__":
    main()
