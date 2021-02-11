from PIL import Image

from PIL import ImageFilter

# Create an image object

image = Image.open("./boy1.jpg")

# Find the edges by applying the filter ImageFilter.FIND_EDGES

imageWithEdges = image.filter(ImageFilter.FIND_EDGES)

# display the original show

image.show()

# display the new image with edge detection done

imageWithEdges.show()