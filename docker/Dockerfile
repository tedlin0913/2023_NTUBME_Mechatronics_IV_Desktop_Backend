ARG FROM_IMAGE

FROM $FROM_IMAGE

SHELL ["/bin/bash", "-c"]

# ARGs are scoped to the stage
ARG USER
ARG ROS_DISTRO

ENV USER ${USER}
ENV ROS_DISTRO ${ROS_DISTRO}
# Create the ros_ws workspace in the Docker image

RUN apt-get update \
    && apt-get install -y \
    python3-pip \
    git \  
    python3-rosdep \
    python3-colcon-common-extensions \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/${USER}/ros_ws/src

COPY ../ros_ws/src/.repo .
RUN pip3 install flask opencv-python-headless numpy==1.23.0 vcstool
RUN vcs import ./ < .repo

WORKDIR /home/${USER}/ros_ws

# TODO: build source
RUN . /opt/ros/${ROS_DISTRO}/setup.sh \
    && rosdep init \
    && rosdep update \
    && rosdep install -i --from-path src --rosdistro ${ROS_DISTRO} -y \
    && colcon build --symlink-install \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*



RUN echo ". /opt/ros/${ROS_DISTRO}/setup.sh" >> ~/.bashrc \
    && echo ". /home/${USER}/ros_ws/install/setup.bash" >> ~/.bashrc


COPY ../docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]   
CMD ["bash"]


