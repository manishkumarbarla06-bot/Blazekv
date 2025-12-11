"""
BlazeKV REST API Server
Professional REST API wrapper for BlazeKV

Start server:
    python blazekv_api.py

API Endpoints:
    POST   /api/v1/kv           - Set key-value
    GET    /api/v1/kv/<key>     - Get value
    DELETE /api/v1/kv/<key>     - Delete key
    GET    /api/v1/stats        - Get statistics
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
from pathlib import Path

try:
    from blazekv import BlazeKV
except ImportError:
    # Fallback if module not available
    class BlazeKV:
        def __init__(self):
            pass
        def set(self, k, v): pass
        def get(self, k): return None
        def delete(self, k): pass


class BlazeKVAPI(BaseHTTPRequestHandler):
    """HTTP request handler for BlazeKV REST API"""
    
    # Global database instance (shared across requests)
    db = None
    stats = {"requests": 0, "sets": 0, "gets": 0, "deletes": 0, "errors": 0}
    
    def do_GET(self):
        """Handle GET requests"""
        self.stats["requests"] += 1
        
        if self.path == "/api/v1/stats":
            return self._get_stats()
        elif self.path.startswith("/api/v1/kv/"):
            return self._get_key()
        elif self.path == "/health":
            return self._health_check()
        else:
            self._send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        self.stats["requests"] += 1
        
        if self.path == "/api/v1/kv":
            return self._set_key()
        else:
            self._send_error(404, "Endpoint not found")
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        self.stats["requests"] += 1
        
        if self.path.startswith("/api/v1/kv/"):
            return self._delete_key()
        else:
            self._send_error(404, "Endpoint not found")
    
    def _get_key(self):
        """GET /api/v1/kv/<key> - Retrieve a value"""
        try:
            key = urllib.parse.unquote(self.path.split("/")[-1])
            value = self.db.get(key)
            
            self.stats["gets"] += 1
            
            if value is None:
                self._send_json({"error": "Key not found"}, 404)
            else:
                self._send_json({"key": key, "value": value}, 200)
        except Exception as e:
            self.stats["errors"] += 1
            self._send_error(500, str(e))
    
    def _set_key(self):
        """POST /api/v1/kv - Set a key-value pair"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            key = data.get('key')
            value = data.get('value')
            
            if not key or value is None:
                return self._send_error(400, "Missing key or value")
            
            self.db.set(key, value)
            self.stats["sets"] += 1
            
            self._send_json({"status": "ok", "key": key}, 201)
        except json.JSONDecodeError:
            self.stats["errors"] += 1
            self._send_error(400, "Invalid JSON")
        except Exception as e:
            self.stats["errors"] += 1
            self._send_error(500, str(e))
    
    def _delete_key(self):
        """DELETE /api/v1/kv/<key> - Delete a key"""
        try:
            key = urllib.parse.unquote(self.path.split("/")[-1])
            self.db.delete(key)
            self.stats["deletes"] += 1
            
            self._send_json({"status": "ok", "key": key}, 200)
        except Exception as e:
            self.stats["errors"] += 1
            self._send_error(500, str(e))
    
    def _get_stats(self):
        """GET /api/v1/stats - Get server statistics"""
        try:
            stats = {
                "uptime": datetime.now().isoformat(),
                "total_requests": self.stats["requests"],
                "operations": {
                    "set": self.stats["sets"],
                    "get": self.stats["gets"],
                    "delete": self.stats["deletes"]
                },
                "errors": self.stats["errors"]
            }
            self._send_json(stats, 200)
        except Exception as e:
            self._send_error(500, str(e))
    
    def _health_check(self):
        """GET /health - Health check endpoint"""
        self._send_json({"status": "healthy"}, 200)
    
    def _send_json(self, data: dict, status_code: int):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        response = json.dumps(data)
        self.wfile.write(response.encode('utf-8'))
    
    def _send_error(self, status_code: int, message: str):
        """Send error response"""
        self._send_json({"error": message}, status_code)
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")


def run_server(host: str = "localhost", port: int = 8080):
    """Start the REST API server"""
    
    # Initialize database
    BlazeKVAPI.db = BlazeKV()
    BlazeKVAPI.db.load()
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, BlazeKVAPI)
    
    print(f"""
╔════════════════════════════════════╗
║     BlazeKV REST API Server        ║
╚════════════════════════════════════╝

🚀 Server running at http://{host}:{port}

📚 API Endpoints:
   POST   /api/v1/kv           - Set key-value
   GET    /api/v1/kv/<key>     - Get value
   DELETE /api/v1/kv/<key>     - Delete key
   GET    /api/v1/stats        - Statistics
   GET    /health              - Health check

📝 Example Usage:
   curl -X POST http://localhost:8080/api/v1/kv \\
     -H "Content-Type: application/json" \\
     -d '{{"key": "username", "value": "alice"}}'
   
   curl http://localhost:8080/api/v1/kv/username
   
   curl -X DELETE http://localhost:8080/api/v1/kv/username

Press Ctrl+C to stop server
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
        BlazeKVAPI.db.save()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="BlazeKV REST API Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to")
    
    args = parser.parse_args()
    run_server(args.host, args.port)
