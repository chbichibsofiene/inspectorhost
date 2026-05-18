import re

with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/localdb.sql", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

for table in ["lesson_progress", "inspections"]:
    print(f"=== TABLE: {table} ===")
    match = re.search(r"CREATE TABLE `{}` \((.*?)\) ENGINE".format(table), content, re.DOTALL | re.IGNORECASE)
    if match:
        print(match.group(1).strip())
    else:
        print("Not found")
