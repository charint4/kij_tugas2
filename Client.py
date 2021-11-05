import socket
import sys
import threading
import DES
import time


def read_msg(sock):
    while True:
        data = sock.recv(65535)
        if len(data) == 0:
            break
        data = data.decode("utf-8")
        if len(data.split()) == 2:
            user, msg = data.split()
            print("\nMessage before decrypted: " + DES.bin2hex(msg))
            print("After decrypted:")
            msg = DES.encrypt(msg, rkb_rev, rk_rev)
            print(user + " " + DES.bin2ascii(msg))
        else:
            print(data)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 6666))
sock.send(bytes(sys.argv[1], "utf-8"))

thread_cli = threading.Thread(target=read_msg, args=(sock,))
thread_cli.start()

key = "testes12"
rkb = []
rk = []
DES.init_keys(key, rkb, rk)
rkb_rev = rkb[::-1]
rk_rev = rk[::-1]

while True:
    dest = input("Input username destination : ")
    msg = input("Input message :")
    if len(msg) != 8:
        print("Message must be 8 characters long")
    else:
        msg = DES.ascii2bin(msg)
        cipher_text = DES.encrypt(msg, rkb, rk)
        print("Encrypted message: " + DES.bin2hex(cipher_text))
        sock.send(bytes("{}|{}".format(dest, cipher_text), "utf-8"))
    time.sleep(0.5)
