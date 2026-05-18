import re

with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/localdb.sql", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

match = re.search(r"CREATE TABLE `action_logs` \((.*?)\) ENGINE", content, re.DOTALL | re.IGNORECASE)
if match:
    print(match.group(1).strip())
else:
    print("action_logs not found")
