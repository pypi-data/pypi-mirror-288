import cv2
import argparse
import threading
import time

def record_webcam(file_path, duration, camera_index):
    cap = cv2.VideoCapture(0)  # Open the default camera (0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for the video file (XVID)
    out = cv2.VideoWriter(file_path, fourcc, 20.0, (640, 480))  # Output video writer

    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            break

        out.write(frame)  # Write the frame to the output video

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Record webcam stream for a specified duration.')
    parser.add_argument('--file_path', type=str, default='output.avi', help='Path to save the output video')
    parser.add_argument('--duration', type=int, default=10, help='Duration of recording in seconds')
    parser.add_argument('--camera_index', type=int, default=1, help='Index to the camera' )
    args = parser.parse_args()

    # Start recording in the background
    recording_thread = threading.Thread(target=record_webcam, args=(args.file_path, args.duration, args.camera_index))
    recording_thread.daemon = True  # Run the thread in the background
    recording_thread.start()

    print(f"Recording webcam stream for {args.duration} seconds...")

    # Wait for the recording to finish
    recording_thread.join()

    print(f"Recording completed. Video saved to {args.file_path}")

if __name__ == '__main__':
    main()
