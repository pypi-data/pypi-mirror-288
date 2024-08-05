from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time  # 引入时间模块
import json
from config import defaultConfig
from browser import createBrowser ,browsers


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 获取内容长度
        content_length = int(self.headers['Content-Length'])
        # 读取 POST 请求的数据
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data)
        print(post_data)
        url = post_data['url']
        name = post_data['name']
        # 判断url和name是否存在
        if not url or not name:
            self.send_response(400)
            self.end_headers()
            response = 'url or name is missing'
            self.wfile.write(response.encode('utf-8')) 
            return
        if post_data['type'] == 'init':
            print('init')
            
            createBrowser(name=post_data['name'], path=post_data.get('path',''), extensions=post_data['extensions'])
            
            

        elif post_data['type'] == 'tabhandler':
            if name in browsers: 
                browser = browsers[name]
                browser.oncommand(post_data)

            else:
                print('browser not found')
             
        # 响应客户端
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers() 
        # 将接收到的数据发送回客户端
        response = 'ok'
        self.wfile.write(response.encode('utf-8'))

def startHttpServer(server_class=ThreadedHTTPServer, handler_class=SimpleHTTPRequestHandler ):
    server_address = ('', defaultConfig['httpport'])
    httpd = server_class(server_address, handler_class)
    
    print(f"Starting httpd server on port { defaultConfig['httpport']}")
    httpd.serve_forever()
