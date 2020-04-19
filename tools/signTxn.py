#!/usr/bin/env python3

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
import argparse
import struct

# Generated from Zilliqa-Js library:
# encodeTransactionProto({
#     "version": 65537,
#     "nonce": 43,
#     "toAddr": "6E263953C92b12060Fd73885FC56e300631591F9",
#     "amount": new BN(100000000000000),
#     "gasPrice": new BN(10000000000),
#     "gasLimit": Long.fromNumber(30),
#     "code": "",
#     "data": "{ \"_tag\":\"SubmitCustomTransferFromTransaction\", \"params\":[{\"vname\":\"proxyTokenContract\",\"type\":\"ByStr20\",\"value\":\"0x6e263953c92b12060fd73885fc56e300631591f9\"},{\"vname\":\"from\",\"type\":\"ByStr20\",\"value\":\"0x5abf71d798ca594b7317b04f52ad5a31fae62170\"},{\"vname\":\"to\",\"type\":\"ByStr20\",\"value\":\"0x5420599c5d62c00b69675cfccf5f14627c1693c5\"},{\"vname\":\"value\",\"type\":\"Uint128\",\"value\":\"10000000\"}]}"
# })
EncodedTxn = "08818004102b1a146e263953c92b12060fd73885fc56e300631591f922030a01002a120a10000000000000000000005af3107a400032120a10000000000000000000000002540be400381e4a82037b20225f746167223a225375626d6974437573746f6d5472616e7366657246726f6d5472616e73616374696f6e222c2022706172616d73223a5b7b22766e616d65223a2270726f7879546f6b656e436f6e7472616374222c2274797065223a2242795374723230222c2276616c7565223a22307836653236333935336339326231323036306664373338383566633536653330303633313539316639227d2c7b22766e616d65223a2266726f6d222c2274797065223a2242795374723230222c2276616c7565223a22307835616266373164373938636135393462373331376230346635326164356133316661653632313730227d2c7b22766e616d65223a22746f222c2274797065223a2242795374723230222c2276616c7565223a22307835343230353939633564363263303062363936373563666363663566313436323763313639336335227d2c7b22766e616d65223a2276616c7565222c2274797065223a2255696e74313238222c2276616c7565223a223130303030303030227d5d7d"

def apduPrefix():
    # https://en.wikipedia.org/wiki/Smart_card_application_protocol_data_unit
    CLA = bytes.fromhex("E0")
    INS = b"\x04"
    P1 = b"\x00"
    P2 = b"\x00"

    return CLA + INS + P1 + P2


def main(args):
    STREAM_LEN = 16 # Stream in batches of STREAM_LEN bytes each.
    indexBytes = struct.pack("<I", args.index)
    txnBytes = bytearray.fromhex(EncodedTxn)

    print("txnBytes: " + txnBytes.hex())
    if len(txnBytes) > STREAM_LEN:
        txn1Bytes = txnBytes[0:STREAM_LEN]
        txnBytes = txnBytes[STREAM_LEN:]
    else:
        txn1Bytes = txnBytes
        txnBytes = bytearray(0)

    txn1SizeBytes = struct.pack("<I", len(txn1Bytes))
    hostBytesLeftBytes = struct.pack("<I", len(txnBytes))

    prefix = apduPrefix()
    # See signTxn.c:handleSignTxn() for sequence details of payload.
    # 1. 4 bytes for indexBytes.
    # 2. 4 bytes for hostBytesLeftBytes.
    # 3. 4 bytes for txn1SizeBytes (number of bytes being sent now).
    # 4. txn1Bytes of actual data.
    payload = indexBytes + hostBytesLeftBytes + txn1SizeBytes + txn1Bytes
    L_c = bytes([len(payload)])
    apdu = prefix + L_c + payload

    dongle = getDongle(True)
    result = dongle.exchange(apdu)

    # Keep streaming data into the device till we run out of it.
    # See signTxn.c:istream_callback() for how this is used.
    # Each time the bytes sent consists of:
    #  1. 4-bytes of hostBytesLeftBytes.
    #  2. 4-bytes of txnNSizeBytes (number of bytes being sent now).
    #  3. txnNBytes of actual data.
    while len(txnBytes) > 0:
        if len(txnBytes) > STREAM_LEN:
            txnNBytes = txnBytes[0:STREAM_LEN]
            txnBytes = txnBytes[STREAM_LEN:]
        else:
            txnNBytes = txnBytes
            txnBytes = bytearray(0)
        hostBytesLeftBytes = struct.pack("<I", len(txnBytes))
        txnNSizeBytes = struct.pack("<I", len(txnNBytes))
        payload = hostBytesLeftBytes + txnNSizeBytes + txnNBytes
        L_c = bytes([len(payload)])
        apdu = prefix + L_c + payload
        result = dongle.exchange(apdu)

    print("Response: " + result.hex())
    print("Length: " + str(len(result)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('--txnJson', '-j', type=str, required=False)
    parser.add_argument('--index', '-i', type=int, required=True)
    args = parser.parse_args()
    main(args)
