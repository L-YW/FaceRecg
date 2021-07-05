#!/usr/bin/env python
# -*- coding: utf8 -*-

import cv2
import socket
import numpy
import argparse
import threading
import serial
import time
import random

for i in range(0,10) :
    print(  float(random.randrange(110000, 145000)) / 100000 )