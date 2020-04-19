#!/usr/bin/env bash

setup_ziliqa_app() {
   

 # create the ledger dir
    mkdir -p ~/ledger

    # export and activate it
    export LEDGER_DIR=~/ledger
    python3 -m venv ${LEDGER_DIR}/ledgerenv
    source ${LEDGER_DIR}/ledgerenv/bin/activate

    # install ledger blue software
    pip3 install wheel
    pip3 install ledgerblue
    
    SECP_BUNDLED_EXPERIMENTAL=1 pip3 --no-cache-dir install --no-binary secp256k1 secp256k1

    # get Ledger toolchain related pre-requisites
    cd $LEDGER_DIR; git clone https://github.com/LedgerHQ/nanos-secure-sdk
    wget -q https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q1-update/+download/gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2
    mkdir devenv; tar -xjf gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2 --directory devenv
}

ziliqa_deps=$(cat <<EOF
default-jdk
libudev-dev 
libusb-1.0-0-dev 
python3
python3-dev 
python3-venv 
python3-pip
gcc-multilib 
g++-multilib 
clang
git 
wget
autoconf
pkg-config
libtool
nano
net-tools
EOF
)

#install deps for ziliqa ledger nano app & then set it up
apt-get update
apt-get install -y ${ziliqa_deps}
setup_ziliqa_app

# remove dev deps & builds tools for ziliqa
apt-get clean
apt-get autoremove -y

# list contents
ls

exit 0