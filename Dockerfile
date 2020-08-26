# vault org api docker file
FROM ubuntu:18.04

WORKDIR /zilliqa

COPY /scripts /zilliqa/scripts

# install zilliqa deps
RUN /zilliqa/scripts/docker_install.sh

CMD ["/bin/bash"]