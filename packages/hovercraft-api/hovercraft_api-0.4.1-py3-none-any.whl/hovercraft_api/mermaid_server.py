# mermaid_server.py

import http.server
import socketserver
import webbrowser
import os
from loguru import logger

class MermaidServer:
    def __init__(self, directory, file_to_open, port=8000):
        self.directory = directory
        self.file_to_open = file_to_open
        self.port = port

    def start(self):
        """
        指定されたディレクトリでHTTPサーバーを起動し、指定されたファイルをデフォルトブラウザで開く
        """
        logger.info(f"ポート{self.port}でHTTPサーバーを起動します")
        os.chdir(self.directory)
        
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            url = f"http://localhost:{self.port}/{self.file_to_open}"
            logger.info(f"サーバーが起動しました。{url} を開いています")
            webbrowser.open(url)
            logger.info("Ctrl+Cで終了します")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                logger.info("サーバーを終了します")

def main():
    server = MermaidServer('example2/hovercraft_assets', 'index_with_svg.html')
    server.start()

if __name__ == "__main__":
    main()
