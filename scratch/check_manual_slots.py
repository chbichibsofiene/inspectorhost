import re

with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/localdb.sql", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

match = re.search(r"INSERT INTO `timetable_slots`.*?;", content, re.DOTALL | re.IGNORECASE)
if match:
    print(match.group(0))
else:
    print("No INSERT INTO timetable_slots found")
