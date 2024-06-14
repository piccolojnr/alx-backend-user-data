#!/usr/bin/env python3
"""_summary_
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """_summary_"""
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        return abort(400)

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    except Exception:
        return abort(400)


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """_summary_"""
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        return abort(400)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            # store session_id in a cookie
            cookie = request.headers.get("cookie")
            if cookie is None:
                cookie = ""
            cookie += f"session_id={session_id};"
            return (
                jsonify({"email": email, "message": "logged in"}),
                200,
                {"Set-Cookie": cookie},
            )
    return abort(401)


@app.route("/session", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """_summary_"""
    session_id = request.form.get("session_id")
    if session_id is None:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """_summary_"""
    cookie = request.headers.get("cookie")
    if cookie is None:
        return abort(403)

    for item in cookie.split(";"):
        if "session_id" in item:
            session_id = item.split("=")[1]
            break

    if session_id is None:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """_summary_"""
    email = request.form.get("email")
    if email is None:
        return abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """_summary_"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if email is None or reset_token is None or new_password is None:
        return abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return abort(403)


@app.route("/", methods=["GET"], strict_slashes=False)
def hello() -> str:
    """_summary_"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
