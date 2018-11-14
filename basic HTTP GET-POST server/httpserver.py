import socket
import threading
import argparse
import time
import pprint as pp

localtime = time.asctime( time.localtime(time.time()) )


header ="\nHTTP/1.0 200 OK \nConnection: keep-alive\nServer: gunicorn/19.9.0\nContent-Type= application/json"
Date =  localtime
ContentLength= ""
header2 = "\nAccess-Control-Allow-Origin: * \nAccess-Control-Allow-Credentials: true\nVia: 1.1 vegur"


getjson = {
  "args": {
    "course": "445",
    "Assignment": "2"
  },
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "_gauges_unique_hour=1; _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1",
    "Host": "localhost",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  "origin": "69.159.180.185",
  "url": "localhost.com/get"
}

postjson = {
  "args": {
    "course": "445",
    "Assignment": "2"
  },
  "data":{},
  "headers": {
    "Connection": "keep-alive",
    "Content-Length": "",
    "Content-Type": "",
    "Host": "localhost",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  "json": "",
  "origin": "",
  "url": "localhost.com/post"
}

def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
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
            getPost = getPost.strip()
            print(getPost)

            if getPost == "GET":
                getjson['origin'] = addr
                data = getjson
                print(data)
                headefinalget = header + "\nDate: " + str(Date) + "\nContent-Length: " + str(len(str(data))) + header2
                data= headefinalget + "\n\n\n\n" + str(data)
                data = str.encode(str(data))
                conn.sendall(data)
                break
            else:
                postjson['data'] = str(s).split("\r\n\r\n", 3)[1]
                postjson['headers']['Content-Length'] = len(str(s).split("\r\n\r\n", 3)[1])
                postjson['headers']['Content-Type'] = str(s).split("Content-Type", 3)[1]
                postjson['json'] = str(s).split("\r\n\r\n", 3)[1]
                postjson['origin'] = addr
                data = postjson
                headefinal = header + "\nDate: " + str(Date) + "\nContent-Length: " + str(len(str(data))) + header2
                data = headefinal +"\n\n\n\n" + str(data)
                data = str.encode(str(data))
                pp.pprint(data)
                conn.sendall(data)
                break



    finally:
        conn.close()


# Usage python echoserver.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=80)
args = parser.parse_args()
run_server('', args.port)