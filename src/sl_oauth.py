from obs_logging import *
import http.server
import socketserver
import urllib.parse
import threading
import webbrowser
import sl_token as sl_token

OAUTH_PORT = 8080


class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_components = urllib.parse.parse_qs(parsed_url.query)

        if "code" in query_components:
            auth_code = query_components["code"][0]
            log_info("Received auth code.")
            token = sl_token.request_token(auth_code)

            if token:
                log_info("Access token obtained.")
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"Authentication successful! You can close this window.")
            else:
                log_error("Token exchange failed.")
                self.send_error(400, "Token exchange failed.")
        else:
            self.send_error("Missing code parameter.")

    def log_message(self, format, *args):
        return  # Suppress default logging


def start_oauth_server():
    with socketserver.TCPServer(("", OAUTH_PORT), OAuthHandler) as httpd:
        try:
            log_info(f"OAuth server started at http://localhost:{OAUTH_PORT}")
            httpd.handle_request()
        except Exception as e:
            log_error(f"OAuth server error: {e}")
        finally:
            httpd.server_close()
            log_info("OAuth server closed.")


def initiate_oauth_flow(_, __):
    auth_url = (
        f"https://streamlabs.com/api/v2.0/authorize"
        f"?client_id={sl_token.CLIENT_ID}"
        f"&redirect_uri={urllib.parse.quote(sl_token.REDIRECT_URI)}"
        f"&response_type=code"
        f"&scope={sl_token.SCOPE}"
    )

    oauth_thread = threading.Thread(target=start_oauth_server, daemon=True)
    oauth_thread.start()

    log_info(f"Visiting OAuth at {auth_url}")
    webbrowser.open(auth_url)
