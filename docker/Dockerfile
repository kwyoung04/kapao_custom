FROM       nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04
MAINTAINER eric@zerontech.com

ARG DEBIAN_FRONTEND=noninteractive

RUN        apt-key del 7fa2af80
RUN        apt update && apt install -y --no-install-recommends wget
RUN        wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb
RUN        dpkg -i cuda-keyring_1.0-1_all.deb

RUN        apt update
RUN        apt install -y \
           vim \
           sudo \
           gedit \
           libboost-all-dev \
           libssl-dev \
           python3-setuptools \
           git 



################ python 3.8    ################
RUN apt install -y python3.8-dev
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN apt install -y python3-pip
RUN pip3 install --upgrade pip
       


################ pytorch 1.11.0 ################
RUN pip3 install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
ADD upsampling.py /usr/local/lib/python3.8/dist-packages/torch/nn/modules/


################ kapao nia ################
#WORKDIR /home/ubuntu
#RUN git clone https://github.com/kwyoung04/kapao_custom.git

################ user setting ################
ARG  HOST_USER=ubuntu
ARG  UNAME=${HOST_USER}
ARG  HOME=/home/${UNAME}
ARG  MAINPC_IP=localhost
ARG  UID=1000
ARG  GID=1000

RUN  groupadd --system --gid ${GID} ${UNAME} \
 &&  useradd -rm -d ${HOME} -s /bin/bash -g root -G sudo,audio,video,plugdev -u ${UID} ${UNAME} \
 &&  usermod -aG dialout ${UNAME} \
 &&  usermod -aG sudo ${UNAME} \
 &&  mkdir -p /etc/sudoers.d \
 &&  echo "${UNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${UNAME} \
 &&  chmod 0440 /etc/sudoers.d/${UNAME} 

USER  ${UNAME}
WORKDIR  $HOME