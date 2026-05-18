import re

with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/localdb.sql", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

for table in ["lesson_progress", "inspections"]:
    print(f"=== FOREIGN KEYS FOR {table} ===")
    matches = re.findall(r"ALTER TABLE `{}`\s*(.*?);".format(table), content, re.DOTALL | re.IGNORECASE)
    for m in matches:
        print(m.strip())
