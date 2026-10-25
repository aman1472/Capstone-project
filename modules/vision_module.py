import cv2
import time
import numpy as np

class ClassroomVisionTracker:
    def __init__(self, frame_skip=3, presence_threshold_seconds=5):
        """
        Lightweight Vision Module with fixed tracking state logic.
        """
        self.frame_skip = frame_skip
        self.frame_count = 0
        
        # Track format: { student_id: [first_seen_timestamp, last_seen_timestamp] }
        self.tracked_students = {} 
        self.presence_threshold = presence_threshold_seconds

    def process_frame(self, frame):
        """Processes a single camera frame using pixel changes to detect human movement/presence."""
        self.frame_count += 1
        current_time = time.time()
        
        if self.frame_count % self.frame_skip != 0:
            return frame, self._count_confirmed(current_time)

        # Convert to gray to detect presence/movement features safely without external XML templates
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Fallback tracking simulation using contour blocks
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        idx = 0
        for contour in contours:
            if cv2.contourArea(contour) > 5000:  # Only track large objects (like a person's head/body)
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                student_id = f"Student_{idx + 1}"
                if student_id not in self.tracked_students:
                    # Initialize with [first_seen, last_seen]
                    self.tracked_students[student_id] = [current_time, current_time]
                else:
                    # FIX: Keep the original first_seen time, only update the last_seen time!
                    self.tracked_students[student_id][1] = current_time
                idx += 1
                if idx >= 5: # Limit mock cluster tracking count
                    break

        confirmed_present = self._draw_overlays(frame, current_time)
        return frame, confirmed_present

    def _count_confirmed(self, current_time):
        confirmed = 0
        for timestamps in self.tracked_students.values():
            first_seen, last_seen = timestamps
            if (last_seen - first_seen) >= self.presence_threshold:
                confirmed += 1
        return confirmed

    def _draw_overlays(self, frame, current_time):
        confirmed_present = 0
        for student, timestamps in list(self.tracked_students.items()):
            first_seen, last_seen = timestamps
            if (last_seen - first_seen) >= self.presence_threshold:
                confirmed_present += 1
                cv2.putText(frame, f"{student}: Verified Present", (10, 30 + (confirmed_present * 25)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return confirmed_present
