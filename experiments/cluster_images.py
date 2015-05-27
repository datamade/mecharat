import cv2
import os
from itertools import combinations
import json
import numpy
from dedupe.clustering import cluster, condensedDistance
import fastcluster
import hcluster
from random import randrange
import time

''' 
This just takes a pair of images, uses the SURF algorithm to find keypoints and
then uses a FLANN based matcher to find where those keypoints match. 
'''

imagedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dumped_images')
all_images = {idx: i for idx, i in enumerate(os.listdir(imagedir))}

def findMatch(image1, image2, min_keypoints=50):
    print(image1, image2)
    img1 = cv2.resize(cv2.imread(image1), (0,0,), fx=0.3, fy=0.3)
    img2 = cv2.resize(cv2.imread(image2), (0,0,), fx=0.3, fy=0.3)

    print('about to surf')
    surf = cv2.xfeatures2d.SURF_create(400)
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    print('about to matcher')
    matcher = cv2.FlannBasedMatcher(index_params,search_params)
    

    print('about to match')
    try:
        matches = matcher.knnMatch(des1,des2,k=2)
    except cv2.error as e:
        # Probably need to figure out what is actually happening here
        print(e)
        return False, 1

    # Iterate the matching keypoints and apply the ratio test described in
    # section 7.1 of the SIFT paper
    # https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf
    
    good = []
    for closest, second_closest in matches:
        good.append(closest.distance)

    if len(good) > min_keypoints:
        # Return average of distances
        # print(min(good), max(good))
        # print('%s, %s' % (len(good), 1 - (sum(good) / len(good))))
        return True, 1 - (sum(good) / len(good))
    return False, 1

def writeClusters(results):
    threshold = 0.9
    results = numpy.fromiter(results, dtype=[('pairs', 'i8', 2), ('score', 'f4', 1,)])
    i_to_id, condensed_distances, N = condensedDistance(results)
    linkages = fastcluster.linkage(condensed_distances, method='ward')
    partition = hcluster.fcluster(linkages, threshold, criterion='inconsistent')
    clusters = {}
    for (i, cluster_id) in enumerate(partition):
        clusters.setdefault(cluster_id, []).append(i_to_id[i])
    i = 0
    for cluster in clusters.values():
        images = []
        for index in cluster:
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
if __name__ == "__main__":

    if os.path.exists('results.json'):
        with open('results.json') as f:
            results = json.load(f)
            r = []
            for pair, score in results:
                r.append((tuple(pair), score))
            writeClusters(r)
    else:

        # Just doing 200 random combos to test it out
        choices = [randrange(0, len(all_images.keys())) for i in range(50)]
        # pairs = combinations(choices, 2)
        pairs = combinations(all_images.keys(), 2)
        results = []
        start = time.time()
        for idx, pair in enumerate(pairs):
            loop_start = time.time()
            image1, image2 = [os.path.join(imagedir, all_images[p]) for p in pair]
            match, score = findMatch(image1, image2, min_keypoints=325)
            if score < 1:
                # img1 = cv2.resize(cv2.imread(image1), (0,0,), fx=0.3, fy=0.3)
                # img2 = cv2.resize(cv2.imread(image2), (0,0,), fx=0.3, fy=0.3)
      
                # gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                # gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
      
                # img3 = numpy.hstack([gray1, gray2])
      
                # cv2.imshow('matches', img3)
      
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                results.append(((pair[0], pair[1],), score,))
                with open('results.json', 'w') as f:
                    f.write(json.dumps(results, indent=4))
            if idx % 100 == 0:
                elapsed = (time.time() - loop_start)
                total_elapsed = (time.time() - start)
                print('made %d comparisons (%s, %s)' % (idx, elapsed, total_elapsed))
                loop_start = time.time()




