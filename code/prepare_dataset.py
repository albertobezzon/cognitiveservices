import csv
import os
import shutil


def read_csv():
    metadata = {}

    with open('HAM10000_metadata.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                metadata.update({row[1]: row[2]})
    return metadata


def preparing_directory(metadata):
    values = list(set([x for x in metadata.values()]))
    for name in values:
        if not os.path.exists(name):
            os.mkdir(name)


def subdivide_image(metadata):
    dir_name = ['HAM10000_images_part_1', 'HAM10000_images_part_2']
    for directory in dir_name:
        for file_ in os.listdir(directory):
            filename = os.path.splitext(file_)[0]
            class_ = metadata[filename]
            shutil.copyfile(directory+"/"+file_, class_+"/"+file_)


if __name__ == "__main__":
    metadata = read_csv()
    preparing_directory(metadata)
    subdivide_image(metadata)
    print("DONE!")
