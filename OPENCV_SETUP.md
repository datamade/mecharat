# Setting up OpenCV for Python 3

This should be easier as soon as OpenCV 3.0 is actually released, but for now
...

Get normal virtualenv setup going:

```bash
$ mkvirtualenv -p /usr/local/bin/python3 opencv
```

The ``cmake`` command you'll want looks a little like this:

```
$ cmake -Wno-dev -DCMAKE_BUILD_TYPE=Release \
                 -DBUILD_opencv_python2=OFF \
                 -DPYTHON3_PACKAGES_PATH=/Users/eric/.virtualenvs/opencv/lib/python3.4/site-packages \
                 -DBUILD_opencv_python3=ON \
                 -DPYTHON3_NUMPY_INCLUDE_DIRS=/Users/eric/.virtualenvs/opencv/lib/python3.4/site-packages/numpy/core/include \
                 -DPYTHON3_EXECUTABLE=/Users/eric/.virtualenvs/opencv/bin/python \
                 -DPYTHON3_INCLUDE_DIR=/Users/eric/.virtualenvs/opencv/include/python3.4m \
                 -DPYTHON3_LIBRARY=/usr/local/Cellar/python3/3.4.3/Frameworks/Python.framework/Versions/3.4/lib/libpython3.4m.dylib \
                 -DPYTHON2_EXECUTABLE=/Users/eric/.virtualenvs/opencv-2.7/bin/python2.7 \
                 -DPYTHON2_INCLUDE_DIR=/Users/eric/.virtualenvs/opencv-2.7/include/python2.7 \
                 -DPYTHON2_LIBRARY=/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib \
                 -DPYTHON2_NUMPY_INCLUDE_DIRS=/Users/eric/.virtualenvs/opencv-2.7/lib/python2.7/site-packages/numpy/core/include \
                 ..
```
