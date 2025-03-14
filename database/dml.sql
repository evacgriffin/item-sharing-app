/*
Authors:	Eva Griffin, Logan Anderson
Course:		CS 340 - Introduction to Databases
Date:		03/14/2025
Assignment:	Project Step 6 - Portfolio

Code Citations:
-------------------------------------------------------------------------------------------
The following queries are based on:

bsg_sample_data_manipulation_queries.sql
Provided on Canvas: Project Step 3 Draft Version: Design HTML Interface + DML SQL (Group / On Ed Discussion)
Section: One .SQL file should contain the Data Manipulation Queries:
Retrieved on 02/10/2025
URL: https://canvas.oregonstate.edu/courses/1987790/assignments/9888509?module_item_id=25023016
*/

/* ---------- Users Page ---------- */

-- Get all fields from Users to be displayed in the table on this page
SELECT
    Users.userID AS "User ID",
    Users.username AS Username,
    Users.password AS Password,
    Users.email AS Email,
    Neighborhoods.neighborhoodName AS "Neighborhood"
FROM Users
LEFT JOIN Neighborhoods ON Users.neighborhoodID = Neighborhoods.neighborhoodID
ORDER BY Users.userID;

-- Get all neighborhood names to populate the neighborhood dropdown
SELECT neighborhoodName FROM Neighborhoods;

-- Add a new user without an associated neighborhood (NULLable relationship)
INSERT INTO Users (userName, password, email)
VALUES (:userNameInput, :passwordInput, :emailInput);

-- Add a new user with an associated neighborhood (NULLable relationship)
INSERT INTO Users (userName, password, email, neighborhoodID)
VALUES (
    :userNameInput, 
    :passwordInput, 
    :emailInput, 
    (SELECT neighborhoodID 
        FROM Neighborhoods 
        WHERE neighborhoodName = :neighborhoodNameInput));

-- Get all fields for the selected user to display on the Edit page
SELECT
    Users.userID AS "User ID",
    Users.username AS Username,
    Users.password AS Password,
    Users.email AS Email,
    Neighborhoods.neighborhoodName AS "Neighborhood"
FROM Users
LEFT JOIN Neighborhoods ON Users.neighborhoodID = Neighborhoods.neighborhoodID
WHERE userID = :userIDSelectedWithEditButton;

-- Edit the selected user if they don't an associated neighborhood (NULLable relationship)
UPDATE Users
SET 
    userName = :userNameInput, 
    password = :passwordInput, 
    email = :emailInput, 
    neighborhoodID = NULL
WHERE userID = :userIDSelectedWithEditButton;

-- Edit the selected user if they have an associated neighborhood (NULLable relationship)
UPDATE Users
SET 
    userName = :userNameInput, 
    password = :passwordInput, 
    email = :emailInput, 
    neighborhoodID = (SELECT neighborhoodID 
                        FROM Neighborhoods 
                        WHERE neighborhoodName = :neighborhoodNameSelectedFromDropdown)
WHERE userID = :userIDSelectedWithEditButton;

-- Delete a user
DELETE FROM Users
WHERE userID = :userIDSelectedWithDeleteButton;

/* ---------- Items Page ---------- */

-- Get all fields from Items to be displayed in the table on this page
SELECT 
    Items.itemID AS "Item ID", 
    Items.itemName AS "Item Name", 
    ItemCategories.categoryName AS "Category Name" 
FROM Items
JOIN ItemCategories ON Items.categoryID = ItemCategories.categoryID
ORDER BY Items.itemID;

-- Get all category names to populate the category dropdown
SELECT categoryName FROM ItemCategories;

-- Add a new item
INSERT INTO Items (itemName, categoryID)
VALUES (
    :itemNameInput, 
    (SELECT categoryID 
        FROM ItemCategories 
        WHERE categoryName = :categoryNameSelectedFromDropdown));

-- Get all fields for the selected item to display on the Edit page
SELECT
    Items.itemID AS "Item ID",
    Items.itemName AS "Item Name",
    ItemCategories.categoryName AS "Category Name"
FROM Items
JOIN ItemCategories ON Items.categoryID = ItemCategories.categoryID
WHERE itemID = :itemIDSelectedWithEditButton;

-- Edit the selected item
UPDATE Items
SET 
    itemName = :itemNameInput, 
    categoryID = (SELECT categoryID 
                    FROM ItemCategories 
                    WHERE categoryName = :categoryNameSelectedFromDropdown)
WHERE itemID = :itemIDSelectedWithEditButton;

-- Delete an item
DELETE FROM Items
WHERE itemID = :itemIDSelectedWithDeleteButton;

/* ---------- User Items Page ---------- */

-- Get all fields from UserItems to be displayed in the table on this page
SELECT
    Users.userName AS "Username",
    Items.itemName AS "Item Name"
FROM UserItems
JOIN Users ON Users.UserID = UserItems.UserID
JOIN Items ON Items.itemID = UserItems.itemID
ORDER BY Users.userName;

-- Get all user names to populate the users dropdown
SELECT userName FROM Users;

-- Get all item names to populate the item dropdown
SELECT itemName FROM Items;

-- Get all user IDs and item IDs for the Edit href
SELECT userID, itemID FROM UserItems;

-- Add a new user item
INSERT INTO UserItems (userID, itemID)
VALUES (
    (SELECT userID FROM Users WHERE userName = :userNameSelectedFromDropdown),
    (SELECT itemID FROM Items WHERE itemName = :itemNameSelectedFromDropdown));

-- Get all fields for the selected UserItem to display on the Edit page
SELECT
    Users.userName AS "Username",
    Items.itemName AS "Item Name"
FROM UserItems
JOIN Users ON Users.UserID = UserItems.UserID
JOIN Items ON Items.itemID = UserItems.itemID
WHERE 
    UserItems.userID = :userIDSelectedWithEditButton AND 
    UserItems.itemID = :itemIDSelectedWithEditButton
LIMIT 1;

-- Get the user ID and item ID for the selected UserItem
SELECT userID, itemID FROM UserItems 
WHERE 
    userID = :userIDSelectedWithEditButton AND 
    itemID = :itemIDSelectedWithEditButton;

-- Edit the selected user item
UPDATE UserItems
SET 
    itemID = (SELECT itemID from Items WHERE itemName = :itemNameSelectedFromDropdown),
    userID = (SELECT userID FROM Users WHERE userName = :userNameSelectedFromDropdown)
WHERE 
    userID = :userIDSelectedWithEditButton AND 
    itemID = :itemIDSelectedWithEditButton
LIMIT 1;

-- Delete a user item
DELETE FROM UserItems
WHERE 
    userID = :userIDSelectedWithDeleteButton AND 
    itemID = :itemIDSelectedWithDeleteButton
LIMIT 1;

/* ---------- Item Categories Page ---------- */

-- Get all fields from ItemCategories to be displayed in the table on this page
SELECT 
    categoryID AS "Category ID", 
    categoryName AS "Category Name" 
FROM ItemCategories
ORDER BY categoryID;

-- Add a new item category
INSERT INTO ItemCategories (categoryName)
VALUES (:categoryNameInput);

-- Get all fields for the selected ItemCategory to display on the Edit page
SELECT 
    categoryID AS "Category ID", 
    categoryName AS "Category Name" 
FROM ItemCategories
WHERE categoryID = :categoryIDSelectedWithEditButton;

-- Edit the selected item category
UPDATE ItemCategories
SET categoryName = :categoryNameInput
WHERE categoryID = :categoryIDSelectedWithEditButton;

-- Delete an item category
DELETE FROM ItemCategories
WHERE categoryID = :categoryIDSelectedWithDeleteButton;

/* ---------- Neighborhoods Page ---------- */

-- Get all fields from Neighborhoods to be displayed in the table on this page
SELECT 
    neighborhoodID AS "Neighborhood ID", 
    neighborhoodName AS "Neighborhood Name" 
FROM Neighborhoods
ORDER BY neighborhoodID;

-- Add a new neighborhood
INSERT INTO Neighborhoods (neighborhoodName)
VALUES (:neighborhoodNameInput);

-- Get all fields for the selected Neighborhood to display on the Edit page
SELECT 
    neighborhoodID AS "Neighborhood ID", 
    neighborhoodName AS "Neighborhood Name" 
FROM Neighborhoods
WHERE neighborhoodID = :neighborhoodIDSelectedWithEditButton;

-- Edit the selected neighborhood
UPDATE Neighborhoods
SET neighborhoodName = :neighborhoodNameInput
WHERE neighborhoodID = :neighborhoodIDSelectedWithEditButton;

-- Delete an item category
DELETE FROM Neighborhoods
WHERE neighborhoodID = :neighborhoodIDSelectedWithDeleteButton;

/* ---------- Transfers Page ---------- */

-- Get all fields from Transfers to be displayed in the table on this page
SELECT 
    TransferUsers.transferID AS "Transfer ID", 
    TransferUsers.transferDateTime AS "Transfer Date and Time",
    LendingUsers.userName AS "Lending User", 
    BorrowingUsers.userName AS "Borrowing User"
FROM Transfers AS TransferUsers
JOIN Users AS LendingUsers ON LendingUsers.userID = TransferUsers.lendingUserID
JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = TransferUsers.borrowingUserID
ORDER BY TransferUsers.transferID;

-- Get all user names to populate the lending users dropdown
SELECT userID, userName AS lendingUserName FROM Users;

-- Get all user names to populate the borrowing users dropdown
SELECT userID, userName AS borrowingUserName FROM Users;

-- Add a new transfer
INSERT INTO Transfers (transferDateTime, lendingUserID, borrowingUserID)
VALUES (
    :transferDateTimeInput, 
    (SELECT userID FROM Users WHERE userName = :lendingUserNameSelectedFromDropdown),
    (SELECT userID FROM Users WHERE userName = :borrowingUserNameSelectedFromDropdown));

-- Get all fields for the selected Transfer to display on the Edit page
SELECT 
    TransferUsers.transferID AS "Transfer ID", 
    TransferUsers.transferDateTime AS "Transfer Date and Time",
    TransferUsers.borrowingUserID, 
    TransferUsers.lendingUserID
FROM Transfers AS TransferUsers
JOIN Users AS LendingUsers ON LendingUsers.userID = TransferUsers.lendingUserID
JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = TransferUsers.borrowingUserID
WHERE TransferUsers.transferID = :transferIDSelectedWithEditButton;

-- Get the lending user ID for the selected Transfer
SELECT userID FROM Users WHERE userName = :lendingUserNameForTransferSelectedWithEditButton;

-- Get the borrowing user ID for the selected Transfer
SELECT userID FROM Users WHERE userName = :borrowingUserNameForTransferSelectedWithEditButton;

-- Edit the selected transfer
UPDATE Transfers
SET 
    transferDateTime = :transferDateTimeInput, 
    lendingUserID = :lendingUserIDObtainedWithAboveQuery, 
    borrowingUserID = :borrowingUserIDObtainedWithAboveQuery
WHERE transferID = :transferIDSelectedWithEditButton;

-- Delete an item category
DELETE FROM Transfers
WHERE transferID = :transferIDSelectedWithDeleteButton;

/* ---------- Transfer Items Page ---------- */

-- Get all fields from TransferItems to be displayed in the table on this page
SELECT
    TransferItems.transferItemID AS "Transfer Item ID",
    Items.itemName AS "Item Name",
    Transfers.transferID AS "Transfer ID",
    LendingUsers.userName AS "Lending User",
    BorrowingUsers.userName AS "Borrowing User",
    TransferItems.quantity AS Quantity,
    TransferItems.milliliters AS Milliliters,
    TransferItems.pounds AS Pounds
FROM TransferItems
JOIN Items ON Items.itemID = TransferItems.itemID
JOIN Transfers ON Transfers.transferID = TransferItems.transferID
JOIN Users AS LendingUsers ON LendingUsers.userID = Transfers.lendingUserID
JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = Transfers.borrowingUserID
ORDER BY TransferItems.transferItemID;

-- Get all item names to populate the item dropdown
SELECT itemName FROM Items;

-- Get all transfer IDs and user names from Transfers to populate the transfer dropdown
SELECT
    Transfers.transferID,
    LendingUsers.userName AS "Lending User",
    BorrowingUsers.userName AS "Borrowing User"
FROM Transfers
JOIN Users AS LendingUsers ON LendingUsers.userID = Transfers.lendingUserID
JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = Transfers.borrowingUserID;

-- Get all transfer IDs and item IDs for the Edit href
SELECT transferID, itemID FROM TransferItems;

-- Add a new transfer item
INSERT INTO TransferItems (transferID, itemID, quantity, milliliters, pounds)
VALUES (
    :transferIDSelectedFromDropdown
    (SELECT itemID FROM Items WHERE itemName = :itemNameSelectedFromDropdown),
    :quantityInput,
    :millilitersInput,
    :poundsInput);

-- Get all fields for the selected transfer item to display on the Edit page
SELECT
    TransferItems.transferItemID AS "Transfer Item ID",
    Items.itemName AS "Item Name",
    Transfers.transferID AS "Transfer ID",
    LendingUsers.userName AS "Lending User",
    BorrowingUsers.userName AS "Borrowing User",
    TransferItems.quantity AS Quantity,
    TransferItems.milliliters AS Milliliters,
    TransferItems.pounds AS Pounds
FROM TransferItems
JOIN Items ON Items.itemID = TransferItems.itemID
JOIN Transfers ON Transfers.transferID = TransferItems.transferID
JOIN Users AS LendingUsers ON LendingUsers.userID = Transfers.lendingUserID
JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = Transfers.borrowingUserID
WHERE TransferItems.transferItemID = :transferItemIDSelectedWithEditButton;

-- Get the item ID for the item name selected from the dropdown
SELECT itemID FROM Items WHERE itemName = :itemNameSelectedFromDropdown;

-- Edit the selected transfer item
UPDATE TransferItems
SET
    transferID = :transferIDSelectedFromDropdown,
    itemID = :itemIDFromAboveQuery,
    quantity = :quantityInput,
    milliliters = :millilitersInput,
    pounds = :poundsInput
WHERE transferItemID = :transferItemIDSelectedWithEditButton;

-- Delete the selected transfer item
DELETE FROM TransferItems
WHERE 
    transferID = :transferIDSelectedWithDeleteButton AND 
    itemID = :itemIDSelectedWithDeleteButton;
