import cv2

''' 
This just takes a pair of images, uses the SURF algorithm to find keypoints and
then uses a FLANN based matcher to find where those keypoints match. It does
not do well on our images but we'll probably want to do something like this
eventually to actually cluster things.
'''

def grok_images(images):
    image1, image2 = images
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    
    surf = cv2.xfeatures2d.SURF_create()
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params,search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    matchesMask = [[0,0] for i in range(len(matches))]
    
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]

    draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)

    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

    cv2.imshow('matches', img3)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import os
    imagedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fewer_images')
    images = []
    for idx, image in enumerate(os.listdir(imagedir)):
        images.append(os.path.join(imagedir, image))
        if (idx + 1) % 2 == 0:
            grok_images(images)
            images = []
