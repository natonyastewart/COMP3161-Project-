import mysql.connector
import random
from faker import Faker
from collections import defaultdict

# ---------------------- CONFIG ---------------------- #
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "  ",
    "database": "ourvle5"
}

NUM_STUDENTS = 100_000
NUM_LECTURERS = 200
NUM_COURSES = 200

# ---------------------- SETUP ---------------------- #
fake = Faker()
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Safe DB reset (skip errors if table doesn't exist)
print("🧹 Resetting tables (skipping missing)...")
tables_to_truncate = [
    "Grades", "Submissions", "Assignments", "CourseContent",
    "Replies", "Threads", "Forums", "CalendarEvents",
    "Enrollments", "Courses", "Users"
]

cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
for table in tables_to_truncate:
    try:
        cursor.execute(f"TRUNCATE TABLE {table}")
    except mysql.connector.errors.ProgrammingError as e:
        print(f"Skipped {table}: {e}")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# ---------------------- INSERT LECTURERS ---------------------- #
print("👨‍🏫 Inserting lecturers...")
lecturer_data = [
    (fake.unique.user_name(), fake.first_name(), fake.last_name(), fake.password()) for _ in range(NUM_LECTURERS)
]
cursor.executemany("""
    INSERT INTO Users (Username, FirstName, LastName, Password, Role)
    VALUES (%s, %s, %s, %s, 'lecturer')
""", lecturer_data)
cursor.execute("SELECT UserID FROM Users WHERE Role = 'lecturer'")
lecturer_ids = [row[0] for row in cursor.fetchall()]

# ---------------------- INSERT STUDENTS ---------------------- #
print("🎓 Inserting students...")
student_data = [
    (fake.unique.user_name(), fake.first_name(), fake.last_name(), fake.password()) for _ in range(NUM_STUDENTS)
]
cursor.executemany("""
    INSERT INTO Users (Username, FirstName, LastName, Password, Role)
    VALUES (%s, %s, %s, %s, 'student')
""", student_data)
cursor.execute("SELECT UserID FROM Users WHERE Role = 'student'")
student_ids = [row[0] for row in cursor.fetchall()]

# ---------------------- INSERT COURSES ---------------------- #
print("Inserting courses...")
departments = {
    "COMP": ["Intro to Programming", "Data Structures", "Operating Systems", "AI Fundamentals", "Software Engineering"],
    "MATH": ["Calculus I", "Linear Algebra", "Differential Equations", "Real Analysis", "Abstract Algebra"],
    "PHYS": ["Mechanics", "Electromagnetism", "Thermodynamics", "Quantum Mechanics", "General Physics"],
    "CHEM": ["Organic Chemistry", "Inorganic Chemistry", "Biochemistry", "Physical Chemistry"],
    "BIOL": ["Cell Biology", "Genetics", "Evolution", "Molecular Biology", "Anatomy"],
    "ECON": ["Microeconomics", "Macroeconomics", "Econometrics", "Development Economics"],
    "PSYC": ["Intro to Psychology", "Cognitive Psychology", "Abnormal Psychology", "Research Methods"],
    "LAW":  ["Criminal Law", "Contract Law", "Human Rights Law", "International Law"],
    "GEND": ["Gender Studies", "Queer Theory", "Feminist Theory", "Gender and Media"]
}

course_ids = []
course_codes = set()
dept_keys = list(departments.keys())
lecturer_course_count = defaultdict(int)
used_lecturers = set()

for _ in range(NUM_COURSES):
    dept = random.choice(dept_keys)
    title = random.choice(departments[dept])
    code = f"{dept}{random.randint(1000, 4999)}"
    while code in course_codes:
        code = f"{dept}{random.randint(1000, 4999)}"
    course_codes.add(code)

    eligible = [lid for lid in lecturer_ids if lecturer_course_count[lid] < 5]
    if not eligible:
        eligible = lecturer_ids  # fallback if everyone has 5

    lecturer_id = random.choice(eligible)
    lecturer_course_count[lecturer_id] += 1
    used_lecturers.add(lecturer_id)

    cursor.execute("""
        INSERT INTO Courses (CourseCode, CourseName, LecturerID)
        VALUES (%s, %s, %s)
    """, (code, title, lecturer_id))
    course_ids.append(cursor.lastrowid)

# Ensure all lecturers teach at least 1 course
unused_lecturers = set(lecturer_ids) - used_lecturers
for lid in unused_lecturers:
    course_index = random.randint(0, NUM_COURSES - 1)
    cursor.execute("UPDATE Courses SET LecturerID = %s WHERE CourseID = %s", (lid, course_ids[course_index]))

# ---------------------- ENROLL STUDENTS ---------------------- #
print("Enrolling students (3–6 courses each)...")
enrollments = defaultdict(set)
course_members = defaultdict(set)

for sid in student_ids:
    selected = random.sample(course_ids, random.randint(3, 6))
    for cid in selected:
        cursor.execute("""
            INSERT INTO Enrollments (StudentID, CourseID)
            VALUES (%s, %s)
        """, (sid, cid))
        enrollments[sid].add(cid)
        course_members[cid].add(sid)

# Ensure each course has at least 10 students
print("Ensuring each course has at least 10 members...")
for cid in course_ids:
    while len(course_members[cid]) < 10:
        sid = random.choice(student_ids)
        if cid not in enrollments[sid] and len(enrollments[sid]) < 6:
            cursor.execute("""
                INSERT INTO Enrollments (StudentID, CourseID)
                VALUES (%s, %s)
            """, (sid, cid))
            enrollments[sid].add(cid)
            course_members[cid].add(sid)

conn.commit()
print("Done.")
