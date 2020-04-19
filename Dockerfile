# vault org api docker file
FROM ubuntu:18.04

WORKDIR /ziliqa

COPY /scripts /ziliqa/scripts

# install ziliqa deps
RUN /ziliqa/scripts/ziliqa_install.sh

CMD ["/bin/bash"]