import cv2
from labeler import label

''' 
This just takes a pair of images, uses the SURF algorithm to find keypoints and
then uses a FLANN based matcher to find where those keypoints match. 
'''

MIN_MATCHES = 50

def findMatch(image1, image2):
    img1 = cv2.resize(cv2.imread(image1), (0,0,), fx=0.3, fy=0.3)
    img2 = cv2.resize(cv2.imread(image2), (0,0,), fx=0.3, fy=0.3)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    surf = cv2.xfeatures2d.SURF_create()
    kp1, des1 = surf.detectAndCompute(gray1, None)
    kp2, des2 = surf.detectAndCompute(gray2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params,search_params)

    try:
        matches = flann.knnMatch(des1,des2,k=2)
    except cv2.error as e:
        # Probably need to figure out what is actually happening here
        print(e)
        return False, 1

    # Iterate the matching keypoints and apply the ratio test described in
    # section 7.1 of the SIFT paper
    # https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf
    
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m.distance)

    if len(good) > MIN_MATCHES:
        # Return average of distances
        return True, (sum(good) / len(good))
    return False, 1

if __name__ == "__main__":
    import os
    from itertools import combinations
    import json
    import numpy

    imagedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dumped_images')
    pairs = combinations(os.listdir(imagedir), 2)
    results = []
    for pair in pairs:
        image_paths = [os.path.join(imagedir, p) for p in pair]
        match, distance = findMatch(*image_paths)
        results.append(((pair[0], pair[1],), distance,))
        with open('results.json', 'w') as f:
            f.write(json.dumps(results, indent=4))

