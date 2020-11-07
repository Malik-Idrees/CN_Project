# CN_Project
Group Members:
[Bilal Waheed](https://github.com/bilalwaheed099/)
[Malik Idrees](https://github.com/Malik-Idrees/)

python virtual multiserver downloader where a number of virtual servers are created and a file is downloaded simultaneously from all of them<br/>
To test run it store a video.mp4 file in root directory and use commands given below<br/>
-n : No of virtual servers<br/>
-p : ports on which the server will run<br/>
-i : intervals after which status is updated(Only for client though)<br/>
-f : a path to input file relative/absolute<br/>
-a : server's IP address<br/>
-o : output path where output will be stored with a file extension e.g ..\..\\outputvideo.mp4 <br/>
although -a receives IP address but SERVER is set to work on localhost<br/>
# Run server 
```shell
python server.py -n 4  -p 10002 10003 10004 10005 -i 2 -f video.mp4
```
# Run client
```shell
python client.py -a 192.168.1.1  -p 10002 10003 10004 10005 -i 2 -o outputvideo.mp4
```
# future changes that you could add
server crash handling and load distribution if particular server is unavailable.
with current setup each server that client wants to connect should be running.
