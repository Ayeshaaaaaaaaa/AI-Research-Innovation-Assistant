import os

def is_utf8(file_path):
    try:
        with open(file_path, "rb") as f:
            raw = f.read()
        raw.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False

bad_files = []

for root, dirs, files in os.walk("."):
    for file in files:
        path = os.path.join(root, file)
        # Ignore virtual environment and git
        if any(skip in path for skip in [".git", "venv", "__pycache__"]):
            continue
        if not is_utf8(path):
            bad_files.append(path)

if bad_files:
    print("⚠️ Files with invalid encoding (not UTF-8):")
    for bf in bad_files:
        print(" -", bf)
else:
    print("✅ All files are valid UTF-8")
