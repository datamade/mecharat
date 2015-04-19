import cv2
import numpy

''' 
Basic attempt at a labeller that displays a pair of images and expects a user
to press "y" or "n" to tell us if the images match. It just dumps out that
training when it's done displaying all of the combinations of images but we
could hypothetically take that input and train a model with it.
'''

def label(image1, image2):
    img1 = cv2.resize(cv2.imread(image1), (0,0,), fx=0.3, fy=0.3)
    img2 = cv2.resize(cv2.imread(image2), (0,0,), fx=0.3, fy=0.3)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    img3 = numpy.hstack([gray1, gray2])

    cv2.imshow('matches', img3)

    k = cv2.waitKey(0)
    if k == ord('y'):
        return 'match'
    elif k == ord('n'):
        return 'distinct'
    else:
        return 'unsure'

if __name__ == "__main__":
    import os
    from itertools import combinations
    import json

    imagedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fewer_images')
    training = {'match': [], 'distinct': []}
    pairs = combinations(os.listdir(imagedir), 2)
    for pair in pairs:
        image_paths = [os.path.join(imagedir, p) for p in pair]
        choice = label(*image_paths)
        training[choice].append(image_paths)
    print(json.dumps(training, indent=4))
