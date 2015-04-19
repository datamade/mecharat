import numpy as np
import cv2

''' 
This is basically a worked example from the Python OpenCV docs that clusters
the classic example of the handwritten digits. I understand very little about
what it's actually doing but I think it's worth examining as we'll probably
need to do things like this eventually.
'''

img = cv2.imread('sample_files/digits.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# image is 2000 x 1000 so we are splitting it into the 20 x 20 cells 
# where the numbers are
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]

x = np.array(cells)

train = x[:,:50].reshape(-1,400).astype(np.float32)
test = x[:,50:100].reshape(-1,400).astype(np.float32)

k = np.arange(10)
train_labels = np.repeat(k,250)[:,np.newaxis]
test_labels = train_labels.copy()

knn = cv2.ml.KNearest_create()
td = cv2.ml.TrainData_create(train, train_labels)
knn.train(td)
ret,result,neighbours,dist = knn.find_nearest(test,k=5)

cv2.imshow(result)

matches = result==test_labels

correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print(accuracy)
