# imports libraries that will be used later on
from PIL import Image
import cv2
from plantcv import plantcv as pcv
import os

img = Image.open("DemoImage.JPG")
# img.show() shows image

# inputs are left top right than bottom
img_crop = img.crop((1875, 730, 5680, 3260))
# img_crop.show() shows cropped image
img_crop.save("Cropped_plate.png")

img_crop = cv2.imread("Cropped_plate.png")  # reads in the saved img
filter_image = pcv.rgb2gray_lab(img_crop, 'b')  # filters out colors to gray scale the image
Threshold = cv2.adaptiveThreshold(filter_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 241, -1)  # Thresholds based on a 241 block size
cv2.imwrite("Threshold.png", Threshold)  # Saves threshold
Threshold = pcv.fill(Threshold, 400)  # removes small white spots left by threshold
cv2.imwrite("Final_threshold.png", Threshold)  # saves threshold with fill changes

# now that we have the threshold we need to crop the clusters out so we can get data from each cluster of 4 cells

dire = os.getcwd()
path = dire + '/photo_dump'
try:
    os.makedirs(path) # so all the pics don't flood our main dir
except OSError:
    pass
img = Image.open("Cropped_plate.png")
sizeX, sizeY = img.size  # finds how big the image is in the x and y directions
sizeX = round(sizeX/12)  # 12 cols
sizeY = round(sizeY/8)  # 8 rows
cluster_counter = 0
# crops the main picture into 9 rows the last one we will ignore
for h in range(0, img.height, sizeY):
    im = img.crop((0, h, img.width - 1, min(img.height, h + sizeY) - 1))
    im.save(os.path.join(path, "RowImage." + str((round(h/316))) + ".png"))

# takes the row image and crops it again to give us 96 images
for i in range(0, 8):
    rowImage = (os.path.join(path, "RowImage.%d.png" % i))
    img = Image.open(rowImage)
    sizeX, sizeY = img.size
    sizeX = round(sizeX/12)
    sizeY = round(sizeY/8)
    width_start = 0
    width_end = sizeX
    for w in range(0, 12):
        im = img.crop((width_start, w, width_end, min(img.height, w + width_end) - 1))
        im.save(os.path.join(path, "Cluster." + str(cluster_counter) + ".png"))
        cluster_counter += 1
        width_start = width_start + sizeX
        width_end = width_end + sizeX

# same thing as above just with the threshold image instead
img = Image.open("Final_threshold.png")
sizeX, sizeY = img.size  # finds how big the image is in the x and y directions
sizeX = round(sizeX/12)  # 12 cols
sizeY = round(sizeY/8)  # 8 rows
cluster_counter = 0
# crops the main picture into 9 rows the last one we will ignore
for h in range(0, img.height, sizeY):
    im = img.crop((0, h, img.width - 1, min(img.height, h + sizeY) - 1))
    im.save(os.path.join(path, "RowImage_Threshold." + str((round(h/316))) + ".png"))

# takes the row image and crops it again to give us 96 images
for i in range(0, 8):
    rowImage = (os.path.join(path, "RowImage_Threshold.%d.png" % i))
    img = Image.open(rowImage)
    sizeX, sizeY = img.size
    sizeX = round(sizeX/12)
    sizeY = round(sizeY/8)
    width_start = 0
    width_end = sizeX
    for w in range(0, 12):
        im = img.crop((width_start, w, width_end, min(img.height, w + width_end) - 1))
        im.save(os.path.join(path, "Cluster_threshold." + str(cluster_counter) + ".png"))
        cluster_counter += 1
        width_start = width_start + sizeX
        width_end = width_end + sizeX

# now time to determine size
for c in range(0, 96):  # 96 because that is how many images we have to process
    CC_image = cv2.imread(os.path.join(path, "Cluster_threshold.%d.png" % c), cv2.IMREAD_UNCHANGED)
    circle_cell = cv2.imread(os.path.join(path, "Cluster.%d.png" % c))

    connectivity = 8  # either 4 or 8
    output = cv2.connectedComponentsWithStats(CC_image, connectivity)  # Will determine the size of our clusters
    

