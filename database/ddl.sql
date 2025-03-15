/*
Authors:	Eva Griffin, Logan Anderson
Course:		CS 340 - Introduction to Databases
Date:		02/19/2025
Assignment:	Project Step 6 - Portfolio

Code Citations:
-------------------------------------------------------------------------------------------
The following queries are based on:

Canvas Week 4 - Intermediate SQL Assignment (on GradeScope)
Hints and Tips for Intermediate SQL Assignment
Retrieved on 02/04/2025
URL: https://canvas.oregonstate.edu/courses/1987790/assignments/9888499?module_item_id=25022993

Canvas Week 5 - MySQL Cascade
Retrieved on 02/04/2025
URL: https://canvas.oregonstate.edu/courses/1987790/pages/exploration-mysql-cascade
*/

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT=0;

-- Create Neighborhoods table
DROP TABLE IF EXISTS Neighborhoods;

CREATE TABLE Neighborhoods (
    neighborhoodID INT AUTO_INCREMENT UNIQUE NOT NULL,
    neighborhoodName VARCHAR(145) UNIQUE NOT NULL,
    PRIMARY KEY (neighborhoodID)
);

-- Create ItemCategories table
DROP TABLE IF EXISTS ItemCategories;

CREATE TABLE ItemCategories (
    categoryID INT AUTO_INCREMENT UNIQUE NOT NULL,
    categoryName VARCHAR(145) UNIQUE NOT NULL,
    PRIMARY KEY (categoryID)
);

-- Create the Users table
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    userID INT AUTO_INCREMENT UNIQUE NOT NULL,
    userName VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    neighborhoodID INT, -- changed to NULLable
    PRIMARY KEY (userID),
    FOREIGN KEY (neighborhoodID) REFERENCES Neighborhoods(neighborhoodID)
    ON DELETE CASCADE
);

-- Create Items table
DROP TABLE IF EXISTS Items;

CREATE TABLE Items (
    itemID INT AUTO_INCREMENT UNIQUE NOT NULL,
    itemName VARCHAR(100) UNIQUE NOT NULL,
    categoryID INT NOT NULL,
    PRIMARY KEY (itemID),
    FOREIGN KEY (categoryID) REFERENCES ItemCategories(categoryID)
    ON DELETE CASCADE
);

-- Create UserItems table
DROP TABLE IF EXISTS UserItems;

CREATE TABLE UserItems (
    userID INT NOT NULL,
    itemID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID)
    ON DELETE CASCADE,
    FOREIGN KEY (itemID) REFERENCES Items(itemID)
    ON DELETE CASCADE
);

-- Create Transfers table
DROP TABLE IF EXISTS Transfers;

CREATE TABLE Transfers (
    transferID INT AUTO_INCREMENT UNIQUE NOT NULL,
    transferDateTime DATETIME NOT NULL,
    lendingUserID INT NOT NULL,
    borrowingUserID INT NOT NULL,
    PRIMARY KEY (transferID),
    FOREIGN KEY (lendingUserID) REFERENCES Users(userID)
    ON DELETE CASCADE,
    FOREIGN KEY (borrowingUserID) REFERENCES Users(userID)
    ON DELETE CASCADE
);

-- Create TransferItems table
DROP TABLE IF EXISTS TransferItems;

CREATE TABLE TransferItems (
    transferItemID INT AUTO_INCREMENT UNIQUE NOT NULL,
    transferID INT NOT NULL,
    itemID INT NOT NULL,
    quantity INT NOT NULL,
    milliliters DECIMAL(7, 2),
    pounds DECIMAL(5, 2),
    PRIMARY KEY (transferItemID),
    FOREIGN KEY (transferID) REFERENCES Transfers(transferID)
	ON DELETE CASCADE,
    FOREIGN KEY (itemID) REFERENCES Items(itemID)
    ON DELETE CASCADE
);

-- Add sample data to Neighborhoods table
INSERT INTO Neighborhoods(neighborhoodName)
VALUES ('Belltown'),
('South Lake Union'),
('West Capitol Hill'),
('Pioneer Square'),
('Waterfront');

-- Add sample data to ItemCategories table
INSERT INTO ItemCategories(categoryName)
VALUES ('lighting'),
('food'),
('drinks'),
('clothing'),
('energy');

-- Add sample data to Users table
INSERT INTO Users(userName, password, email, neighborhoodID)
VALUES ('katie775', 'example_pw_1', 'katie775@gmail.com', 5),
('friendly_neighbor3', 'example_pw_2', 'neighbor3@gmail.com', 3),
('ben.smith89', 'example_pw_3', 'bsmith89@gmail.com', 4),
('griff123', 'example_pw_4', 'griff123@hotmail.com', NULL),
('camper007', 'example_pw_5', 'camper7@gmail.com', 2);

-- Add sample data to Items table
INSERT INTO Items(itemName, categoryID)
VALUES ('lantern', (SELECT categoryID FROM ItemCategories WHERE categoryName = 'lighting')),
('AA battery', (SELECT categoryID FROM ItemCategories WHERE categoryName = 'energy')),
('water bottle', (SELECT categoryID FROM ItemCategories WHERE categoryName = 'drinks')),
('rice', (SELECT categoryID FROM ItemCategories WHERE categoryName = 'food')),
('beanie', (SELECT categoryID FROM ItemCategories WHERE categoryName = 'clothing'));

-- Add sample data to UserItems table
INSERT INTO UserItems(userID, itemID)
VALUES ((SELECT userID FROM Users WHERE userName = 'katie775'), (SELECT itemID FROM Items WHERE itemName = 'beanie')),
((SELECT userID FROM Users WHERE userName = 'katie775'), (SELECT itemID FROM Items WHERE itemName = 'water bottle')),
((SELECT userID FROM Users WHERE userName = 'ben.smith89'), (SELECT itemID FROM Items WHERE itemName = 'AA battery')),
((SELECT userID FROM Users WHERE userName = 'ben.smith89'), (SELECT itemID FROM Items WHERE itemName = 'rice')),
((SELECT userID FROM Users WHERE userName = 'camper007'), (SELECT itemID FROM Items WHERE itemName = 'water bottle'));

-- Add sample data to Transfers table
INSERT INTO Transfers(transferDateTime, lendingUserID, borrowingUserID)
VALUES ('2025-02-04 11:00', (SELECT userID FROM Users WHERE userName = 'ben.smith89'), (SELECT userID FROM Users WHERE userName = 'katie775')),
('2025-02-07 15:30', (SELECT userID FROM Users WHERE userName = 'ben.smith89'), (SELECT userID FROM Users WHERE userName = 'friendly_neighbor3')),
('2025-01-27 17:45', (SELECT userID FROM Users WHERE userName = 'katie775'), (SELECT userID FROM Users WHERE userName = 'friendly_neighbor3')),
('2025-01-01 10:00', (SELECT userID FROM Users WHERE userName = 'katie775'), (SELECT userID FROM Users WHERE userName = 'ben.smith89')),
('2025-02-01 18:30', (SELECT userID FROM Users WHERE userName = 'camper007'), (SELECT userID FROM Users WHERE userName = 'griff123'));

-- Add sample data to TransferItems table
INSERT INTO TransferItems (itemID, transferID, quantity, milliliters, pounds)
VALUES ((SELECT itemID FROM Items WHERE itemName = 'AA battery'), (SELECT transferID FROM Transfers JOIN Users u1 ON Transfers.lendingUserID = u1.userID JOIN Users u2 ON Transfers.borrowingUserID = u2.userID WHERE u1.userName = 'ben.smith89' AND u2.userName = 'katie775'), 20, NULL, NULL),
((SELECT itemID FROM Items WHERE itemName = 'rice'), (SELECT transferID FROM Transfers JOIN Users u1 ON Transfers.lendingUserID = u1.userID JOIN Users u2 ON Transfers.borrowingUserID = u2.userID WHERE u1.userName = 'ben.smith89' AND u2.userName = 'friendly_neighbor3'), 3, NULL, NULL),
((SELECT itemID FROM Items WHERE itemName = 'beanie'), (SELECT transferID FROM Transfers JOIN Users u1 ON Transfers.lendingUserID = u1.userID JOIN Users u2 ON Transfers.borrowingUserID = u2.userID WHERE u1.userName = 'katie775' AND u2.userName = 'friendly_neighbor3'), 3, NULL, 2.0),
((SELECT itemID FROM Items WHERE itemName = 'water bottle'), (SELECT transferID FROM Transfers JOIN Users u1 ON Transfers.lendingUserID = u1.userID JOIN Users u2 ON Transfers.borrowingUserID = u2.userID WHERE u1.userName = 'katie775' AND u2.userName = 'ben.smith89'), 4, 500.00, NULL),
((SELECT itemID FROM Items WHERE itemName = 'water bottle'), (SELECT transferID FROM Transfers JOIN Users u1 ON Transfers.lendingUserID = u1.userID JOIN Users u2 ON Transfers.borrowingUserID = u2.userID WHERE u1.userName = 'camper007' AND u2.userName = 'griff123'), 2, 600.00, NULL);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;