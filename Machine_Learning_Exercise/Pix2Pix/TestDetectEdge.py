import DetectEdge

def testGetImgList():
    p =  DetectEdge.getImgList()
    assert p


def testGetEdge():
    from os import path
    DetectEdge.getEdge("/Users/kent/git/kent-ai-learning-notebook/Machine_Learning_Exercise/Pix2Pix/pet_dataset/images/Abyssinian_1.jpg")
    assert path.exists("/Users/kent/git/kent-ai-learning-notebook/Machine_Learning_Exercise/Pix2Pix/pet_dataset/edge_images/Abyssinian_1.jpg")
