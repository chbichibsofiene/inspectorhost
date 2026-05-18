import re

with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/localdb.sql", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print("File length:", len(content))

for match in re.finditer(r"INSERT INTO `profile_delegations`", content, re.IGNORECASE):
    start = max(0, match.start() - 100)
    end = min(len(content), match.end() + 500)
    print("--- MATCH ---")
    print(content[start:end])
