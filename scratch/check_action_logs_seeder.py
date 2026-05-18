import re

with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/seed_production_data.sql", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

match = re.search(r"INSERT INTO `action_logs`.*?;", content, re.DOTALL | re.IGNORECASE)
if match:
    print(match.group(0)[:1000])
else:
    print("action_logs insert not found")
