import usb.core
import usb.util
import matplotlib.pyplot as plt
import cv2
import numpy as np

VENDOR_ID = 6447
PRODUCT_ID = 1046

# find the USB device
device = usb.core.find(idVendor=VENDOR_ID,idProduct=PRODUCT_ID)

if device.is_kernel_driver_active(0):
    reattach = True
    device.detach_kernel_driver(0)
# use the first/default configuration
device.set_configuration()
# In order to read the pixel bytes, reset PIX_GRAB by sending a write command
while True:
	response = device.ctrl_transfer(bmRequestType = 0x40, #Write
			                             bRequest = 0x01,
			                             wValue = 0x0000,
			                             wIndex = 0x0c, #PIX_GRAB register value
			                             data_or_wLength = None
			                             )
	# Read all the pixels (360 in this chip)
	pixList = []
	for i in range(361):
	    response = device.ctrl_transfer(bmRequestType = 0xC0, #Read
			                                 bRequest = 0x01,
			                                 wValue = 0x0000,
			                                 wIndex = 0x0c, #PIX_GRAB register value
			                                 data_or_wLength = 1
			                                 )
	    pixList.append(response)

	pixelArray = np.asarray(pixList)
	pixelArray = pixelArray.reshape((19,19))
	pixelArray = pixelArray.transpose()
	pixelArray = np.flipud(pixelArray)
	cv_img = pixelArray.astype(np.uint8)
	cv2.imshow('test',cv_img)
	cv2.waitKey(1)
