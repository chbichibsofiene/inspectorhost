import re

with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/localdb.sql", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

for table in ["profile_delegations", "profile_departments", "profile_dependencies", "profile_etablissements"]:
    print(f"=== {table} ===")
    match = re.search(rf"INSERT INTO `{table}`.*?;", content, re.DOTALL | re.IGNORECASE)
    if match:
        print(match.group(0))
    else:
        print("No insert found")
