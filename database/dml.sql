/*
Authors:	Eva Griffin, Logan Anderson
Course:		CS 340 - Introduction to Databases
Date:		02/19/2025
Assignment:	Project Step 3 FINAL VERSION - DML SQL Queries

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
SELECT userID AS "User ID", username AS Username, password AS Password, email AS Email, neighborhoodID AS "Neighborhood ID" FROM Users;

-- Get all neighborhood IDs and neighborhood names to populate the neighborhood dropdown in the "Add New User" and "Edit User" forms
SELECT neighborhoodID, neighborhoodName FROM Neighborhoods;

-- Add a new user
INSERT INTO Users (userName, password, email, neighborhoodID)
VALUES (:userNameInput, :passwordInput, :emailInput, :neighborhoodIDSelectedFromDropdown);

-- Edit an existing user
UPDATE Users
SET userName = :userNameInput, password = :passwordInput, email = :emailInput, neighborhoodID = :neighborhoodIDSelectedFromDropdown
WHERE userID = :userIDFromUpdateForm;

-- Delete a user
DELETE FROM Users
WHERE userID = :userIDSelectedFromUsersTable;

/* ---------- Items Page ---------- */

-- Get all fields from Items to be displayed in the table on this page
SELECT itemID AS "Item ID", itemName AS "Item Name", categoryID AS "Category ID" FROM Items;

-- Get all category IDs and category names to populate the category dropdown in the "Add New Item" and "Edit Item" forms
SELECT categoryID, categoryName FROM ItemCategories;

-- Add a new item
INSERT INTO Items (itemName, categoryID)
VALUES (:itemNameInput, :categoryIDSelectedFromDropdown);

-- Edit an existing item
UPDATE Items
SET itemName = :itemNameInput, categoryID = :categoryIDSelectedFromDropdown
WHERE itemID = :itemIDFromUpdateForm;

-- Delete an item
DELETE FROM Items
WHERE itemID = :itemIDSelectedFromItemsTable;

/* ---------- User Items Page ---------- */

-- Get all fields from UserItems to be displayed in the table on this page
SELECT userID AS "User ID", itemID AS "Item ID" FROM UserItems;

-- Get all user IDs and user names to populate the username dropdown in the "Add New User Item" form
SELECT userID, userName FROM Users;

-- Get all item IDs and item names to populate the item name dropdown in the "Add New User Item" and "Edit User Item" forms
SELECT itemID, itemName FROM Items;

-- Add a new user item
INSERT INTO UserItems (userID, itemID)
VALUES (:userIDSelectedFromDropdown, :itemIDSelectedFromDropdown);

-- Edit an existing user item
UPDATE UserItems
SET itemID = :itemIDSelectedFromDropdown
WHERE userID = :itemIDFromUpdateForm AND itemID = :itemIDSelectedFromUserItemsTable;

-- Delete a user item
DELETE FROM UserItems
WHERE userID = :userIDSelectedFromUserItemsTable AND itemID = :itemIDSelectedFromUserItemsTable;

/* ---------- Item Categories Page ---------- */

-- Get all category IDs and category names to be displayed in the table on this page
SELECT categoryID AS "Category ID", categoryName AS "Category Name" FROM ItemCategories;

-- Add a new item category
INSERT INTO ItemCategories (categoryName)
VALUES (:categoryNameInput);

-- Edit an existing item category
UPDATE ItemCategories
SET categoryName = :categoryNameInput
WHERE categoryID = :categoryIDFromUpdateForm;

-- Delete an item category
DELETE FROM ItemCategories
WHERE categoryID = :categoryIDSelectedFromCategoriesPage;

/* ---------- Neighborhoods Page ---------- */

-- Get all neighborhood IDs and neighborhood names to be displayed in the table on this page
SELECT neighborhoodID AS "Neighborhood ID", neighborhoodName AS "Neighborhood Name" FROM Neighborhoods;

-- Add a new neighborhood
INSERT INTO Neighborhoods (neighborhoodName)
VALUES (:neighborhoodNameInput);

-- Edit an existing neighborhood
UPDATE Neighborhoods
SET neighborhoodName = :neighborhoodNameInput
WHERE neighborhoodID = :neighborhoodIDFromUpdateForm;

-- Delete an item category
DELETE FROM Neighborhoods
WHERE neighborhoodID = :neighborhoodIDSelectedFromNeighborhoodsPage;

/* ---------- Transfers Page ---------- */

-- Get all fields from the Transfers table to be displayed in the table on this page
SELECT transferID AS "Transfer ID", transferDateTime AS "Transfer Date and Time", lendingUserID AS "Lending User ID", borrowingUserID AS "Borrowing User ID" FROM Transfers;

-- Get user IDs and userNames to populate dropdowns
SELECT userID AS lendingUserID, userName FROM Users;
SELECT userID AS borrowingUserID, userName FROM Users;

-- Add a new transfer
INSERT INTO Transfers (transferDateTime, lendingUserID, borrowingUserID)
VALUES (:transferDateTimeInput, :lendingUserIDFromDropdown, :borrowingUserIDFromDropdown);

-- Edit an existing transfer
UPDATE Transfers
SET transferDateTime = :transferDateTimeInput, lendingUserID = :lendingUserIDFromDropdown, borrowingUserID = :borrowingUserIDFromDropdown
WHERE transferID = :transferIDFromUpdateForm;

-- Delete an item category
DELETE FROM Transfers
WHERE transferID = :transferIDSelectedFromTransfersPage;

/* ---------- Transfer Items Page ---------- */

-- Get all fields from the TransferItems table to be displayed in the table on this page
SELECT transferItemID AS "Transfer Item ID", itemID AS "Item ID", transferID AS "Transfer ID", quantity AS Quantity, milliliters AS Milliliters, pounds AS Pounds FROM TransferItems;

-- Get all transfer IDs and their associated user IDs to populate the transfer dropdown
SELECT transferID, lendingUserID, borrowingUserID FROM Transfers;

-- Get all item IDs and item names to populate the items dropdown
SELECT itemID, itemName FROM Items;

-- Add a new transfer item relationship to the table
-- Associate an existing item with a transfer (M:N relationship)
INSERT INTO TransferItems (transferID, itemID, quantity, milliliters, pounds)
VALUES (:transferIDFromDropdown, :itemIDFromDropdown, :quantityInput, :millilitersInput, :poundsInput);

-- Edit an existing transfer-item relationship
UPDATE TransferItems
SET transferID = :transferIDFromDropdown, itemID = :itemIDFromDropdown, quantity = :quantityInput, milliliters = :millilitersInput, pounds = :poundsInput
WHERE transferItemID = :transferItemIDFromUpdateForm;

-- Delete a transfer-item relationship
DELETE FROM TransferItems
WHERE transferItemID = :transferItemIDSelectedFromTable;
