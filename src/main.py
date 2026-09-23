from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

CONTACTS_FILE = (
    Path(__file__).resolve().parent.parent / "html" / "prototype4.html"
)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/prototype4":
            self.send_error(404, "Страница не найдена")
            return

        with CONTACTS_FILE.open("r", encoding="utf-8") as file:
            page = file.read().encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self) -> None:
        if self.path != "/prototype4":
            self.send_error(404, "Страница не найдена")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(body)
        print("Получены данные формы:", form_data)
        self.do_GET()


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), RequestHandler)
    print("Сервер запущен: http://localhost:8000/prototype4")
    server.serve_forever()