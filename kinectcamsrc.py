#!/usr/bin/env python
""" Source buf """
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#

import gobject
#gobject.threads_init()

import pygst
pygst.require('0.10')
import gst

import numpy
import cv
import freenect


class KinectCamSrc(gst.BaseSrc):
    """ Cam """
    #here we register our plugin details
    __gstdetails__ = (
        "Kinect cam source",
        "kinectcamsrc.py",
        "Source element for Kinect camera",
        "Oleksandr Lavrushchenko <kpykcb@gmail.com>")
 
    _src_template = gst.PadTemplate ("src",
                                     gst.PAD_SRC,
                                     gst.PAD_ALWAYS,
                                     gst.caps_from_string ("video/x-raw-rgb,bpp=24,depth=24,width=[ 1, 2147483647 ],height=[ 1, 2147483647 ],framerate=[ 0/1, 2147483647/1 ]"))
 
    __gsttemplates__ = (_src_template,)


    def __init__ (self, *args, **kwargs):
        gst.BaseSrc.__init__(self)
        gst.info('creating srcpad')
        self.src_pad = gst.Pad (self._src_template)
        self.src_pad.use_fixed_caps()

    def do_create(self, offset, length):
        rgb, timestamp = freenect.sync_get_video()
        databuf = numpy.getbuffer(rgb.view(numpy.uint8))
        self.buf = gst.Buffer(databuf)
        self.buf.timestamp = 0
        self.buf.duration = pow(2, 63) -1
        return gst.FLOW_OK, self.buf

# Register element class
gobject.type_register(KinectCamSrc)
gst.element_register(KinectCamSrc, 'kinectcamsrc', gst.RANK_MARGINAL)

