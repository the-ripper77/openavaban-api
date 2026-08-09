import os
import base64
import json
import mimetypes
import requests
from typing import Union


def _extract_api_key(token: str) -> str:
    token = token.strip().strip("'\"")
    if token.startswith("eyJ"):
        try:
            padded = token + "=" * (4 - len(token) % 4)
            decoded = json.loads(base64.b64decode(padded).decode("utf-8"))
            return decoded.get("apiKey", token)
        except Exception:
            pass
    return token


class UploadThingClient:
    def __init__(self):
        self.token = os.getenv("UPLOADTHING_TOKEN", "")
        if not self.token:
            raise ValueError("UPLOADTHING_TOKEN must be set")
        self.api_key = _extract_api_key(self.token)

    def upload(self, file_data: bytes, file_name: str, file_type: str) -> dict:
        file_size = len(file_data)

        prep_resp = requests.post(
            "https://api.uploadthing.com/v7/prepareUpload",
            json={
                "fileName": file_name,
                "fileType": file_type,
                "fileSize": file_size,
                "acl": "public-read",
            },
            headers={
                "x-uploadthing-api-key": self.api_key,
                "x-uploadthing-version": "7.4.0",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        prep_resp.raise_for_status()
        data = prep_resp.json()

        if isinstance(data, dict):
            upload_url = data.get("url") or data.get("presignedUrl")
            file_key = data.get("key", "")
        elif isinstance(data, list) and data:
            upload_url = data[0].get("url") or data[0].get("presignedUrl")
            file_key = data[0].get("key", "")
        else:
            raise Exception(f"Unexpected prepareUpload response: {data}")

        if not upload_url:
            raise Exception(f"No upload URL in response: {data}")

        up_resp = requests.put(
            upload_url,
            files={"file": (file_name, file_data, file_type)},
            timeout=120,
        )

        if up_resp.status_code not in (200, 201, 204):
            raise Exception(f"Upload failed ({up_resp.status_code}): {up_resp.text[:400]}")

        public_url = f"https://utfs.io/f/{file_key}"

        return {
            "url": public_url,
            "key": file_key,
            "name": file_name,
            "size": file_size,
            "type": file_type,
        }

    def delete(self, file_key: str):
        resp = requests.post(
            "https://api.uploadthing.com/v6/deleteFiles",
            json={"fileKeys": [file_key]},
            headers={
                "x-uploadthing-api-key": self.api_key,
                "x-uploadthing-version": "6.4.0",
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        resp.raise_for_status()

    def list_files(self, limit: int = 500, offset: int = 0) -> list:
        resp = requests.post(
            "https://api.uploadthing.com/v6/listFiles",
            json={"limit": limit, "offset": offset},
            headers={
                "x-uploadthing-api-key": self.api_key,
                "x-uploadthing-version": "6.4.0",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json().get("files", [])
