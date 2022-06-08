FROM ubuntu:focal

RUN apt update && apt upgrade && apt autoremove
RUN apt install -y cmake
RUN apt install -y git
RUN apt install -y unzip
RUN apt install -y wget
RUN apt install -y libglu1-mesa-dev xorg-dev
RUN apt install -y yasm

RUN apt install -y python3-pip
RUN pip install --upgrade pip
RUN pip install Flask flask-cors

RUN mkdir -p /opt/build
WORKDIR /opt/build

WORKDIR /opt/build
RUN wget https://github.com/evilkermit/ospray_studio/archive/refs/heads/master.zip
RUN unzip master.zip
RUN mv ospray_studio-master ospray_studio
RUN mkdir /opt/build/ospray_studio/build
WORKDIR /opt/build/ospray_studio/build
RUN cmake ..
RUN cmake --build .

WORKDIR /opt/build
RUN git clone --depth=1 https://gitlab.com/AOMediaCodec/SVT-AV1.git svt
WORKDIR /opt/build/svt/Build
RUN cmake .. -G"Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
RUN make
RUN make install

WORKDIR /opt/build
RUN git clone --depth=1 https://github.com/FFmpeg/FFmpeg ffmpeg
WORKDIR /opt/build/ffmpeg
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"
ENV PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig"
RUN ./configure --enable-libsvtav1
RUN make

RUN mkdir -p /opt/run
WORKDIR /opt/run
ADD app .
