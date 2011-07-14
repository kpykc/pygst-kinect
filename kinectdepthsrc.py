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


class KinectDepthSrc(gst.BaseSrc):
    """ Depth """
    #here we register our plugin details
    __gstdetails__ = (
        "Kinect depth source",
        "kinectdepthsrc.py",
        "Source element for Kinect depth",
        "Oleksandr Lavrushchenko <kpykcb@gmail.com>")
 
    _src_template = gst.PadTemplate ("src",
                                     gst.PAD_SRC,
                                     gst.PAD_ALWAYS,
                                     gst.caps_from_string ("video/x-raw-gray,bpp=(int)16,depth=(int)16,width=[ 1, 2147483647 ],height=[ 1, 2147483647 ],framerate=[ 0/1, 2147483647/1 ]"))

 
    __gsttemplates__ = (_src_template,)


    def __init__ (self, *args, **kwargs):
        gst.BaseSrc.__init__(self)
        gst.info('creating srcpad')
        self.src_pad = gst.Pad (self._src_template)
        self.src_pad.use_fixed_caps()

    def do_create(self, offset, length):
        depth, timestamp = freenect.sync_get_depth()
        databuf = numpy.getbuffer(depth)
        self.buf = gst.Buffer(databuf)
        self.buf.timestamp = 0
        self.buf.duration = pow(2, 63) -1
        return gst.FLOW_OK, self.buf

# Register element class
gobject.type_register(KinectDepthSrc)
gst.element_register(KinectDepthSrc, 'kinectdepthsrc', gst.RANK_MARGINAL)



