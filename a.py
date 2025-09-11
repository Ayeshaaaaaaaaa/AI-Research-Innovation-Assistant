import os
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError

try:
    creds, project = default()
    print("✅ Logged in successfully!")
    print("Project ID:", project)
except DefaultCredentialsError:
    print("❌ No credentials found! Check your JSON path and environment variable.")
