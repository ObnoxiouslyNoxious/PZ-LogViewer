import os
import json
import glob
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

LOGS_DIR = config.get("logsDir", "")
HOST = config.get("host", "127.0.0.1")
PORT = config.get("port", 8080)
START_TIME = int(time.time())


def find_newest_log(pattern):
    matches = glob.glob(os.path.join(LOGS_DIR, pattern))
    if not matches:
        return None
    return max(matches, key=os.path.getmtime)


def get_file_info(filepath):
    if filepath is None or not os.path.exists(filepath):
        return {"path": None, "name": "No log found", "modified": None}
    mtime = os.path.getmtime(filepath)
    return {
        "path": filepath,
        "name": os.path.basename(filepath),
        "modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
    }


class LogHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._serve_html()
        elif self.path == "/api/logs":
            self._serve_log_info()
        elif self.path == "/api/log/client":
            self._serve_log_content("client")
        elif self.path == "/api/log/server":
            self._serve_log_content("server")
        elif self.path == "/api/stop":
            self._stop_server()
        else:
            self.send_error(404)

    def _serve_html(self):
        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        body = content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(body)

    def _serve_log_info(self):
        client = find_newest_log("*_DebugLog.txt")
        server = find_newest_log("*_DebugLog-server.txt")
        data = json.dumps({
            "client": get_file_info(client),
            "server": get_file_info(server),
        }).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(data)

    def _serve_log_content(self, log_type):
        if log_type == "client":
            filepath = find_newest_log("*_DebugLog.txt")
        else:
            filepath = find_newest_log("*_DebugLog-server.txt")

        if filepath is None or not os.path.exists(filepath):
            data = b'{"content":""}'
        else:
            try:
                with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                data = json.dumps({"content": content}).encode("utf-8")
            except Exception as e:
                data = json.dumps({"error": str(e)}).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass

    def _stop_server(self):
        data = b'{"status":"stopping"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        os._exit(0)


if __name__ == "__main__":
    print(f"Log Viewer running at http://{HOST}:{PORT}")
    print(f"Watching: {LOGS_DIR}")
    print("Use the STOP LOGGING button in the browser to shut down.")
    server = HTTPServer((HOST, PORT), LogHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()
