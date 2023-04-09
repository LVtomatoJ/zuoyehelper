import json
with open("config.json", "r", encoding="utf-8") as f:
    content = json.load(f)

print(content)