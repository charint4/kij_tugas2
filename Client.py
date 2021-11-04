import socket
import sys
import threading
import DES
import time


def read_msg(sock_cli):
    while True:
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break
        data = data.decode("utf-8")
        if len(data.split()) == 2:
            user, msg = data.split()
            print("\nPesan sebelum didekripsi: " + DES.bin2hex(msg))
            print("Setelah didekripsi:")
            msg = DES.encrypt(msg, rkb_rev, rk_rev)
            print(user + " " + DES.bin2ascii(msg))
        else:
            print(data)


sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_cli.connect(("127.0.0.1", 6666))
sock_cli.send(bytes(sys.argv[1], "utf-8"))

thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

key = "testes12"
rkb = []
rk = []
DES.init_keys(key, rkb, rk)
rkb_rev = rkb[::-1]
rk_rev = rk[::-1]

while True:
    dest = input("Masukkan username tujuan: ")
    msg = input("Masukkan pesan anda: ")
    if len(msg) != 8:
        print("Pesan harus sepanjang 8 karakter")
    else:
        msg = DES.ascii2bin(msg)
        cipher_text = DES.encrypt(msg, rkb, rk)
        print("Pesan setelah dienkripsi: " + DES.bin2hex(cipher_text))
        sock_cli.send(bytes("{}|{}".format(dest, cipher_text), "utf-8"))
    time.sleep(0.5)
