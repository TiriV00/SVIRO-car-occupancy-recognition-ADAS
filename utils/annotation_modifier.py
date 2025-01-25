import os

def correggi_annotazioni_cartella(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # parse all the files
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            correggi_annotazioni(file_path, output_path)

def correggi_annotazioni(file_path, output_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    index_to_remove = []
    index_shift = 0

    for i, line in enumerate(lines):
        elements = line.strip().split()

        # check for classes 1 or 2
        if elements[0] in ['1', '2']:
            adult_present = False
            adult_index = None

            # parse all the lines
            for j in range(0, len(lines)):
                other_elements = lines[j].strip().split()

                # check adult in bbox
                if other_elements[0] == '3' and is_inside(elements, other_elements):
                    adult_present = True
                    adult_index = j
                    break

            # adult present, delete line
            if adult_present:
                index_to_remove.append(adult_index)
            else:
                # change calsses to 5 or 6
                elements[0] = '5' if elements[0] == '1' else '6'
                lines[i - index_shift] = ' '.join(elements)

                # adult present, more shift
                if adult_present:
                    index_shift += 1

    # delete adult line
    for index in sorted(index_to_remove, reverse=True):
        del lines[index]

    # write modifications in the new file
    with open(output_path, 'w') as output_file:
        output_file.writelines(lines)

def is_inside(box1, box2):
    
    # Box1: [x1, y1, w1, h1], Box2: [x2, y2, w2, h2]
    x1, y1, w1, h1 = map(float, box1[1:])
    x2, y2, w2, h2 = map(float, box2[1:])

    # vertex calculation
    x1_min, y1_min, x1_max, y1_max = x1 - w1/2, y1 - h1/2, x1 + w1/2, y1 + h1/2
    x2_min, y2_min, x2_max, y2_max = x2 - w2/2, y2 - h2/2, x2 + w2/2, y2 + h2/2

    # check the center
    center_inside_x = x1_min <= x2 <= x1_max
    center_inside_y = y1_min <= y2 <= y1_max

    # check the area
    area_condition = (w2 * h2) < (w1 * h1)

    return center_inside_x and center_inside_y and area_condition

# file utlities
correggi_annotazioni_cartella('/hpc/home/valerio.tiri/LABORS/adas_sviro/dataset_sviro/teslamodel3/labels/train_old/', '/hpc/home/valerio.tiri/LABORS/adas_sviro/dataset_sviro/teslamodel3/labels/train/')
print("conversion done")