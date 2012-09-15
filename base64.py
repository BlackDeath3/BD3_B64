# Base64 Encoder/Decoder
# Author: David Frye
# Date: 09/14/2012
# Description: Encodes and decodes plaintext to and from base64 encoded data.
#           For more information, see: http://en.wikipedia.org/wiki/Base64

# Import the sys module to make use of command line arguments.
import sys

# This table maps 6-bit decimal values to characters.
base64Table = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '\n']

# Function: readInfileData
# Parameters: path, buffer
# Return: Boolean
# Description: Opens a file, then reads from the file and write this data into the buffer. Returns True upon successful data retrieval.
def readInfileData(path, buffer):
    with open(path, "r") as infile:
        i = 1
        character = infile.read(1)
        while(character != ""):
            buffer.append(character)
            infile.seek(i)
            character = infile.read(1)
            i += 1
    
    return True

# Function: writeOutfileData
# Parameters: path, buffer
# Return: Boolean
# Description: Opens a file, then reads from the buffer and write this data into the file. Returns True upon successful data insertion.
def writeOutfileData(path, buffer):
    with open(path, mode = "w") as outfile:
        for i in range(0, len(buffer)):
            outfile.write(buffer[i])
	    # The below commented-out code formats output data with newlines. However, it also causes propogating errors during encoding/decoding.
##            if(0 == (i + 1) % 80):
##                outfile.write('\n')
	    #
		
    return True

# Function: bitEncode
# Parameters: readBuffer, bitBuffer, mask, width
# Return: None
# Description: Converts "width"-bit wide input data from readBuffer into a bit stream and writes this stream to bitBuffer.
def bitEncode(readBuffer, bitBuffer, width):
    mask = 2 ** (width - 1)
    for x in readBuffer:
        for y in range(0, width):
            if(mask == (mask & (x << y))):
                bitBuffer.append(1)
            else:
                bitBuffer.append(0)

# Function: bitDecode
# Parameters: readBuffer, bitBuffer, mask, width
# Return: None
# Description: Converts "width"-bit wide input data from readBuffer into a bit stream and writes this stream to bitBuffer.
def bitDecode(bitBuffer, writeBuffer, width):
    value = 0
    for i in range(0, len(bitBuffer)):
        bitPlace = (width - 1) - (i % width)
        value += bitBuffer[i] * (2 ** bitPlace)
        if(0 == (i + 1) % width):
            writeBuffer.append(value)
            value = 0
    if(0 != value):
        writeBuffer.append(value)

# Function: fileEncode
# Parameters: infilePath, outfilePath
# Return: Boolean
# Description: Encodes plaintext data from a file and writes that encoded data to a file.
def fileEncode(infilePath, outfilePath):
    plaintext = []
    asciiText = []
    bitBuffer = []
    indexBuffer = []
    ciphertext = []
    
    readInfileData(infilePath, plaintext)
    for x in plaintext:
        asciiText.append(ord(x))
    bitEncode(asciiText, bitBuffer, 8)
    bitDecode(bitBuffer, indexBuffer, 6)
    for x in indexBuffer:
        ciphertext.append(base64Table[x])
    writeOutfileData(outfilePath, ciphertext)
                
    return True

# Function: fileDecode
# Parameters: infilePath, outfilePath
# Return: Boolean
# Description: Decodes ciphertext data from a file and writes that decoded data to a file.
def fileDecode(infilePath, outfilePath):
    ciphertext = []
    indexBuffer = []
    bitBuffer = []
    asciiText = []
    plaintext = []

    readInfileData(infilePath, ciphertext)
    for x in ciphertext:
        if(64 != base64Table.index(x)):
            indexBuffer.append(base64Table.index(x))
    bitEncode(indexBuffer, bitBuffer, 6)
    bitDecode(bitBuffer, asciiText, 8)
    for x in asciiText:
        plaintext.append(chr(x))
    writeOutfileData(outfilePath, plaintext)
    
    return True

# Function: main
# Parameters: operation, infilePath, outfilePath
# Return: None
# Description: Encodes or decodes data based upon command line arguments.
def main():
    if("encode" == sys.argv[1]):
        successful = fileEncode(sys.argv[2], sys.argv[3])
        if(True == successful):
            print("Finished encoding %s to %s." % (sys.argv[2], sys.argv[3]))
    elif("decode" == sys.argv[1]):
        successful = fileDecode(sys.argv[2], sys.argv[3])
        if(True == successful):
            print("Finished decoding %s to %s." % (sys.argv[2], sys.argv[3]))
    else:
        print("ERROR!")

# Call main() to begin program execution.
if __name__ == '__main__':
    main()
