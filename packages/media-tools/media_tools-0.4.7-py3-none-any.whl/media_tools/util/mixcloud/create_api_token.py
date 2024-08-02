__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import sys
import threading
import webbrowser
from argparse import Namespace
from functools import partial
from time import sleep
from typing import Dict, Optional, Type
from urllib.parse import urlencode

from media_tools.util.mixcloud.constants import ACCESS_TOKEN_FILE
from media_tools.util.mixcloud.oauth_parameter_receiver import (
    OAuthCodeReceiver, OAuthTokenReceiver, run_local_server
)

MIXCLOUD_URL = 'https://www.mixcloud.com'
REGISTER_APP_URL = f'{MIXCLOUD_URL}/developers/create'
REQUEST_OAUTH_CODE_URL = f'{MIXCLOUD_URL}/oauth/authorize'
REQUEST_TOKEN_URL = f'{MIXCLOUD_URL}/oauth/access_token'


class CreateAPIToken:

    help_text: Optional[str] = None

    def __repr__(self):
        return str(vars(self))

    def pre_run(self):
        print(self.help_text)

    def run(self):
        raise NotImplementedError()

    def post_run(self):
        raise NotImplementedError()

    @classmethod
    def create(cls, opts: Namespace):
        if opts.create_app:
            return Step1()
        if opts.create_code:
            return Step2(opts.client_id)
        if opts.create_token:
            return Step3(opts.client_id, opts.client_secret, opts.oauth_code)
        return Help()


class Help:
    help_text = """
Creating an authentication token for the Mixcloud API takes three steps.

Step 1: Create a Mixcloud app
Before you start this step, ensure that you are logged in to Mixcloud on your
system browser, because you need to fill in the form that is going to open in
your browser.
Then enter:
    mixcloud create-auth --create-app
A window will open in your browser. Follow the instructions printed in your
terminal - click on the app name in the browser and copy the client ID for steps
2 and 3 and the client secret for step 3.

Step 2: Create OAuth token
Use the client ID and secret from step 1 to run
    mixcloud create-auth --create-code --client-id CLIENT_ID
Again a browser window will open with a page displaying an "Authorize" button.
Click it and you will be taken to a page displaying a so-called OAuth code.
Copy the code to use it in step 3.

Step 3: Create the Mixcloud API token
Use the code from step 2 to run
    mixcloud create-auth --create-token --client-id CLIENT_ID \\
                                        --client-secret CLIENT_SECRET \\
                                        --oauth-code OAUTH_CODE
This will open yet another browser window showing you a token (in JSON format).
Copy only the string inside the quotes to use as token - either directly (here
called <TOKEN>) or written (without any extra spaces or newlines) to a file
(here called <TOKEN_FILE>).

Afterwards you can use the generated token to upload mixes to Mixcloud with:
    mixcloud upload --auth-token-string <TOKEN> ...
    mixcloud upload --auth-token-file <TOKEN_FILE> ...
If you store this access token as ".mixcloud_access_token" in either the current
directory, your user's $HOME directory or under $HOME/.config/media-tools, that
token will be used without specifying --auth-token-string or --auth-token-file.
        """

    def run(self):
        print(self.help_text)
        sys.exit(1)


class Step1(CreateAPIToken):

    help_text = """
Please fill in the "Create new app" form opening in your browser.

Please note that you have to be logged in to Mixcloud for the form to work. If
you are not logged in, the "Create" button will be deactivated.

After successfully registering your app it will appear in the "Registered
Applications" section at the top of the page.

Clicking on the app link leads to a page on which you can find the client ID
and the client secret. These will be necessary for the next step.
"""

    def run(self):
        self.pre_run()
        webbrowser.open_new_tab(REGISTER_APP_URL)
        self.post_run()

    def post_run(self):
        pass


class ReceivesResponseViaRedirect(CreateAPIToken):

    request_url: Optional[str] = None
    capture_class: Optional[Type] = None

    def run(self):
        self.pre_run()
        http_server_thread = threading.Thread(
            target=partial(
                run_local_server, capture_class=self.capture_class,
                server_port=self.get_server_port(), create_token=self
            )
        )
        http_server_thread.start()
        sleep(0.1)
        uri = self.get_url()
        webbrowser.open_new_tab(uri)
        http_server_thread.join()
        self.post_run()

    def post_run(self):
        raise NotImplementedError()

    @staticmethod
    def get_server_port() -> int:
        return 8888

    def request_params(self):
        raise NotImplementedError()

    def get_url(self) -> str:
        return f'{self.request_url}?{urlencode(self.request_params())}'

    def local_server(self):
        return f'http://localhost:{self.get_server_port()}'


class Step2(ReceivesResponseViaRedirect):

    request_url = REQUEST_OAUTH_CODE_URL
    capture_class = OAuthCodeReceiver
    help_text = """
Please click the "Authorize" button on the page opening in your browser.
"""

    def __init__(self, client_id: str) -> None:
        self.client_id = client_id
        self.oauth_code: Optional[str] = None

    def set_oauth_code(self, code: str) -> None:
        self.oauth_code = code

    def post_run(self):
        print(f"""
Your OAuth code is {self.oauth_code}. Now start
$ mixcloud create-auth --create-token \
    --client-id {self.client_id} --client-secret <YOUR CLIENT SECRET> \
    --oauth-code {self.oauth_code}
        """)

    def request_params(self) -> Dict[str, str]:
        return {
            'client_id': self.client_id,
            'redirect_uri': self.local_server()
        }


class Step3(ReceivesResponseViaRedirect):

    request_url = REQUEST_TOKEN_URL
    capture_class = OAuthTokenReceiver

    def __init__(self, client_id: str, client_secret: str, oauth_code: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_code = oauth_code
        self.token: Optional[str] = None

    def post_run(self):
        print(f"""
Your Mixcloud authorization token is {self.token}. It has been written to the
file ./{ACCESS_TOKEN_FILE}. You can leave it there, or move it to
~/{ACCESS_TOKEN_FILE} or ~/.config/{ACCESS_TOKEN_FILE}.
        """)

    def request_params(self):
        return {
            'client_id': self.client_id,
            'redirect_uri': self.local_server(),
            'client_secret': self.client_secret,
            'code': self.oauth_code
        }
