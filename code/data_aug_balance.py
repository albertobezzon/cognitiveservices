import csv
import os
import shutil
import numpy as np
import pandas as pd
from glob import glob
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical


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
    dir_name = ['training_set']
    for directory in dir_name:
        for file_ in os.listdir(directory):
            filename = os.path.splitext(file_)[0]
            class_ = metadata[filename]
            shutil.copyfile(directory+"/"+file_, class_+"/"+file_)


def train_split():
    base_skin_dir = 'Images'
    imageid_path_dict = {os.path.splitext(os.path.basename(x))[0]: x for x in glob(os.path.join(base_skin_dir, '*.jpg'))}

    lesion_type_dict = {
        'nv': 'Melanocytic nevi',
        'mel': 'Melanoma',
        'bkl': 'Benign keratosis-like lesions',
        'bcc': 'Basal cell carcinoma',
        'akiec': 'Actinic keratoses',
        'vasc': 'Vascular lesions',
        'df': 'Dermatofibroma'
    }
    skin_df = pd.read_csv('HAM10000_metadata.csv')

    skin_df['path'] = skin_df['image_id'].map(imageid_path_dict.get)
    skin_df['cell_type'] = skin_df['dx'].map(lesion_type_dict.get)
    skin_df['cell_type_idx'] = pd.Categorical(skin_df['cell_type']).codes

    x_train_o, x_test_o, y_train_o, y_test_o = train_test_split(skin_df['path'], skin_df['cell_type_idx'], test_size=0.20, random_state=1234)
    
    if not os.path.exists('training_set'):
        print("Creating directory training_set")
        os.mkdir('training_set')
        print("Done")
    else:
        print("training_set is already present, removing all images inside it")
        for file_ in os.listdir('training_set'):
            os.remove(file_)
        print("Done")
    
    for element in x_train_o:
        # Get filename
        image = element[7:-4]
        shutil.copyfile('Images/' + image + '.jpg', 'training_set/' + image + '.jpg')


def data_augmentation():
    class_list = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'vasc']
    for item in class_list:
        aug_dir = 'aug_dir'
        os.mkdir(aug_dir)
        # create a dir within the base dir to store images of the same class
        img_dir = os.path.join(aug_dir, 'img_dir')
        os.mkdir(img_dir)

        # Choose a class
        img_class = item

        # list all images in that directory
        img_list = os.listdir(img_class)

        # Copy images from the class train dir to the img_dir e.g. class 'mel'
        for fname in img_list:
            # source path to image
            src = os.path.join(img_class, fname)
            # destination path to image
            dst = os.path.join(img_dir, fname)
            # copy the image from the source to the destination
            shutil.copyfile(src, dst)


        # point to a dir containing the images and not to the images themselves
        path = aug_dir
        save_path = img_class
        datagen = ImageDataGenerator(rotation_range=45, zoom_range=0.2, width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True, vertical_flip=True, fill_mode='nearest')
        batch_size = 32
        aug_datagen = datagen.flow_from_directory(path, save_to_dir=save_path, save_format='jpg', target_size=(450,600), batch_size=batch_size)
        num_aug_images_wanted = 1000 # 6000
        num_files = len(os.listdir(img_dir))
        num_batches = int(np.ceil((num_aug_images_wanted-num_files)/batch_size))

        # run the generator and create about 6000 augmented images
        for i in range(0,num_batches):

            imgs, labels = next(aug_datagen)
            
        # delete temporary directory with the raw image files
        shutil.rmtree('aug_dir')


def count_element_dir():
    directory_list = ['nv', 'mel', 'bkl', 'bcc', 'akiec', 'vasc', 'df']
    for dir_ in directory_list:
        print(dir_ + " : " + str(len(os.listdir(dir_))))


def create_metadata():
    metadata = {}
    class_list = ['nv', 'mel', 'bkl', 'bcc', 'akiec', 'vasc', 'df']
    for class_ in class_list:
        for file_ in os.listdir(class_):
            filename_tuple = os.path.splitext(file_)
            filename = filename_tuple[0] + filename_tuple[1]
            metadata[filename] = class_

    with open('DA_metadata.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['image_id', 'dx'])
        for key, value in metadata.items():
            writer.writerow([key, value])


def aggregate_images():
    if not os.path.exists('all_images'):
        print("Creating directory all_images")
        os.mkdir('allImages')
        print("Done")
    else:
        print("all_images is already present, removing all images inside it")
        for file_ in os.listdir('all_images'):
            print(file_)
            os.remove('all_images/' + file_)
        print("Done")
    directory_list = ['nv', 'mel', 'bkl', 'bcc', 'akiec', 'vasc', 'df']
    print("Copying images of class directories inside all_images")
    for directory in directory_list:
        for file_ in os.listdir(directory):
            shutil.copyfile(directory + '/' + file_, 'all_images/' + file_)
    print("Done")


if __name__ == "__main__":
    #metadata = read_csv()
    #train_split()
    #preparing_directory(metadata)
    #subdivide_image(metadata)
    #print("DONE!")
    #data_augmentation()
    #count_element_dir()
    #create_metadata()
    aggregate_images()
    

