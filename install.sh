# Configuration
HOME_DIR=/home/anshuman/
VERSION=3.2.0

# Installation
# sudo apt-get update
# sudo apt-get upgrade
sudo apt-get install -y build-essential cmake pkg-config
sudo apt-get install -y libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python2.7-dev

cd ${HOME_DIR}
wget -O opencv.zip https://github.com/Itseez/opencv/archive/${VERSION}.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/${VERSION}.zip
unzip opencv_contrib.zip

cd ${HOME_DIR}/opencv-${VERSION}/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=${HOME_DIR}/opencv_contrib-${VERSION}/modules \
    -D PYTHON_EXECUTABLE=/usr/bin/python \
    -D BUILD_EXAMPLES=ON ..

# Check output cmake, it should include python 2
# For more information check: http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/

make -j4
sudo make install
sudo ldconfig

cd ${HOME_DIR}
rm -rf opencv-${VERSION} opencv_contrib-${VERSION} opencv.zip opencv_contrib.zip

print "[INFO] Operation Successful!"
