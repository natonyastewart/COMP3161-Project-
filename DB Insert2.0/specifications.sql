SELECT COUNT(*) AS TotalStudents FROM students;

SELECT COUNT(*) AS TotalCourses FROM courses;


SELECT StudentID, COUNT(CourseID) AS CoursesEnrolled
FROM Enrollment
GROUP BY StudentID
HAVING COUNT(CourseID) > 6;


SELECT StudentID, COUNT(CourseID) AS CoursesEnrolled
FROM Enrollment
GROUP BY StudentID
HAVING COUNT(CourseID) < 3;


SELECT CourseID, COUNT(StudentID) AS Members
FROM Enrollment
GROUP BY CourseID
HAVING COUNT(StudentID) < 10;


SELECT LecturerID, COUNT(CourseID) AS CoursesAssigned
FROM LecturerCourses
GROUP BY LecturerID
HAVING COUNT(CourseID) > 5;


SELECT LecturerID
FROM Lecturers
WHERE LecturerID NOT IN (SELECT DISTINCT LecturerID FROM LecturerCourses);
