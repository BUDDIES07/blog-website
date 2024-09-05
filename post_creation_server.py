from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import cgi

POSTS_FILE = 'post.json'
UPLOAD_DIR = 'uploads'

class RequestHandler(SimpleHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_GET(self):
        if self.path == '/posts':
            self.handle_get_posts()
        else:
            super().do_GET()

    def handle_get_posts(self):
        print("GET request for /posts")
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, 'r') as file:
                posts = json.load(file)
        else:
            posts = []

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(posts, indent=4).encode())
        print("Sent posts")

    def do_POST(self):
        if self.path == '/posts':
            self.handle_post_request()
        else:
            super().do_POST()

    def handle_post_request(self):
        print("Received POST request to /posts")
        content_type = self.headers.get('Content-Type')
        print(f"Content-Type: {content_type}")

        if content_type == 'application/json':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                post_data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Invalid JSON."}).encode())
                return

            title = post_data.get('title')
            author = post_data.get('author')
            content = post_data.get('content')
            image_url = post_data.get('image')  # Assuming image URL for simplicity

            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"Content: {content}")
            print(f"Image URL: {image_url}")

            if title and author and content:
                new_post = {
                    'title': title,
                    'author': author,
                    'content': content,
                }

                if image_url:
                    new_post['image'] = image_url

                # Append to existing posts
                if os.path.exists(POSTS_FILE):
                    with open(POSTS_FILE, 'r') as file:
                        posts = json.load(file)
                else:
                    posts = []

                posts.append(new_post)

                # Save updated posts
                with open(POSTS_FILE, 'w') as file:
                    json.dump(posts, file, indent=4)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Post created successfully!"}).encode())
                print("Post created successfully")
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Invalid post data."}).encode())
                print("Invalid post data")
        else:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Unsupported Media Type."}).encode())
            print("Unsupported Media Type")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=2000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
