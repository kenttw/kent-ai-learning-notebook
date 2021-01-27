"""
 * Python script to demonstrate Canny edge detection.
 *
 * usage: python CannyEdge.py <filename> <sigma> <low_threshold> <high_threshold>
"""
import skimage
import skimage.feature
from skimage.viewer import ImageViewer
import os
import sys

from skimage import data
from skimage.viewer import ImageViewer

def showimg(img):
    # load the prepared dataset
    from numpy import load
    from matplotlib import pyplot
    pyplot.imshow(img,cmap='gray')
    pyplot.show()

def getImgList(path="/Users/kent/git/kent-ai-learning-notebook/Machine_Learning_Exercise/Pix2Pix/pet_dataset/images/"):
    import os
    files_path = [path + x for x in os.listdir(path)]
    return files_path


# read command-line arguments
def getEdge(filename = "./pet_dataset/images/Abyssinian_2.jpg"):

    try:
        fname = filename.split("/")[-1]

        to_file = "./pet_dataset/edge_images/"+fname
        if os.path.exists(to_file) :
            return

        sigma = 2.0#float(sys.argv[2])
        low_threshold = .1#float(sys.argv[3])
        high_threshold = .3#float(sys.argv[4])


        # load and display original image as grayscale
        image = skimage.io.imread(fname=filename, as_gray=True)


        edges = skimage.feature.canny(
            image=image,
            sigma=sigma,
            low_threshold=low_threshold,
            high_threshold=high_threshold,
        )



        skimage.io.imsave(to_file,edges)
        print("*", end="")
    except:
        print("error at " + fname)


if __name__=='__main__':

    for p in getImgList():
        getEdge(p)
