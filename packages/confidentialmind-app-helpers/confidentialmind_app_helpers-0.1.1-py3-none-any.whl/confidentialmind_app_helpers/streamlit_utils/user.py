from streamlit.web.server.websocket_headers import _get_websocket_headers
import jwt


def get_access_token():
    """
    Retrieve the access token from the websocket headers.

    Returns:
        str: The access token if present, otherwise None.
    """
    headers = _get_websocket_headers()
    return headers.get("X-Auth-Request-Access-Token")


def get_access_token_claims():
    """
    Decode the access token to retrieve its claims.

    Verifying of the token is handled by ConfidentialMind stack before
    the requests reaches the container.

    Returns:
        dict: A dictionary containing the decoded claims of the access token.
    """
    access_token = get_access_token()
    return jwt.decode(access_token, options={"verify_signature": False})


def get_user_emai():
    """
    Extract and return the email address from the access token claims.

    Returns:
        str: The user's email address if present in the claims, otherwise None.
    """
    return get_access_token_claims().get("email")


def get_user_id():
    """
    Extract and return the user ID (subject) from the access token claims.

    Returns:
        str: The user's ID if present in the claims, otherwise None.
    """
    return get_access_token_claims().get("sub")
