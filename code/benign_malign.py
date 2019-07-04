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


def create_benign(metadata):
    if not os.path.exists('benign'):
        os.mkdir('benign')
    if not os.path.exists('malign'):
        os.mkdir('malign')
    dir_name = 'Images'
    count_nv = 0
    count_bkl = 0
    for file_ in os.listdir(dir_name):
        filename = os.path.splitext(file_)[0]
        class_ = metadata[filename]
        if class_ == 'akiec' or class_ == 'vasc' or class_ == 'df':
            shutil.copyfile(dir_name + '/' + file_, 'benign/'+file_)
        if class_ == 'bkl':
            # Number of bkl 1099
            shutil.copyfile(dir_name + '/' + file_, 'benign/'+file_)
        if class_ == 'nv' and count_nv < 2230:
            count_nv += 1
            shutil.copyfile(dir_name + '/' + file_, 'benign/'+file_)
        if class_ == 'mel' or class_ == 'bcc':
            shutil.copyfile(dir_name + '/' + file_, 'malign/'+file_)
    path, dirs, files = next(os.walk("benign/"))
    file_count = len(files)
    print("Number of images inside benign: " + file_count)
    path, dirs, files = next(os.walk("malign/"))
    file_count = len(files)
    print("Number of images inside malign: " + file_count)


def create_metadata():
    metadata = {}
    for file_ in os.listdir('benign'):
        filename = os.path.splitext(file_)[0]
        metadata[filename] = 'ben'
    for file_ in os.listdir('malign'):
        filename = os.path.splitext(file_)[0]
        metadata[filename] = 'mal'
    with open('BM_metadata.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['image_id', 'dx'])
        for key, value in metadata.items():
            writer.writerow([key+".jpg", value])


def aggregate_images():
    if not os.path.exists('allImages'):
        print("Creating directory allImages")
        os.mkdir('allImages')
        print("Done")
    else:
        print("allImages is already present, removing all images inside it")
        for file_ in os.listdir('allImages'):
            os.remove(file_)
        print("Done")
    directory_list = ['benign', 'malign']
    print("Copying images in benign and malign inside allImages")
    for directory in directory_list:
        for file_ in os.listdir(directory):
            shutil.copyfile(directory + '/' + file_, 'allImages/' + file_)
    print("Done")
    

if __name__ == "__main__":
    #metadata = read_csv()
    #create_benign(metadata)
    #create_metadata()
    aggregate_images()