CREATE DATABASE ourvle;
USE ourvle;

CREATE TABLE User (
    UserID INT PRIMARY KEY,
    UserName VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE Account (
    AccountID INT PRIMARY KEY,
    AccountName VARCHAR(255) NOT NULL,
    AccountType VARCHAR(255) NOT NULL
);

CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(255) NOT NULL,
    Description TEXT
);

CREATE TABLE DiscussionForum (
    ForumID INT PRIMARY KEY,
    ForumName VARCHAR(255) NOT NULL,
    CourseID INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE DiscussionThread (
    ThreadID INT PRIMARY KEY,
    ThreadName VARCHAR(255) NOT NULL,
    ForumID INT,
    FOREIGN KEY (ForumID) REFERENCES DiscussionForum(ForumID)
);

CREATE TABLE Member (
    MemberID INT PRIMARY KEY,
    MemberName VARCHAR(255) NOT NULL,
    MemberType VARCHAR(255) NOT NULL,
    CourseID INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE Admin (
    AdminID INT PRIMARY KEY,
    AdminName VARCHAR(255) NOT NULL,
    AdminEmail VARCHAR(255) NOT NULL,
    AdminContactInfo VARCHAR(255),
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    StudentName VARCHAR(255) NOT NULL,
    Major VARCHAR(255),
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE Lecturer (
    LecturerID INT PRIMARY KEY,
    LecturerName VARCHAR(255) NOT NULL,
    Department VARCHAR(255),
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE CalendarEvent (
    EventID INT PRIMARY KEY,
    EventName VARCHAR(255) NOT NULL
);

CREATE TABLE Assignment (
    AssignmentID INT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    DueDate DATE,
    CourseID INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE SectionItem (
    SectionID INT PRIMARY KEY,
    SectionName VARCHAR(255) NOT NULL
);

CREATE TABLE LectureSlide (
    LectureID INT PRIMARY KEY,
    LectureSlideName VARCHAR(255) NOT NULL,
    CourseID INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE ISALink (
    LinkID INT PRIMARY KEY,
    LinkName VARCHAR(255) NOT NULL
);
