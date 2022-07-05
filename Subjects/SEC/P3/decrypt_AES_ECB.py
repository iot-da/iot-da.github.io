#!/usr/bin/python3

from Crypto.Cipher import AES
from binascii import unhexlify

aeskey="KEY"

wiresharkpacket = unhexlify("WireShark_Data_as_HexStream")

aesobj = AES.new(aeskey, AES.MODE_ECB)
print(aesobj.decrypt(wiresharkpacket[42:]))