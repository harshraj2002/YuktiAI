"""
Simple HTTP server for YuktiAI web interface
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class YuktiHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="web", **kwargs)
    
    def end_headers(self):
        #Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    """Start the HTTP server"""
    
    #Check if web directory exists
    web_dir = Path("web")
    if not web_dir.exists():
        print("❌ Web directory not found!")
        print("Please ensure the 'web' directory exists with index.html")
        sys.exit(1)
    
    #Check if index.html exists
    index_file = web_dir / "index.html"
    if not index_file.exists():
        print("❌ index.html not found in web directory!")
        sys.exit(1)
    
    PORT = 8000
    
    try:
        with socketserver.TCPServer(("", PORT), YuktiHTTPRequestHandler) as httpd:
            print("🌐 YuktiAI Web Interface")
            print("=" * 50)
            print(f"✅ Server started at: http://localhost:{PORT}")
            print(f"📁 Serving files from: {web_dir.absolute()}")
            print("\n🚀 Opening YuktiAI in your browser...")
            print("💡 Make sure Ollama is running: ollama serve")
            print("\n⏹️  Press Ctrl+C to stop the server")
            
            #Open browser
            webbrowser.open(f'http://localhost:{PORT}')
            
            #Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 98:  #Port already in use
            print(f"❌ Port {PORT} is already in use!")
            print("Please stop any other servers or use a different port")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()