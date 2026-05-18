import re

with open("c:/Users/scsof/Downloads/Inspector_1-main/Inspector_1-main/localdb.sql", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

tables = [
    "courses", "course_modules", "course_lessons", "course_assignments",
    "quizzes", "quiz_questions", "quiz_assignments", "quiz_submissions"
]

for table in tables:
    print(f"=== TABLE: {table} ===")
    match = re.search(r"CREATE TABLE `{}` \((.*?)\) ENGINE".format(table), content, re.DOTALL | re.IGNORECASE)
    if match:
        print(match.group(1).strip())
    else:
        print("Not found")
