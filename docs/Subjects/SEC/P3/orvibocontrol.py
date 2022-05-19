#!/usr/bin/python2.7

import socket
import threading
import pyaes
import zlib
import struct
import json
import cStringIO
import random
import time
import Queue
import string
from collections import namedtuple
import BaseHTTPServer
from ctypes import *

SOCKET_MAC_ADDRESS = None

"""
A Packet
"""
TOrviboPkt = namedtuple('TOrviboPkt', ['header', 'body'])

"""
The header of every packet
"""
class TOrviboPktHeader(BigEndianStructure):
    _pack_ = 1
    _fields_ = [('signature', c_char*2),
            ('pkt_size', c_ushort),
            ('pkt_type', c_char*2),
            ('crc32_body', c_uint),
            ('session_id', c_char*32)]


# Packets read from socket
socket_read_Q = Queue.Queue()

# Packets to be sent to socket
socket_write_Q = Queue.Queue()

# Packets read from homemate server
server_read_Q = Queue.Queue()

# Packets to be sent to homemate server
server_write_Q = Queue.Queue()

class OrviboSession:
    def __init__(self):
        self.aes_key = 'khggd54865SNJHGF'
        self.session_id = None
        self.mutex = threading.Lock()

    def get_aes_key(self):
        self.mutex.acquire()
        key = self.aes_key
        self.mutex.release()
        return key
      
    def set_aes_key(self, key):
        self.mutex.acquire()
        self.aes_key = key
        self.mutex.release()

    def get_session_id(self):
        return self.session_id

    def set_session_id(self, sid):
        self.session_id = sid


"""
Reads numBytes from a network socket
"""
def read_socket(sock, numBytes):
    nRead = 0
    buf = cStringIO.StringIO()
    
    while nRead < numBytes:
        buf.write(sock.recv(numBytes - nRead))
        nRead = buf.tell()
    
    return buf.getvalue()


"""
Writes a buffer to a network socket
"""
def write_socket(sock, buf):
    sock.sendall(buf)


"""
Read one packet, returns header, body (which is encrypted)
"""
def read_packet(sock):
    header = TOrviboPktHeader.from_buffer_copy(read_socket(sock, sizeof(TOrviboPktHeader)))
    body_size = header.pkt_size - sizeof(TOrviboPktHeader)
    body = read_socket(sock, body_size)
    return TOrviboPkt(header, body)


"""
Write one packet, body must be encrypted before
"""
def write_packet(sock, pkt):
    write_socket(sock, string_at(addressof(pkt.header), sizeof(TOrviboPktHeader)) + pkt.body)

"""
Function to read packets from a network socket and put in a Q
"""
def read_worker(sock, Q):
    while True:
        pkt = read_packet(sock)
        Q.put(pkt)


"""
Function to write packets from a Q to a network socket
"""
def write_worker(sock, Q):
    while True:
        pkt = Q.get()
        write_packet(sock, pkt)

"""
Reads from src_Q and writes to dst_Q
"""
def pipe_queues_worker(session, src_Q, dst_Q):
    while True:
        pkt = src_Q.get()
        pkt = process_packet(session, pkt, src_Q, dst_Q)
        if pkt is not None:
            dst_Q.put(pkt)

"""
Encrypts buffer using AES-128 ECB PKCS#7
"""
def decrypt_buffer(ct, key):
    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
    pt = ''
    pt += decrypter.feed(ct)
    pt += decrypter.feed()
    return pt


"""
Decrypts buffer using AES-128 ECB PKCS#7
"""
def encrypt_buffer(pt, key):
    encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationECB(key))
    ct = ''
    ct += encrypter.feed(pt)
    ct += encrypter.feed()
    return ct


"""
Process a packet
"""
def process_packet(session, pkt, src_Q, dst_Q):
    global SOCKET_MAC_ADDRESS
    msg_json = json.loads(decrypt_buffer(pkt.body, session.get_aes_key()).strip('\x00'))
    
    # Packets from socket to server
    if src_Q == socket_read_Q and dst_Q == server_write_Q:
        print 
        print '[+] socket -> server'
        print msg_json
        
        if SOCKET_MAC_ADDRESS is None and 'uid' in msg_json:
            SOCKET_MAC_ADDRESS = msg_json['uid']

        if 'clientSessionId' in msg_json:
            if msg_json['clientSessionId'].startswith('drop_me_'):
                print '[*] Dropping...'
                pkt = None
   
    # Packets from server to socket
    elif src_Q == server_read_Q and dst_Q == socket_write_Q:
        print '[+] server -> socket'
        print msg_json
        print
        if 'key' in msg_json:
            session.set_aes_key(msg_json['key'])
            assert pkt.header.pkt_type == 'pk'
            session.set_session_id(pkt.header.session_id)

    return pkt


"""
Construct a packet from JSON dict
"""
def construct_packet_from_json(session_id, aes_key, body_json, pkt_type = 'dk'):
    enc_body = encrypt_buffer(json.dumps(body_json), aes_key)
    header = TOrviboPktHeader(signature = 'hd',
             pkt_size = sizeof(TOrviboPktHeader) + len(enc_body),
             pkt_type = pkt_type,
             crc32_body = zlib.crc32(enc_body) & 0xFFFFFFFF,
             session_id = session_id)

    return TOrviboPkt(header, enc_body)

"""
Generate a random string
"""
def generate_random_string(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


"""
Constructs an ON/OFF packet
"""
def construct_on_off_packet(session, switch='off'):
    body_json  = {'userName': 'arandom@email.com', #Not checked
                'clientSessionId': 'drop_me_' + generate_random_string(24), 
                'ver': '3.7.0', 
                'uid': SOCKET_MAC_ADDRESS, #mac address of socket
                'propertyResponse': 0, 
                'debugInfo': 'Android_ZhiJia365_23_3.7.0.302', 
                'cmd': 15, 
                'defaultResponse': 1, 
                'qualityOfService': 1, 
                'value4': 0, 
                'value3': 0, 
                'value2': 0, 
                'value1': 1 if switch == 'off' else 0,
                'serial': random.randrange(1<<28, 1<<30), # A large number 
                'delayTime': 0, 
                'order': switch, 
                'deviceId': 'a'*25} #Not checked
 
    return construct_packet_from_json(session.get_session_id(), session.get_aes_key(), body_json)

"""
Toggles the socket at regular intervals
"""
def switch_toggler(session, interval):
    current = 'off'
    while True:
        time.sleep(interval)
        if current == 'off':
            pkt = construct_on_off_packet(session, 'on')
            print '[+] Switching ON'
            current = 'on'
        else:
            pkt = construct_on_off_packet(session, 'off')
            print '[+] Switching OFF'
            current = 'off'
        
        socket_write_Q.put(pkt)


the_session = None

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        if s.path == '/':
            s.wfile.write('<html><head><title>Orvibo S20C Socket Controller</title></head>')
            s.wfile.write('<body><h2>Orvibo S20C Socket Controller</h2>')
            s.wfile.write('<a href="/on"><button type="button">Send ON command</button></a>')
            s.wfile.write('<br><a href="/off"><button type="button">Send OFF command</button></a>')
            s.wfile.write("</body></html>")
        
        elif s.path == '/on':
            pkt = construct_on_off_packet(the_session, 'on')
            socket_write_Q.put(pkt)
            s.wfile.write('<html><head><title>Orvibo S20C Socket Controller</title></head>')
            s.wfile.write('<body><h2>Orvibo S20C Socket Controller</h2>')
            s.wfile.write('<a href="/on"><button type="button">Send ON command</button></a>')
            s.wfile.write('<br><a href="/off"><button type="button">Send OFF command</button></a>')
            s.wfile.write('<h3>Turned ON!</h3>')
            s.wfile.write("</body></html>")

        elif s.path == '/off':
            pkt = construct_on_off_packet(the_session, 'off')
            socket_write_Q.put(pkt)
            s.wfile.write('<html><head><title>Orvibo S20C Socket Controller</title></head>')
            s.wfile.write('<body><h2>Orvibo S20C Socket Controller</h2>')
            s.wfile.write('<a href="/on"><button type="button">Send ON command</button></a>')
            s.wfile.write('<br><a href="/off"><button type="button">Send OFF command</button></a>')
            s.wfile.write('<h3>Turned OFF!</h3>')
            s.wfile.write("</body></html>")

        else:
            s.wfile.write('<html><head><title>Orvibo S20C Socket Controller</title></head>')
            s.wfile.write('<body><h2>404 Not Found</h2>')
            s.wfile.write("</body></html>")
        

def main():
    print '[+] Main'
    global the_session
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 8080))
    sock.listen(1)
    
    csock, _ = sock.accept()
    print '[+] Client connected'

    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.connect(('homemate.orvibo.com', 10001))
    session = OrviboSession()
    the_session = session

    socket_rw = threading.Thread(target=read_worker, args=(csock, socket_read_Q))
    socket_ww = threading.Thread(target=write_worker, args=(csock, socket_write_Q))
    server_rw = threading.Thread(target=read_worker, args=(ssock, server_read_Q))
    server_ww = threading.Thread(target=write_worker, args=(ssock, server_write_Q))

    socket_to_server_w = threading.Thread(target=pipe_queues_worker, args=(session, socket_read_Q, server_write_Q))
    server_to_socket_w = threading.Thread(target=pipe_queues_worker, args=(session, server_read_Q, socket_write_Q))

    # toggler = threading.Thread(target=switch_toggler, args=(session, 10))

    socket_rw.start()
    socket_ww.start()
    server_rw.start()
    server_ww.start()
    socket_to_server_w.start()
    server_to_socket_w.start()
    # toggler.start()

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('', 5555), Handler)
    print '[+] HTTP Server started on 5555'
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    main()
