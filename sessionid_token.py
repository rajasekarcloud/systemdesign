from flask import Flask, request, make_response, redirect, url_for
import os
import uuid
import hmac
import binascii
import time

app = Flask(__name__)

# --- "Database" ---
USERS = {
    "alice": {"id": "u1", "password": "welcome"},
    "bob":   {"id": "u2", "password": "welcome"},
}

# Server-side session store: session_id -> {user_id, username, token, created_at}
SESSIONS = {}
SESSION_LIFETIME = 60 * 1


def validate_password(username: str, password: str) -> bool:
    """
    Checks a submitted username/password against the USERS store.
    """
    user = USERS.get(username)
    if user is None:
        hmac.compare_digest("x", password)  # dummy compare, timing consistency
        return False
    return hmac.compare_digest(user["password"], password)


def validate_session(session_id: str, session_token: str) -> dict | None:
    """
    Checks that a session_id exists, hasn't expired, and the token matches.
    Returns the session dict if valid, otherwise None.
    """
    session = SESSIONS.get(session_id)
    if session is None:
        return None

    if time.time() - session["created_at"] > SESSION_LIFETIME:
        del SESSIONS[session_id]
        return None

    if not hmac.compare_digest(session["token"], session_token or ""):
        return None

    return session


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
            <form method="post">
                Username: <input name="username"><br>
                Password: <input name="password" type="password"><br>
                <button type="submit">Log in</button>
            </form>
        """

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if not validate_password(username, password):
        return "Invalid username or password", 401

    user = USERS[username]
    session_id = uuid.uuid4().hex
    session_token = binascii.hexlify(os.urandom(32)).decode()

    SESSIONS[session_id] = {
        "user_id": user["id"],
        "username": username,
        "token": session_token,
        "created_at": time.time(),
    }

    resp = make_response(redirect(url_for("welcome", username=username)))
    resp.set_cookie("session_id", session_id, httponly=True, samesite="Lax")
    resp.set_cookie("session_token", session_token, httponly=True, samesite="Lax")
    return resp

@app.route("/view/<sessionid>")
def view_session(sessionid):
    return SESSIONS[sessionid]

@app.route("/welcome/<username>")
def welcome(username):
    session_id = request.cookies.get("session_id")
    session_token = request.cookies.get("session_token")

    session = validate_session(session_id, session_token)
    if session is None:
        return "Invalid or expired session. Please /login again.", 403

    # Make sure the session actually belongs to the username in the URL,
    # not just any valid session (otherwise alice could view /welcome/bob).
    if session["username"] != username:
        return "You are not authorized to view this page.", 403

    return f"Welcome, {session['username']}! (session_id: {session_id})"


@app.route("/")
def home():
    session_id = request.cookies.get("session_id")
    session_token = request.cookies.get("session_token")

    session = validate_session(session_id, session_token)
    if session is None:
        return "Not logged in (no valid session). Go to /login"

    return f"Logged in as {session['username']} (id: {session['user_id']}, session_id: {session_id})"


@app.route("/logout")
def logout():
    session_id = request.cookies.get("session_id")
    SESSIONS.pop(session_id, None)
    resp = make_response("Logged out")
    resp.delete_cookie("session_id")
    resp.delete_cookie("session_token")
    return resp


if __name__ == "__main__":
    app.run(debug=True)
