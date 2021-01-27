# load, split and scale the maps dataset ready for training
from os import listdir
from numpy import asarray
from numpy import vstack
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from numpy import savez_compressed
from tqdm import tqdm


# load all images in a directory into memory
def load_images(src_path,tar_path, size=(256, 512)):
    src_list, tar_list = list(), list()
    # enumerate filenames in directory, assume all are images
    for filename in tqdm(listdir(src_path)[:100]):

        src_file = src_path + filename
        tar_file = tar_path + filename

        # load and resize the image
        src_pixels = load_img(src_file, target_size=size)
        tar_pixels = load_img(tar_file, target_size=size)
        # convert to numpy array
        src_pixels = img_to_array(src_pixels)
        tar_pixels = img_to_array(tar_pixels)

        src_list.append(src_pixels)
        tar_list.append(tar_pixels)
    return [asarray(src_list), asarray(tar_list)]


if __name__ == '__main__':
    path = "/Users/kent/git/kent-ai-learning-notebook/Machine_Learning_Exercise/Pix2Pix/pet_dataset/"

    src_path = path + "edge_images/"
    tar_path = path + "images/"
    [src_images, tar_images] = load_images(src_path,tar_path)
    filename = 'pet_256_100.npz'
    savez_compressed(filename, src_images, tar_images)
    print('Saved dataset: ', filename)

# if __name__ =="__main__":
#     # dataset path
#     path = 'maps/train/'
#     # load dataset
#     [src_images, tar_images] = load_images(path)
#     print('Loaded: ', src_images.shape, tar_images.shape)
#     # save as compressed numpy array
#     filename = 'maps_256.npz'
#     savez_compressed(filename, src_images, tar_images)
#     print('Saved dataset: ', filename)