from pathlib import Path
import torch
import cv2
import pathlib
import platform

# Fix path issue for environments that have compatibility issues with pathlib
# This ensures that PosixPath is properly handled on Windows machines if it is a window's machine
if platform.system() == "Windows":
    pathlib.PosixPath = pathlib.WindowsPath

# Load the custom-trained YOLOv5 model from a local file ('best.pt')
model = torch.hub.load('yolov5', 'custom', path='C:/Users/victo/Downloads/AslRunCoding/AslRunCoding/best.pt', source='local')

# Print available classes in the model
print("Classes in the model:")
for idx, class_name in model.names.items():
    print(f'{idx}: {class_name}')
print(f'\nTotal number of classes: {len(model.names)}')

# Initialize the webcam (device index 0, which is the default webcam)
cap = cv2.VideoCapture(0)

# Start the webcam feed and process frames in real-time
while cap.isOpened():
    ret, frame = cap.read()  # Capture a frame from the webcam
    if not ret:
        break  # Exit the loop if the frame is not captured successfully

    # Convert the frame from BGR (OpenCV default) to RGB (required by YOLOv5)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform object detection using the YOLOv5 model
    results = model(rgb_frame)
    detections = results.xyxy[0]  # Extract bounding box results

    # If no objects are detected, print a message
    if len(detections) == 0:
        print("No objects detected in this frame.")
    else:
        # Loop through each detected object and draw bounding boxes
        for *box, conf, cls in detections:
            x1, y1, x2, y2 = map(int, box)  # Convert coordinates to integers

            # Retrieve the class name and remove any trailing '?' characters
            class_name = model.names[int(cls)].strip('?')

            # Construct the label with class name and confidence score
            label = f'{class_name}: {conf:.2f}'
            print(label)  # Print detection results in the console

            # Draw a bounding box around the detected object (green box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Prepare the label background for better visibility
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
            )
            cv2.rectangle(frame, (x1, y1 - text_height - 10),
                          (x1 + text_width, y1), (0, 255, 0), -1)

            # Display the label text on the image
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Show the frame with bounding boxes in a window
    cv2.imshow('YOLOv5 Custom Bounding Box Detection', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
