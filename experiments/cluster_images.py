import cv2
from labeler import label

''' 
This just takes a pair of images, uses the SURF algorithm to find keypoints and
then uses a FLANN based matcher to find where those keypoints match. 
'''

def findMatch(image1, image2, min_keypoints=50):
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

    if len(good) > min_keypoints:
        # Return average of distances
        return True, (sum(good) / len(good))
    return False, 1

if __name__ == "__main__":
    import os
    from itertools import combinations
    import json
    import numpy
    from dedupe.clustering import cluster
    from random import randrange

    imagedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dumped_images')
    all_images = {idx: i for idx, i in enumerate(os.listdir(imagedir))}

    # Just doing 20 random combos to test it out
    choices = [randrange(0, len(all_images.keys())) for i in range(20)]
    pairs = combinations(choices, 2)
    results = []
    for idx, pair in enumerate(pairs):
        image1, image2 = [os.path.join(imagedir, all_images[p]) for p in pair]
        match, distance = findMatch(image1, image2, min_keypoints=60)
        if distance < 1:
            results.append(((pair[0], pair[1],), (1 - distance),))
            with open('results.json', 'w') as f:
                f.write(json.dumps(results, indent=4))
        if idx % 100 == 0:
            print('made %d comparisons' % idx)
    results = numpy.fromiter(results, dtype=[('pairs', 'i8', 2), ('score', 'f4', 1,)])
    clusters = cluster(results)
    for indexes, scores in clusters:
        images = []
        i = 0
        for index in indexes:
            image_name = all_images[index]
            image_path = os.path.join(imagedir, image_name)
            cluster_path = 'clustered_images/{0}'.format(str(i))

            # There must be a better way to do this
            try:
                os.mkdir(cluster_path)
            except OSError:
                for f in os.listdir(cluster_path):
                    try:
                        os.remove(f)
                    except OSError:
                        pass
            print('writing %s' % image_name)
            with open(image_path, 'rb') as inp:
                with open(os.path.join('clustered_images', str(i), image_name), 'wb') as outp:
                    outp.write(inp.read())
            i += 1




