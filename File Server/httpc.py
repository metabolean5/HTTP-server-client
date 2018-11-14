import socket
import argparse
import sys
import re
import json
import pprint
#import httplib


#exec("home/Dev/python/445/a1/httplib.py")

j = { "args": { "assignment": "1", "course": "networking" }, "headers": { "assignment": "1"}, "url": "http://httpbin.org/get?course=networking&assignment=1"
}

##HTTP LIB

def get(link,fname):
    url = str(link).replace('and', '&')
    host = str(link).split("/", 3)[2]
    aqp = str(url).split("/", 3)
    queryParam = aqp[3]
    if (fname):
        request = "GET /" + str(queryParam) + " HTTP/1.0\r\nHost: " + str(host) +"\r\nFile: " + fname  + "\r\n\r\n"
    else:
        request = "GET /" + str(queryParam) + " HTTP/1.0\r\nHost: " + str(host) + "\r\n\r\n"
    request = str.encode(request)
    return run_client(host,request)


def post(link, data):
    jstring = str(data)
    contentLen = len(jstring)
    url = str(link).replace('and', '&')
    host = str(link).split("/", 3)[2]
    aqp = str(url).split("/", 3)
    queryParam = aqp[3]

    # if (args.h):
    #     request = "POST /" + str(queryParam) + " HTTP/1.0\r\nHost: " + str(
    #         host) + "\r\n"+ args.h + "\r\nContent-Length:" + str(
    #         contentLen) + "\r\n\r\n" + "\r\nContent-Length:" +jstring
    # else:
    #     request = "POST /" + str(queryParam) + " HTTP/1.0\r\nHost: " + str(
    #         host) + "\r\nContent-Length:" + str(contentLen) + "\r\n" + jstring + "\r\n"

    if (args.pf):
        request = "POST /" + str(queryParam) + " HTTP/1.0\r\nHost: " + str(
            host) +  "\r\nFile:"+ str(args.pf)+ "\r\nData:"+ str(args.d) + "\r\n"

    request = str.encode(request)
    run_client(host, request)


def run_client(host,request):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    conn.connect((str(host), 8007))
    print(str(request))
    conn.send(request)
    data = conn.recv(1000)


    while (len(data) > 0):

        if args.v == True:
            content = data.decode('utf-8')
            sys.stdout.write("Replied: {" + content)
        else:
            content = data.decode('utf-8')
            print(content)

        data = conn.recv(1000)





parser = argparse.ArgumentParser()


parser.add_argument("--getPost", help="GET or POST request", default="localhost")
parser.add_argument("--url", help="url of server",  default="localhost")
parser.add_argument("--out", help="output to txt file", default= False)
parser.add_argument("--v", help="verbose", default= False)
parser.add_argument("--h", help="include/post header content", default= False)
parser.add_argument("--d", help="inline data", default= False)
parser.add_argument("--f", help="inline file", default= False)
parser.add_argument("--pf", help="file to post", default= False)
parser.add_argument("--fn", help="file name to get", default= False)
parser.add_argument("--help1", help="help information", default= 'def')
args = parser.parse_args()


# PARSE GET REQUEST

if args.help1=='get':
    sys.stdout.write("httpc help get usage: httpc get [-v] [-h key:value] URL\r\n Get executes a HTTP GET request for a given URL.\r\n-v Prints the detail of the response such as protocol, status,and headers.\r\n-h key:value Associates headers to HTTP Request with the format'key:value\r\n'")

if args.help1 == 'help':
    sys.stdout.write("httpc is a curl-like application but supports HTTP protocol only.\r\nUsage:\r\nhttpc command [arguments]\r\nThe commands are: \r\nget executes a HTTP GET request and prints the response.\r\npost executes a HTTP POST request and prints the response.\r\nhelp prints this screen.\r\nUse 'httpc help [command]' for more information about a command.\r\n")

if args.help1 == 'post':
    sys.stdout.write("usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\r\nPost executes a HTTP POST request for a given URL with inline data or from file.\r\n -v Prints the detail of the response such as protocol, status,and headers.\r\n-h key:value Associates headers to HTTP Request with the format'key:value'.\r\n-d string Associates an inline data to the body HTTP POST request.\r\n -f file Associates the content of a file to the body HTTP POST request.\r\nEither [-d] or [-f] can be used but not both.\r\n")

if args.getPost == 'get':
    get(args.url,args.fn)


if args.getPost == 'post':
   post(args.url,args.d)

# if args.getPost == 'post' and args.d:
#    post(args.url,args.d)

# if args.getPost == 'post' and args.f:
#     with open(args.f) as f:
#         fdata = f.read()
#     post(args.url,fdata)

# if args.getPost == 'get' and args.out:
#     with open(args.out,'w') as w:
#         w.write(get(args.url,args.fn))



