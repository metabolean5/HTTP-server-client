import socket
import threading
import argparse
import os
from os import listdir

fileDir = os.path.dirname(os.path.realpath('__file__'))

def getFile(file):

    path = "data/" + str(file)
    filename = os.path.join(str(fileDir), path)

    print(filename.strip())

    with open(filename.strip(),'r') as f:
        read = f.read()

    return read




def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Echo server is listening at', port)
        file = open("welcome.txt", "r")
        print(file.read())
        while True:
            conn, addr = listener.accept()
            ##threading.Thread(target=handle_client, args=(conn, addr)).start()
            handle_client(conn,addr)
    finally:
        listener.close()


def handle_client(conn, addr):
    print('New client from' + str(addr) )
    try:
        while True:
            data = conn.recv(1024)
            data = data.decode("utf-8")
            s = str(data)
            print(s)
            getPost = str(s).split("/", 3)[0]
            try:
                fname = str(s).split("File:", 3)[1]
                fname = fname.strip()
            except:
                fname = "NULL"
            try:
                pdata = str(s).split("Data:", 3)[1]
                pdata = pdata.strip()
            except:
                pdata = "NULL"

            getPost = getPost.strip()

            print("FNAME CHECK ", fname)


            if (getPost == "POST"):
                fname = fname.replace(pdata,"")
                fname = fname.replace("Data:", "")
                if "../" in fname:
                    reply = 'THREAT DETECTED SYSTEM SHUTDOWN'
                    reply = str.encode(str(reply))
                    conn.sendall(reply)
                    return
                fname = fname.replace("../", "")
                print("FNAME : " + fname)
                path = "data/" + str(fname)
                filename = os.path.join(str(fileDir), path)
                print(filename.strip())
                f = open(filename.strip(), "w")
                print('LE DATA = '+ pdata)
                f.write(pdata)
                reply = 'CONTENT WRITTEN INTO FILE :'+ fname
                reply = str.encode(str(reply))
                conn.sendall(reply)
                break

            print('FNAME ' , fname)



            if (getPost == "GET" and fname== "NULL"):
                files = os.listdir("./data")
                print(files)
                files = str.encode(str(files))
                conn.sendall(files)
                break


            if (getPost == "GET" and fname):
                if "../" in fname:
                    reply = 'THREAT DETECTED SYSTEM SHUTDOWN'
                    reply = str.encode(str(reply))
                    conn.sendall(reply)
                    return
                dataToSend = getFile(fname)
                dataToSend = str.encode(str(dataToSend))
                conn.sendall(dataToSend)
                break


    except:
        print('error')
        reply = 'FILE ' + fname + ' DOES NOT EXIST'
        reply = str.encode(str(reply))
        conn.sendall(reply)

    conn.close()


# Usage python echoserver.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=80)
args = parser.parse_args()
run_server('', args.port)