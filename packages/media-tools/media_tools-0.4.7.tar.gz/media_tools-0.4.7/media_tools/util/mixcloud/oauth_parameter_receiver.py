__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional, Tuple, Type
from urllib.parse import urlparse


class ReceivedCode(BaseException):
    def __init__(self, code: str) -> None:
        logging.info(code)
        self.code = code
        super().__init__()


class OAuthParameterReceiver(BaseHTTPRequestHandler):

    parameter: Optional[str] = None

    def do_GET(self):  # pylint: disable=invalid-name
        request_query = urlparse(self.path).query
        if self.parameter not in request_query:
            # probably trying to GET /favicon.ico
            return

        key_value: Tuple[str, str] = tuple(request_query.split('=', 1))
        try:
            params = dict([key_value])
            self.write_response(200, f'{self.parameter} received', request_query, 'OK, thanks!')
            raise ReceivedCode(params[self.parameter])
        except (KeyError, ValueError):
            logging.warning("could not parse %s from request path '%s'", self.parameter, self.path)
            return

    def write_response(self, status: int, title: str, request_query: str, message: str) -> None:
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(
            bytes(f"""
    <html>
      <head><title>{title}</title></head>
      <body><p>{request_query}</p><p>{message}</p></body>
    </html>
    """, 'utf-8')
        )


class OAuthCodeReceiver(OAuthParameterReceiver):
    """
    When registering an app with the Mixcloud API to receive a token, the API
    requires a redirect URL for a callback:
    `https://www.mixcloud.com/oauth/authorize?client_id=YOUR_CLIENT_ID
                                             &redirect_uri=YOUR_REDIRECT_URI`
     This URL is then called in the form
     `YOUR_REDIRECT_URI?code=OAUTH_CODE`
     This class starts a local HTTP server to catch the callback and extract
     the `code` parameter as the OAuth code.
    """
    parameter = 'code'


class OAuthTokenReceiver(BaseHTTPRequestHandler):
    """
    When registering an app with the Mixcloud API to receive a token, the API
    requires a redirect URL for a callback:
    `https://www.mixcloud.com/oauth/access_token?client_id=YOUR_CLIENT_ID
                                                &client_secret=YOUR_CLIENT_SECRET
                                                &code=OAUTH_CODE
                                                &redirect_uri=YOUR_REDIRECT_URI`
     This URL is then called in the form
     `YOUR_REDIRECT_URI?access_token=ACCESS_TOKEN`
     This class starts a local HTTP server to catch the callback and extract
     the `access_token` parameter as the OAuth code.
    """
    parameter = 'access_token'


def run_local_server(server_port: int, capture_class: Type, create_token) -> None:

    host_name = 'localhost'
    web_server = HTTPServer((host_name, server_port), capture_class)
    logging.info('Server started http://%s:%s', host_name, server_port)

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        logging.warning('Interrupted manually')
    except ReceivedCode as received:
        logging.info('Received code %s', received.code)
        create_token.set_oauth_code(received.code)
    except KeyError as error:
        logging.error('mismatched response (%s)', error)
    finally:
        web_server.server_close()

    logging.info('Server stopped.')
