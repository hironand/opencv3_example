# OpenCV3 quickstart on Python2.7, OSX

## Goal
* Running OpenCV3 using Python2.7 in OSX
* Using virtualenv
* Create OpenCV3 python project ong Intellij IDEA using virtualenv
* Make some example python program and run. 

## My Environment
* Mac OSX 10.12 Sierra
* Python 2.7 (installed)
* Numpy (installed)
* OpenCV2 (installed)

## Related Site
Official  
[http://opencv.org/](http://opencv.org/)

Introduction to OpenCV  
[http://docs.opencv.org/2.4/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html](http://docs.opencv.org/2.4/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html)

Github  
[https://github.com/opencv/opencv](https://github.com/opencv/opencv)
[https://github.com/opencv/opencv_contrib](https://github.com/opencv/opencv_contrib)


## Installation
Install OpenCV 3.0 and Python 2.7+ on OSX  
[http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/](http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/)


  
install Xcode  
-> Skip (installed)

### step.2
install Homebrew  
-> Skip (installed) 

### step.3
install Python  

before install python, add PATH in ~/.bash_profile and update.

```
export PATH=/usr/local/bin:$PATH
source ~/.bash_profile
```

install Python from Homebrew

```
brew install python
which python

/usr/local/bin/python
```

### Step.4  
install virtualenv  and virtualenvwrapper

```
sudo pip install virtualenv virtualenvwrapper
...
Successfully installed pbr-1.10.0 six-1.10.0 stevedore-1.19.0 virtualenv-15.1.0 virtualenv-clone-0.2.6 virtualenvwrapper-4.7.2
```

add ~/.bash_profile & update  

```
# Virtualenv/VirtualenvWrapper  
source /usr/local/bin/virtualenvwrapper.sh
```

```
source ~/.bash_profile
```

create a new Python environment

```
mkvirtualenv cv
...
Installing setuptools, pip, wheel...done.
```

### Step.5  
install Numpy on "cv" virtualenv environment.
```
pip install numpy
```

### Step.6  
install Cmake

```
brew install cmake pkg-config
```

install other packages.
-> skip (installed)

```
brew install jpeg libpng libtiff openexr
brew install eigen tbb
```

### Step.7/8  
compile and install OpenCV 3!!!

clone from git.

```
git clone https://github.com/opencv/opencv.git
git checkout 3.1.0
git status
...
HEAD detached at 3.1.0
```

```
git clone https://github.com/opencv/opencv_contrib.git
git checkout 3.1.0
git status
...
HEAD detached at 3.1.0
```

Confirm latest versioin or Dowonload from:
[http://opencv.org/downloads.html](http://opencv.org/downloads.html)

```
cd opencv_contrib/modules
cmake \
	-D OPENCV_EXTRA_MODULES_PATH=~/dev/src/github/opencv3/opencv_contrib/modules \
	-D BUILD_opencv_reponame=OFF ~/dev/src/github/opencv3/opencv
...
--   Python 2:
--     Interpreter:                 /usr/local/bin/python2.7 (ver 2.7.12)
--     Libraries:                   /usr/lib/libpython2.7.dylib (ver 2.7.12)
--     numpy:                       /Library/Python/2.7/site-packages/numpy/core/include (ver 1.11.1)
--     packages path:               lib/python2.7/site-packages

cat 
```

build cmake

```
cd opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D PYTHON2_PACKAGES_PATH=~/.virtualenvs/cv/lib/python2.7/site-packages \
	-D PYTHON2_LIBRARY=/Library/Frameworks/Python.framework/Versions/2.7/bin \
	-D PYTHON2_INCLUDE_DIR=/Library/Frameworks/Python.framework/Headers \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D BUILD_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/dev/src/github/opencv3/opencv_contrib/modules \
	-DBUILD_opencv_videoio=OFF ..
...
-- Configuring done
-- Generating done
-- Build files have been written to: ~/dev/src/github/opencv3/opencv/build
```

if `QTKit/QTKit.h  file not found ` error has occured, see blow.  

[QTKit not available anymore on macOS Sierra](https://github.com/clementfarabet/lua---camera/issues/27 "QTKit not available anymore on macOS Sierra")

In macOS 10.12, apple removed most of QTKit's components...  
[OpenCV 3.1 can't compile on macOS 10.12 beta because QTKit #6913](https://github.com/opencv/opencv/issues/6913 "OpenCV 3.1 can't compile on macOS 10.12 beta because QTKit #6913")


```
make -j4
...
[100%] Building CXX object modules/python2/CMakeFiles/opencv_python2.dir/__/src2/cv2.cpp.o
[100%] Linking CXX shared module ../../lib/cv2.so
[100%] Built target opencv_python2
```
```
sudo make install
...
-- Installing: /usr/local/share/OpenCV/samples/python/video_v4l2.py
-- Installing: /usr/local/share/OpenCV/samples/python/watershed.py
```

if openCV2 preinstalled, and CMake error occured,
```
CMake Error at include/cmake_install.cmake:31 (file):
  file INSTALL destination: /usr/local/include/opencv is not a directory.
Call Stack (most recent call first):
  cmake_install.cmake:77 (include)
...
```
openCV2 file rename to old.

```
mv /usr/local/include/opencv2 /usr/local/include/opencv2.old
mv /usr/local/share/OpenCV /usr/local/share/OpenCV.old
mv /usr/local/include/opencv /usr/local/include/opencv.old
```


### step.9  
check OpenCV3 is installed

```
cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
ls -l cv2.so 
-rwxr-xr-x  1 root  staff  2949336 12  4 13:52 cv2.so
```
installation succeed!!!

verify in python.

```
python
>>> import cv2
>>> cv2.__version__
'3.1.0-dev'
```
quiita ━━━ヽ(ヽ(ﾟヽ(ﾟ∀ヽ(ﾟ∀ﾟヽ(ﾟ∀ﾟ)ﾉﾟ∀ﾟ)ﾉ∀ﾟ)ﾉﾟ)ﾉ)ﾉ━━━!!!! 


### Other Links  
Installation in Linux  
[http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html#linux-installation](http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html#linux-installation)



## Using virtualenv

[virtulaenv](https://virtualenv.pypa.io/en/stable/ "virtulaenv")

### on terminal



We create virtualenv named "cv" .
to go into virtualenv

```
workon cv
```

to go out virtualenv  

```
deactivate
```

### on IntelliJ IDEA
[IntelliJ IDEAのPythonプラグインからもvirtualenvが使える](http://qiita.com/todogzm/items/973f35e4f7f269062b8e "IntelliJ IDEAのPythonプラグインからもvirtualenvが使える")

* create New Python Project
* Configure SDK -> Python SDK -> select python SDK on "cv" virtualenv path.
or We can create virtualenv on IntelliJ !!!














