import os


def check_api_key(request) -> tuple[bool, str]:
    api_key = os.getenv("API_KEY")
    if not api_key:
        return True, ""

    provided_key = request.headers.get("x-api-key", "")
    if provided_key != api_key:
        return False, "Invalid or missing X-API-Key header"
    return True, ""
