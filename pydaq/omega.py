from __future__ import print_function
import sys

__author__ = 'rob'

import daqflex


def configure(mccdevice):
    from mmap import ACCESS_READ, mmap
    import usb
    # import time
    # print("Attempting FPGACFG/0xAD unlock...")
    # r = mccdevice.send_message(u'DEV:FPGACFG/0xAD')
    # if u'DEV:FPGACFG=CONFIGMODE' != r:
    #     raise IOError('Unable to enter FPGA configuration mode. {}'.format(r))
    # print('Unlocked. {}'.format(r))

    rbf = open('USB-1608GX.iic', mode='rb')
    mm = mmap(rbf.fileno(), 0, access=ACCESS_READ)
    i = 0
    print('Sending {} on Endpoint 0, command 0x51...'.format(rbf.name))
    while i < mm.size():
        rbfbytes = mm[i:i+64]
        mccdevice.dev.ctrl_transfer(
            usb.TYPE_VENDOR + usb.ENDPOINT_OUT,
            0x51,
            0,
            0,
            rbfbytes
        )
        # print('{}: {}'.format(chunk, len(rbfbytes)))
        i += len(rbfbytes)
    mccdevice.dev.ctrl_transfer(
        usb.TYPE_VENDOR + usb.ENDPOINT_OUT,
        0x51,
        0,
        0,
        ""
    )
    print('Sent {} bytes.'.format(i))
    mm.close()
    rbf.close()
    # time.sleep(2)
    # mccdevice.send_message(u'AISCAN:QUEUE=DISABLE')
    # mccdevice.send_message(u"DEV:FLASHLED/1")
    #r = mccdevice.send_message(u'?DEV:FPGACFG')
    #print(r)
    #if u'CONFIGURED' in r:
    #    print('Successfully delivered firmware to device. ({})'.format(r))
    #else:
    #    raise IOError('Failed to complete firmware send. ({})'.format(r))


def testing(device):
    good_commands = {
        "Flash": "DEV:FLASHLED/1",
        "AI scan disable": "AISCAN:QUEUE=DISABLE"
    }

    good_queries = {
        "Temp 0": "?DEV:TEMP{0}",
        "Temp 1": "?DEV:TEMP{1}",
        "FPGA Configuration": "?DEV:FPGACFG",
        "Device ID": "?DEV:ID"
    }

    try:
        print ("\n\nCommands.")
        for name, message in good_commands.iteritems():
            print('{} response: {}'.format(name, device.send_message(message)))

        print ("\n\nQueries.")
        for name, message in good_queries.iteritems():
            print('{} response: {}'.format(name, device.send_message(message)))

    except IOError as e:
        print("Omega script failed :(", file=sys.stderr)
        print(e, file=sys.stderr)


if __name__ == "__main__":
    d = daqflex.USB_1608GX()
    print('Found {} (1680GX) on USB: {}'.format(d.id_product, d.dev.serial_number))
    # if u'CONFIGMODE' in response:
    # print("Configuration required.")
    configure(d)
    testing(d)