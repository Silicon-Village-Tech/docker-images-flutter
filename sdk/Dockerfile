FROM cirrusci/android-sdk:33
# FROM node:slim
USER root

COPY debug.keystore /root/.android/debug.keystore
COPY gp-uploader /opt/gp/
RUN chmod +x /opt/gp/gp-uploader
COPY gp-uploader.py /opt/gp/
ENV PATH ${PATH}:/opt/gp/



ENV FLUTTER_HOME=${HOME}/sdks/flutter \
    FLUTTER_VERSION=3.32.0
ENV FLUTTER_ROOT=$FLUTTER_HOME

ENV PATH ${PATH}:${FLUTTER_HOME}/bin:${FLUTTER_HOME}/bin/cache/dart-sdk/bin

RUN git clone --depth 1 --branch ${FLUTTER_VERSION} https://github.com/flutter/flutter.git ${FLUTTER_HOME}

RUN flutter precache

RUN yes | flutter doctor --android-licenses \
    && flutter doctor \
    && chown -R root:root ${FLUTTER_HOME}

RUN curl -O https://github.com/google/bundletool/releases/download/1.14.1/bundletool-all-1.14.1.jar
RUN mv bundletool-all-1.14.1.jar bundletool.jar

RUN apt-get update -qqy && apt-get install -qqy \
        curl \
        gcc \
        python3-dev \
        python3-pip \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
        gnupg \
        openjdk-11-jdk \
        unzip
RUN pip3 install -U crcmod google-api-python-client google-auth

RUN curl -sL https://firebase.tools | bash

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-427.0.0-linux-x86_64.tar.gz

RUN tar -xvf google-cloud-cli-427.0.0-linux-x86_64.tar.gz -C /opt

RUN /opt/google-cloud-sdk/install.sh --quiet

ENV PATH ${PATH}:/opt/google-cloud-sdk/bin

#installing sonar scanner
RUN curl -O https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.7.0.2747-linux.zip
RUN unzip sonar-scanner-cli-4.7.0.2747-linux.zip -d /opt


ENV PATH ${PATH}:/opt/sonar-scanner-cli-4.7.0.2747-linux/bin

