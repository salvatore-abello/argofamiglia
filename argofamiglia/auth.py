import requests
import secrets
import inspect
import base64
import re

from hashlib import sha256
from .CONSTANTS import *

CHALLENGE_URL = "https://auth.portaleargo.it/oauth2/auth"
LOGIN_URL = "https://www.portaleargo.it/auth/sso/login"
TOKEN_URL = "https://auth.portaleargo.it/oauth2/token"
REDIRECT_URI = "it.argosoft.didup.famiglia.new://login-callback"

CLIENT_ID = "72fd6dea-d0ab-4bb9-8eaa-3ac24c84886c"

def logout():
    raise NotImplementedError(f"The function {inspect.getframeinfo(inspect.currentframe()).function} hasn't been implemented yet")

def refresh(refresh_token: str) -> dict:
    NotImplementedError(f"The function {inspect.getframeinfo(inspect.currentframe()).function} hasn't been implemented yet")
    return requests.post(TOKEN_URL,
                         headers={
                             "Accept": "Application/json",
                             "Content-Type": "application/x-www-form-urlencoded"
                         },
                         data={
                             "refresh_token": refresh_token,
                             "grant_type": "refresh_token",
                             "scope": "openid offline profile user.roles argo",
                             "redirect_uri": REDIRECT_URI,
                             "client_id": CLIENT_ID
                         }
                         ).json()


def codeChallengeLogin(school: str, username: str, password: str) -> tuple:
    CHALLENGE_RE = re.compile("login_challenge=([0-9a-f]+)&?")
    CODE_RE = re.compile("code=([0-9a-zA-Z-_.]+)&?")

    CODE_VERIFIER = secrets.token_hex(64)
    CODE_CHALLENGE = base64.urlsafe_b64encode(
        sha256(
            CODE_VERIFIER.encode()
        ).digest()
    ).replace(b"+", b"-").replace(b"/", b"_").replace(b"=", b"").decode()

    params = {
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "response_type": "code",
        "prompt": "login",
        "state": secrets.token_urlsafe(32),
        "scope": "openid offline profile user.roles argo",
        "code_challenge": CODE_CHALLENGE,
        "code_challenge_method": "S256"
    }

    session = requests.Session()

    request = session.get(CHALLENGE_URL, params=params)
    login_challenge = CHALLENGE_RE.search(request.url).group(1)

    login_data = {
        "challenge": login_challenge,
        "client_id": CLIENT_ID,
        "prefill": "true",
        "famiglia_customer_code": school,
        "username": username,
        "password": password,
        "login": "true"
    }

    request = session.post(LOGIN_URL, data=login_data, allow_redirects=False)
    if "Location" not in request.headers:
        raise ValueError("Wrong credentials")

    while not (code_group := CODE_RE.search(request.headers["Location"])):
        request = session.get(request.headers["Location"], allow_redirects=False)
    code = code_group.group(1)

    token_request_data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code_verifier": CODE_VERIFIER,
        "client_id": CLIENT_ID
    }

    tokens = session.post(TOKEN_URL, data=token_request_data).json()

    login_headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "Application/json",
        "Authorization": "Bearer " + tokens["access_token"],
        "Accept": "Application/json",
    }

    json = {
        "clientID": secrets.token_urlsafe(64),
        "lista-x-auth-token": "[]",
        "x-auth-token-corrente": "null",
        "lista-opzioni-notifiche": "{}"
    }

    return requests.post(ENDPOINT + "login", headers=login_headers, json=json).json()["data"][0]["token"], tokens
