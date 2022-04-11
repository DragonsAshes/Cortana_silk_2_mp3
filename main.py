#!/usr/bin/env python

import sys
import os
import pyshark

audio_offset = 276 #Define the offset to the data representing the audio in the payload

def build_data(requete, ip, output):
    filter = "websocket && ip.src == "+ip+" && websocket.opcode == binary"
    caps = pyshark.FileCapture(requete, include_raw=True, use_json=True, display_filter=filter)
    try:
        f = open(output, "w")
        for cap in caps:
            f.write(cap.websocket.payload_raw[0][audio_offset:])    
        f.close()
    except IOError:
        print('Error While Opening the file!')

def transform_data(output, decoder):
    pwd = os.getcwd()
    cmd = 'xxd -r -p '+output+' > '+output+'.slk'
    os.system(cmd)
    os.chdir(decoder)
    cmd = 'sh ./converter.sh '+pwd+'/'+output+'.slk mp3'
    os.system(cmd)

def show_help():
    print("python main.py <file.pcapng> <ip.src> <path to silk-v3-decoder> <output file>")

def main():
    if len(sys.argv) != 5:
        show_help()
    else:
        build_data(sys.argv[1], sys.argv[2], sys.argv[4])
        transform_data(sys.argv[4], sys.argv[3])

if __name__ == "__main__":
    main()
