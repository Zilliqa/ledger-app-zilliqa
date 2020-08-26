export LEDGER_DIR=~/ledger # edit this as necessary.
export GCCPATH=${LEDGER_DIR}/devenv/gcc-arm-none-eabi-5_3-2016q1/bin/
export BOLOS_SDK=${LEDGER_DIR}/nanos-secure-sdk
# We use a custom script.ld. So $SCRIPT_LD must be set to point to it.
export SCRIPT_LD=/zilliqa/code/script.ld
source ${LEDGER_DIR}/ledgerenv/bin/activate # activate python3 virtualenv