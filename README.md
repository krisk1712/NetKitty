# NetKitty
Some Netcat alternative

It is a netcat alternative with certain file features

It can execute command and smaller version of netcat 

so the execution time is less

and "Certain bugs are found will be fixed soon"

# Open Source Project Written in python2.7

# You can Use it like this with Certain examples:

     NetKitty
   
     Usage : python2.7 netkitty.py -t target_host -p port
     -l --listen                       -listen on [host]:[port] for incoming conncetion
     -e --execute=file_to_run          - execute the given file upon recv connection
     -c --command                      -init a command shell
     -u --upload=destination           - upon recv coon upload a file and write a dest
     Examples:
     python2.7 netkitty.py -t 192.168.0.1 -p 4444 -l -c
     python2.7 nettkitty.py -t 192.168.0.1 -p 4444 -l -u=c:\\target.exe
     python2.7 netkitty.py -t 192.168.0.1 -p 4444 -l -e=\"cat /etc/passwd\"
     echo 'ABCDEFGHI' | python2.7 netkitty.py -t 192.168.11.12 -p 135
