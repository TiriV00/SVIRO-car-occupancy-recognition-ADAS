import os

def convert_to_yolo_format(input_folder, output_folder):
    # Create output directory
    os.makedirs(output_folder, exist_ok=True)

    # File elaboration
    for filename in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, f"{filename}")

        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
            for line in input_file:
                parts = line.strip().split(',')
                class_name = parts[0]
                x1, y1, x2, y2 = map(int, parts[1:])
                normalized_x_center = (x1 + x2) / (2 * 960)
                normalized_y_center = (y1 + y2) / (2 * 640)
                normalized_width = (x2 - x1) / 960
                normalized_height = (y2 - y1) / 640
                output_line = f"{class_name} {normalized_x_center} {normalized_y_center} {normalized_width} {normalized_height}\n"
                output_file.write(output_line)

# function utilities
input_file_path = '/hpc/home/valerio.tiri/LABORS/adas_sviro/dataset_sviro/teslamodel3/labels/train_sviro/'
output_file_path = '/hpc/home/valerio.tiri/LABORS/adas_sviro/dataset_sviro/teslamodel3/labels/train/'
convert_to_yolo_format(input_file_path, output_file_path)
print('conversion done')
