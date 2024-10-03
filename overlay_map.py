import cv2
import numpy as np

# Load the Gazebo world image (ground truth map)
gazebo_map_path = "/home/student/map.png"  # Updated path to the Gazebo map image
gazebo_map = cv2.imread(gazebo_map_path, cv2.IMREAD_COLOR)

# Load the generated SLAM map
slam_map_path = "/home/student/ros2_ws/src/sprint3/maps/my_map.pgm"  # Path to your SLAM map
slam_map = cv2.imread(slam_map_path, cv2.IMREAD_COLOR)

# Rotate the SLAM map 90 degrees clockwise
(h, w) = slam_map.shape[:2]
center = (w // 2, h // 2)
rotation_matrix = cv2.getRotationMatrix2D(center, 0, 1.0)
rotated_slam_map = cv2.warpAffine(slam_map, rotation_matrix, (w, h))

# Scaling factor to resize the SLAM map
scaling_factor = 1  # Increased to enlarge the SLAM map

# Calculate the new dimensions for the SLAM map
new_width = int(gazebo_map.shape[1] * scaling_factor)
new_height = int(gazebo_map.shape[0] * scaling_factor)

# Resize the rotated SLAM map using the scaling factor
resized_slam_map = cv2.resize(rotated_slam_map, (new_width, new_height))

# Find the top-left corner to place the resized SLAM map onto the Gazebo map
x_offset = (gazebo_map.shape[1] - new_width) // 2
y_offset = (gazebo_map.shape[0] - new_height) // 2

# Adjust offsets if they are negative (meaning the resized map is too large)
if x_offset < 0:
    x_offset = 0
    new_width = gazebo_map.shape[1]

if y_offset < 0:
    y_offset = 0
    new_height = gazebo_map.shape[0]

# Resize the SLAM map again if necessary to fit into the canvas
resized_slam_map = cv2.resize(rotated_slam_map, (new_width, new_height))

# Create a blank canvas with the same size as the Gazebo map
canvas = np.zeros_like(gazebo_map)

# Place the resized SLAM map onto the canvas
canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_slam_map

# Overlay the SLAM map onto the Gazebo map with some transparency
overlay = cv2.addWeighted(gazebo_map, 0.7, canvas, 0.3, 0)  # Adjust weights for transparency

# Show the overlaid image
cv2.imshow('Overlay', overlay)
cv2.waitKey(0)  # Press any key to close the window
cv2.destroyAllWindows()

# Save the overlaid image
output_path = "/home/student/ros2_ws/src/sprint3/maps/overlay.png"  # Output path
cv2.imwrite(output_path, overlay)
