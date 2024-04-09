import cv2
import csv

def pixel_value_to_temperature(pixel_value, calibration_data):
    temperature = (pixel_value - calibration_data['offset']) / calibration_data['scale']
    return temperature

def read_thermal_image(image_path, output_csv, calibration_data):
    # Load the thermal image using OpenCV
    thermal_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    if thermal_image is None:
        print("Failed to load the image.")
        return
    
    # Create or open the CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header row
        csv_writer.writerow(['Row', 'Column', 'Temperature (Celsius)'])
        
        # Iterate through each pixel and save its temperature in the CSV
        for row_idx, row in enumerate(thermal_image):
            for col_idx, pixel_value in enumerate(row):
                temperature = pixel_value_to_temperature(pixel_value, calibration_data)
                csv_writer.writerow([row_idx, col_idx, temperature])

if __name__ == "__main__":
    image_path = "halo.jpg"
    output_csv = "output_temperature_data.csv"
    
    # Replace with your calibration data
    calibration_data = {
        'offset': 100,   # Replace with the offset value from your calibration data
        'scale': 0.1     # Replace with the scale value from your calibration data
    }
    
    read_thermal_image(image_path, output_csv, calibration_data)

