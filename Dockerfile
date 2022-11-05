FROM osrf/ros:melodic-desktop-full
LABEL maintainer="Kin Zhang <kin_eng@163.com>"

# Just in case we need it
ENV DEBIAN_FRONTEND noninteractive

# install zsh
RUN apt update && apt install -y wget git zsh tmux vim g++ rsync
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p git \
    -p ssh-agent \
    -p https://github.com/agkozak/zsh-z \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting

RUN apt update && apt install -y python-wstool python-catkin-tools ros-melodic-cmake-modules protobuf-compiler autoconf build-essential libtool

RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws
RUN catkin init
RUN catkin config --extend /opt/ros/melodic
RUN catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release
RUN catkin config --merge-devel
WORKDIR /root/catkin_ws/src/
RUN git clone https://github.com/Kin-Zhang/voxblox.git
RUN wstool init . ./voxblox/voxblox_https.rosinstall
RUN wstool update