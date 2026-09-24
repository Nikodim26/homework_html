from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_DIR = BASE_DIR / "html"
STATIC_DIR = BASE_DIR / "static"

class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/contacts":
            contacts_file = HTML_DIR / "contacts.html"
            if not contacts_file.exists():
                self.send_error(404, "Страница не найдена")
                return
            with contacts_file.open(mode="r", encoding="utf-8") as file:
                page = file.read().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/contacts":
            self.send_error(404, "Страница не найдена")
            return
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(body)
        print("Получены данные формы:", form_data)
        self.do_GET()

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), RequestHandler)
    print("Сервер запущен: http://localhost:8000/contacts")
    server.serve_forever()
