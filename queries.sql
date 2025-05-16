USE ourvle5;

-- Count of students (should be 100000)
SELECT COUNT(*) FROM Users WHERE Role = 'student';

-- Count of courses (should be 200)
SELECT COUNT(*) FROM Courses;

-- Students enrolled in less than 3 or more than 6 courses (should return 0)
SELECT StudentID, COUNT(*) AS NumCourses
FROM Enrollments
GROUP BY StudentID
HAVING NumCourses < 3 OR NumCourses > 6;

-- Courses with fewer than 10 students (should return 0)
SELECT CourseID, COUNT(*) AS NumStudents
FROM Enrollments
GROUP BY CourseID
HAVING NumStudents < 10;

-- Lecturers teaching less than 1 or more than 5 courses (should return 0)
SELECT LecturerID, COUNT(*) AS NumCourses
FROM Courses
GROUP BY LecturerID
HAVING NumCourses < 1 OR NumCourses > 5;

-- Courses without a lecturer assigned (should return 0)
SELECT CourseID
FROM Courses
WHERE LecturerID IS NULL;

-- Total enrollments (just informational)
SELECT COUNT(*) FROM Enrollments;

-- Optional: Students with no course enrollment
SELECT u.UserID
FROM Users u
LEFT JOIN Enrollments e ON u.UserID = e.StudentID
WHERE u.Role = 'student'
GROUP BY u.UserID
HAVING COUNT(e.CourseID) = 0;

-- Optional: Lecturers with no courses assigned
SELECT u.UserID
FROM Users u
LEFT JOIN Courses c ON u.UserID = c.LecturerID
WHERE u.Role = 'lecturer'
GROUP BY u.UserID
HAVING COUNT(c.CourseID) = 0;





