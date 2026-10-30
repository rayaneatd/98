from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_ANON_KEY

_client: Client | None = None


def get_supabase_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return _client


def sign_in(email: str, password: str) -> dict:
    client = get_supabase_client()
    try:
        response = client.auth.sign_in_with_password({
            "email": email.strip(),
            "password": password,
        })
        user = response.user
        metadata = user.user_metadata or {}
        name = metadata.get("full_name") or email.split("@")[0].capitalize()
        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": name,
            },
        }
    except Exception as exc:
        err_msg = str(exc)
        if "Invalid login credentials" in err_msg:
            err_msg = "Invalid email or password."
        return {"success": False, "error": err_msg}


def sign_up(email: str, password: str, full_name: str | None = None) -> dict:
    client = get_supabase_client()
    try:
        options = {}
        if full_name:
            options["data"] = {"full_name": full_name.strip()}

        response = client.auth.sign_up({
            "email": email.strip(),
            "password": password,
            "options": options,
        })
        user = response.user
        if not user:
            return {"success": False, "error": "Could not create account."}

        name = full_name or email.split("@")[0].capitalize()
        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": name,
            },
        }
    except Exception as exc:
        err_msg = str(exc)
        if "already registered" in err_msg.lower():
            err_msg = "An account with this email already exists."
        elif "password should be" in err_msg.lower():
            err_msg = "Password should be at least 6 characters."
        return {"success": False, "error": err_msg}


def sign_out() -> None:
    client = get_supabase_client()
    try:
        client.auth.sign_out()
    except Exception:
        pass
