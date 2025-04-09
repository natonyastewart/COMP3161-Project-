import pandas as pd
import mysql.connector

# Database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "   ",
    "database": "ourvle"
}

def sql_escape(value):
    if pd.isnull(value):
        return 'NULL'
    return str(value).replace("'", "''")

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert Students
    students_df = pd.read_csv("students.csv")
    with open("students.sql", "w", encoding="utf-8") as f:
        for _, row in students_df.iterrows():
            sql = f"""INSERT INTO Users (Username, FirstName, LastName, Password, Role)
            VALUES ('{sql_escape(row['Username'])}', '{sql_escape(row['FirstName'])}', '{sql_escape(row['LastName'])}',
                '{sql_escape(row['Password'])}', 'students');"""
            f.write(sql)
            cursor.execute("INSERT INTO Users (Username, FirstName, LastName, Password, Role) VALUES (%s, %s, %s, %s, %s)", 
                           (row['Username'], row['FirstName'], row['LastName'], row['Password'], 'students'))

    # Insert Lecturers
    lecturers_df = pd.read_csv("lecturers.csv")
    with open("lecturers.sql", "w", encoding="utf-8") as f:
        for _, row in lecturers_df.iterrows():
            username = row['Email'].split("@")[0]
            sql = f"""INSERT INTO Users (Username, FirstName, LastName, Password, Role)
                VALUES ('{sql_escape(username)}', '{sql_escape(row['FirstName'])}', '{sql_escape(row['LastName'])}',
                '{sql_escape(row['Password'])}', 'lecturer');"""
            f.write(sql)
            cursor.execute("INSERT INTO Users (Username, FirstName, LastName, Password, Role) VALUES (%s, %s, %s, %s, %s)", 
                           (username, row['FirstName'], row['LastName'], row['Password'], 'lecturer'))

    # Insert Admins
    admins_df = pd.read_csv("admins.csv")
    with open("admins.sql", "w", encoding="utf-8") as f:
        for _, row in admins_df.iterrows():
            username = row['Email'].split("@")[0]
            sql = f"""INSERT INTO Users (Username, FirstName, LastName, Password, Role)
                VALUES ('{sql_escape(username)}', '{sql_escape(row['FirstName'])}', '{sql_escape(row['LastName'])}',
                '{sql_escape(row['Password'])}', 'admin');"""
            f.write(sql)
            cursor.execute("INSERT INTO Users (Username, FirstName, LastName, Password, Role) VALUES (%s, %s, %s, %s, %s)", 
                           (username, row['FirstName'], row['LastName'], row['Password'], 'admin'))

    # Insert Courses (temporarily LecturerID = NULL)
    courses_df = pd.read_csv("courses.csv")
    with open("courses.sql", "w", encoding="utf-8") as f:
        for _, row in courses_df.iterrows():
            sql = f"""INSERT INTO Courses (CourseCode, CourseName, LecturerID)
            VALUES ('{sql_escape(row['CourseCode'])}', '{sql_escape(row['CourseName'])}', NULL);"""
            f.write(sql)
            cursor.execute("INSERT INTO Courses (CourseCode, CourseName, LecturerID) VALUES (%s, %s, %s)", 
                           (row['CourseCode'], row['CourseName'], None))

    conn.commit()
    print("Data inserted and SQL files created.")

except mysql.connector.Error as e:
    print(f"MySQL Error: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
