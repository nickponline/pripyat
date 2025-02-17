import cv2
import numpy as np
import json
import os
import sys

# Load YOLO model
net = cv2.dnn.readNet("./assets/yolov3.weights", "./assets/darknet/cfg/yolov3.cfg")

# Check for folder argument
folder = None
if len(sys.argv) > 1:
    folder = sys.argv[1]

# Initialize image list if folder is provided
images = []
if folder:
    images = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()

# Initialize webcam if no folder is provided
cap = None
if not images:
    cap = cv2.VideoCapture(0)

index = 0
while True:
    # Capture frame from webcam or load image from folder
    if images:
        image = cv2.imread(images[index])
        index = (index + 1) % len(images)
    else:
        ret, image = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

    # Get image dimensions
    (height, width) = image.shape[:2]

    # Define the neural network input
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform forward propagation
    output_layer_name = net.getUnconnectedOutLayersNames()
    output_layers = net.forward(output_layer_name)

    # Initialize list of detected people
    boxes = []
    confidences = []

    # Loop over the output layers
    for output in output_layers:
        # Loop over the detections
        for detection in output:
            # Extract the class ID and confidence of the current detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Only keep detections with a high confidence
            if class_id == 0 and confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Add the detection to lists
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))

    # Apply non-maximum suppression to remove overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # Create final list of filtered people detections
    people = []
    if len(indices) > 0:
        indices = indices.flatten()
        for i in indices:
            people.append(tuple(boxes[i]))

    # Save people count to JSON file
    with open('stats.json', 'w') as f:
        results = {"people": len(people)}
        json.dump(results, f)
        print(results)

    # Draw bounding boxes around the people
    for (x, y, w, h) in people:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the image
    cv2.imshow("Webcam" if not images else "Image", image)
    
    # Wait for 5 seconds or until 'q' is pressed
    if cv2.waitKey(5000) & 0xFF == ord('q'):
        break

# Release webcam and close windows
if cap:
    cap.release()
cv2.destroyAllWindows()