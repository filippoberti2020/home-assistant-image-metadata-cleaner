import os
import base64
from io import BytesIO
from PIL import Image
import http.server
import socketserver
import webbrowser

def remove_metadata(path):
    img = Image.open(path)
    img_data = list(img.getdata())
    img_no_exif = Image.new(img.mode, img.size)
    img_no_exif.putdata(img_data)
    img_no_exif.save(path)

def start_web_interface(port):
    Handler = http.server.SimpleHTTPRequestHandler
    class UploadHandler(Handler):
        def do_POST(self):
            if self.path == "/upload":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                length = int(self.headers["Content-Length"])
                file = self.rfile.read(length)
                img_path = "uploaded_image.jpg"
                with open(img_path, "wb") as f:
                    f.write(file)
                remove_metadata(img_path)
                self.wfile.write(base64.b64encode(open(img_path, "rb").read()))
                os.remove(img_path)
    with socketserver.TCPServer(("", port), UploadHandler) as httpd:
        print("serving at port", port)
        webbrowser.open_new("http://localhost:" + str(port))
        httpd.serve_forever()

def run(port):
    # Serve the web interface
    start_web_interface(port)

if __name__ == "__main__":
    port = 8000
    run(port)
