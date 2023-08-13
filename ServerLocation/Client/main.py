from UI import Console

UploadCapture = 'http://127.0.0.1:8001/upload/capture.jpg'
UploadTXT = 'http://127.0.0.1:8001/upload/txt.txt'
Upload100mb = 'http://127.0.0.1:8001/upload/100mb.bin'
Upload1000mb = 'http://127.0.0.1:8001/upload/1000mb.bin'

Download100mb = 'http://127.0.0.1:8001/download/100mb.bin'
Download1000mb = 'http://127.0.0.1:8001/download/1000mb.bin'
DownloadTXT = 'http://127.0.0.1:8001/download/txt.txt'
DownloadCapture = 'http://127.0.0.1:8001/download/capture.jpg'


def start_app():
    console = Console()
    console.run()


if __name__ == '__main__':
    start_app()
