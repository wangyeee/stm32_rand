from serial import Serial
import os

def printData(data):
    print(''.join('%02x'%i for i in data))

if __name__ == '__main__':
    size = 1024 * 1024
    size *= 10
    batchSize = 64
    i = 0
    serialPort = Serial('COM10', timeout = 2)
    if os.path.exists('rand.bin'):
        os.remove('rand.bin')
    binFile = open('rand.bin', 'wb')
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
