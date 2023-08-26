import os

SCOPES = ['https://www.googleapis.com/auth/drive']
DIRECTORY_ID = os.getenv("GOOGLE_DIRECTORY_ID", "")
GOOGLE_CONFIG = {
    "installed": {
        "client_id": os.getenv("GOOGLE_API_CLIENT_ID"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": os.getenv("GOOGLE_API_CLIENT_SECRET"),
        "refresh_token": "",
        "redirect_uris": [
            "http://localhost"
        ]
    }
}


