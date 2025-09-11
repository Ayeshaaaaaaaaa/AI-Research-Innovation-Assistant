import io

files = ["requirements.txt", "uv.lock"]

for f in files:
    try:
        with open(f, "rb") as infile:
            raw = infile.read()
        text = raw.decode("utf-8", errors="ignore")  # ignore bad chars
        with io.open(f, "w", encoding="utf-8") as outfile:
            outfile.write(text)
        print(f"✅ Fixed: {f}")
    except Exception as e:
        print(f"❌ Error fixing {f}: {e}")
