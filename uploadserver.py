from flask import Flask, request
from werkzeug.datastructures import FileStorage
from werkzeug.formparser import parse_form_data
import os
import argparse
import netifaces as ni
import logging

# ANSI escape codes for colored text and styles
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Suppress the development server warning
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Flask Upload Server')
parser.add_argument('-o', '--upload-folder', type=str, default='uploads',
                    help='The path where uploaded files will be stored (default: uploads)')
parser.add_argument('-i', '--interface', type=str, default='eth0',
                    help='Network interface to run the server on (default: eth0)')
parser.add_argument('-p', '--port', type=int, default=80,
                    help='Port number to run the server on (default: 80)')
args = parser.parse_args()

UPLOAD_FOLDER = args.upload_folder
INTERFACE = args.interface
PORT = args.port

try:
    IP_ADDRESS = ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr']
except ValueError:
    print(f"Error: Interface {INTERFACE} not found.")
    exit(1)

app = Flask(__name__)

@app.route('/upload/<filename>', methods=['POST'])
def upload_file(filename):
    environ = request.environ.copy()
    environ['wsgi.input'] = request.stream
    environ['CONTENT_LENGTH'] = int(request.headers['Content-Length'])
    streams, fields, files = parse_form_data(environ)

    file = files['file']

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return 'File uploaded successfully'

if __name__ == '__main__':
    print(f"{GREEN}Server running on {IP_ADDRESS}:{PORT} (interface: {INTERFACE}){RESET}")
    print(f"\n{YELLOW}{BOLD}To upload a file from Linux:{RESET}")
    print(f"{BOLD}curl -F \"file=@myfile.txt\" http://{IP_ADDRESS}:{PORT}/upload/myfile.txt{RESET}")
    print(f"\n{YELLOW}{BOLD}To upload a file from Windows:{RESET}")
    print(f"{BOLD}iwr -Uri \"http://{IP_ADDRESS}:{PORT}/upload/myfile.txt\" -Method Post -Infile \"myfile.txt\"\n{RESET}")
    app.run(host=IP_ADDRESS, port=PORT)

