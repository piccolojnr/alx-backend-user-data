#!/usr/bin/env python3
"""
Main file
"""

import requests


def register_user(email: str, password: str) -> None:
    """_summary_"""
    r = requests.post(
        "http://localhost:5000/users",
        data={
            "email": email,
            "password": password,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("email") == email
    assert data.get("message") == "user created"


def log_in_wrong_password(email: str, password: str) -> None:
    """_summary_"""
    r = requests.post(
        "http://localhost:5000/sessions",
        data={
            "email": email,
            "password": password,
        },
    )
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """_summary_"""
    r = requests.post(
        "http://localhost:5000/sessions",
        data={
            "email": email,
            "password": password,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("email") == email
    assert data.get("message") == "logged in"
    return r.headers.get("Set-Cookie").split(";")[0].split("=")[1]


def profile_unlogged() -> None:
    """_summary_"""
    r = requests.get("http://localhost:5000/profile")
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """_summary_"""
    r = requests.get(
        "http://localhost:5000/profile", cookies={"session_id": session_id}
    )
    assert r.status_code == 200
    data = r.json()


def log_out(session_id: str) -> None:
    """_summary_"""
    r = requests.delete(
        "http://localhost:5000/session", data={"session_id": session_id}
    )
    assert r.status_code == 200


def reset_password_token(email: str) -> str:
    """_summary_"""
    r = requests.post(
        "http://localhost:5000/reset_password",
        data={"email": email},
    )
    assert r.status_code == 200
    return r.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """_summary_"""
    r = requests.put(
        "http://localhost:5000/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password,
        },
    )
    assert r.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
