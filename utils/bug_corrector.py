import os

def correggi_file_yolo(input_path, output_path):
    # create output directory
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # list input files
    files = os.listdir(input_path)

    for file_name in files:
        input_file_path = os.path.join(input_path, file_name)

        output_file_path = os.path.join(output_path, file_name)

        # open file in read mode
        with open(input_file_path, 'r') as input_file:
            # read all the files lines
            lines = input_file.readlines()

            # open file il write mode
            with open(output_file_path, 'w') as output_file:
                # iterate on every line
                for line in lines:
                    elements = line.strip().split()

                    # file line has more than 5 elements, split
                    if len(elements) > 5:
                        # take last character
                        last_char_of_fifth_element = elements[4][-1]
                        fifth_element_no_last_char = elements[4][:-1]
                        
                        # write first part on the other line
                        output_file.write(' '.join(elements[:4])+ ' ' + fifth_element_no_last_char)
                        output_file.write('\n')

                        # write the last character of the fifth element
                        output_file.write(last_char_of_fifth_element + ' ' + ' '.join(elements[5:]))
                        output_file.write('\n')
                    else:
                        output_file.write(line)

# file utilities
input_folder = "/hpc/home/valerio.tiri/LABORS/adas_sviro/dataset_sviro/teslamodel3/labels/train_bug"
output_folder = "/hpc/home/valerio.tiri/LABORS/adas_sviro/dataset_sviro/teslamodel3/labels/train"
correggi_file_yolo(input_folder, output_folder)
print('conversion done')
