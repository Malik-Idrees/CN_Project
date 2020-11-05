# CN_Project
python virtual multiserver downloader where a number of virtual servers are created and a file is downloaded simultaneously from all of them
To test run it store a video.mp4 file in root directory and use commands given below
-n : No of virtual servers
-p : ports on which the server will run
-i : intervals after which status is updated(Only for client though)
-f : a path to input file relative/absolute
-a : server's IP address
-o : output path where output will be stored with a file extension e.g ..\..\\outputvideo.mp4
although -a receives IP address but SERVER is set to work on localhost
# Run server 
python server.py -n 4  -p 10002 10003 10004 10005 -i 2 -f video.mp4
# Run client
python client.py -a 192.168.1.1  -p 10002 10003 10004 10005 -i 2 -o outputvideo.mp4
# future changes that you could add
server crash handling and load distribution if particular server is unavailable.
with current setup each server that client wants to connect should be running.
