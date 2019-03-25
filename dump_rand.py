from serial import Serial
from serial.tools.list_ports import comports
from argparse import ArgumentParser
import os, sys

UNITS = {
    'K' : 1024,
    'M' : 1024 * 1024,
    'G' : 1024 * 1024 * 1024,
    'T' : 1024 * 1024 * 1024 * 1024
}

def printData(data):
    print(''.join('%02x'%i for i in data))

def parseSize(sizeStr):
    if sizeStr == None:
        return -1
    sizeStr = sizeStr.strip().upper()
    unit = sizeStr[len(sizeStr) - 1]
    if unit in UNITS:
        sz = int(sizeStr[0 : len(sizeStr) - 1])
        sz *= UNITS[unit]
        return sz
    return -2

def skipExistingFile(fileName):
    choice = 'A'
    while choice not in ('Y', 'N', 'YES', 'NO'):
        choice = input('File {} already exists, overwrite? Y/N: '.format(fileName))
        choice = choice.upper()
    return choice[0]

def listSerialPorts():
    portsInfo = sorted(comports(False))
    cnts = 0
    print('Searching available serial ports...')
    for p in portsInfo:
        print(str(p))
        cnts += 1
    if cnts == 0:
        print('No ports available')

if __name__ == '__main__':
    parser = ArgumentParser(description = 'Dump random data into a file.')
    parser.add_argument("--list", action = 'store_true', help='List available serial ports.')
    parser.add_argument('-p', required=False, help='The serial port, e.g. COM1 on Windows or /dev/ttyUSB0 on Linux.')
    parser.add_argument('-o', required=False, help='Output file name')
    parser.add_argument('-s', required=False, default='1M', help='File size, e.g. 64, 1K, 10M, 2G, etc.')

    args = parser.parse_args()
    if args.list:
        listSerialPorts()
        sys.exit(0)

    size = parseSize(args.s)
    if size < 10:
        print('Invalid size:', args.s)
        sys.exit(1)
    batchSize = 64
    i = 0
    if os.path.exists(args.o):
        c = skipExistingFile(args.o)
        if c == 'N':
            print('Skip existing file: {}'.format(args.o))
            sys.exit(0)
        print('Overwrite existing file: {}'.format(args.o))
        os.remove(args.o)
    binFile = open(args.o, 'wb')
    serialPort = Serial(args.p, timeout = 2)
    if serialPort.isOpen() == False:
        serialPort.open()
    if serialPort.isOpen():
        print('Serial port opened')
        while i < size:
            rand = serialPort.read(batchSize)
            binFile.write(rand)
            if i % 40960 == 0:
                printData(rand)
            i += batchSize
        binFile.close()
        serialPort.close()
        print('Serial port closed')
    else:
        print('Failed to open serial port')
