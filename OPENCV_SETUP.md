# Setting up OpenCV for Python 3

This should be easier as soon as OpenCV 3.0 is actually released, but for now
...

**Get normal virtualenv setup going and install numpy**

``` bash
$ mkvirtualenv -p /usr/local/bin/python3 opencv
$ pip install numpy
```

**Install OS level dependencies** (these are hastily copied from an older set of
instructions I put together for this and might be inaccurate. Also, they are,
obviously, Ubuntu specific. OS X (aka Homebrew) versions of all these exist,
you'll just need to translate that for now, OK?)

``` bash
sudo apt-get install cmake libgtk2.0-dev pkg-config libavcodec-dev \
  libavformat-dev libswscale-dev libamd2.2.0 libblas3gf libc6 libgcc1 \
  libgfortran3 liblapack3gf libumfpack5.4.0 libstdc++6 build-essential \
  gfortran libatlas-dev libatlas-base-dev libblas-dev liblapack-dev libjpeg-dev \
  libpng-dev libtiff-dev libjasper-dev
```

**Clone OpenCV and OpenCV contrib**

``` bash
$ https://github.com/Itseez/opencv_contrib.git 
$ https://github.com/Itseez/opencv.git
```

The ``cmake`` command you'll want looks a little like the one below. Things to note:

* Despite building this thing for Python 3, you actually need to specify all of
that Python 2 junk, too. It's apparently needed for the build process
* The Python 2 that you're going to use needs numpy, too.
* Make sure you specify a packages path otherwise the shared objects (``.so`` 
files) will be placed in a path relative to where you are doing your build.
* The last flag passed below is a path to where you cloned Open CV Contrib

```
$ cmake -Wno-dev -DCMAKE_BUILD_TYPE=Release \
                 -DBUILD_opencv_python2=OFF \
                 -DPYTHON2_EXECUTABLE=/Users/eric/.virtualenvs/opencv-2.7/bin/python2.7 \
                 -DPYTHON2_INCLUDE_DIR=/Users/eric/.virtualenvs/opencv-2.7/include/python2.7 \
                 -DPYTHON2_LIBRARY=/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib \
                 -DPYTHON2_NUMPY_INCLUDE_DIRS=/Users/eric/.virtualenvs/opencv-2.7/lib/python2.7/site-packages/numpy/core/include \
                 -DBUILD_opencv_python3=ON \
                 -DPYTHON3_EXECUTABLE=/Users/eric/.virtualenvs/opencv/bin/python \
                 -DPYTHON3_INCLUDE_DIR=/Users/eric/.virtualenvs/opencv/include/python3.4m \
                 -DPYTHON3_LIBRARY=/usr/local/Cellar/python3/3.4.3/Frameworks/Python.framework/Versions/3.4/lib/libpython3.4m.dylib \
                 -DPYTHON3_NUMPY_INCLUDE_DIRS=/Users/eric/.virtualenvs/opencv/lib/python3.4/site-packages/numpy/core/include \
                 -DPYTHON3_PACKAGES_PATH=/Users/eric/.virtualenvs/opencv/lib/python3.4/site-packages \
                 -DOPENCV_EXTRA_MODULES_PATH=/Users/eric/code/opencv/src/opencv_contrib/modules \
                 ..
```
