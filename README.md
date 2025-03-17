# Item-Sharing-App

## Table of Contents

- [Description](#description)
- [Run the App](#run-the-app)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Citations](#citations)
- [Collaborators](#collaborators)

## Description
The **Item Sharing App** allows database administrators to manually add, edit, and delete data to manage the database for a neighborhood item sharing app. This application was made as a term-long project in CS 340 - Introduction to Databases at Oregon State University, in response to to the November 2024 bomb cyclone that hit and caused large-scale damage in the Pacific Northwest.

## Run the App

1. Clone the repository to the directory of your choice on your local machine:
    ```shell
    git clone https://github.com/lomacanderson/Item-Sharing-App
     ```
2. Create a [MySQL Database](https://dev.mysql.com/doc/mysql-getting-started/en/) to be used

3. Populate the database using the ddl.sql file found at Item-Sharing-App/database/ddl.sql, modifying any data you may want initially in the database

4. Create a file in the root directory called '.env' and populate it with the following:
    ```ini
    APP_MYSQL_HOST = # MySQL database host (e.g., localhost or a remote database server)
    APP_MYSQL_USER = # MySQL username for authentication
    APP_MYSQL_PASSWORD = # MySQL password for authentication (keep this secure and do not share)
    APP_MYSQL_DB_NAME = # Name of the MySQL database to be used by the application
    ```
5. Install Gunicorn to deploy the application
   ```shell
   $ pip install gunicorn
    ```
6. Run Gunicorn:
    ```shell
    gunicorn -w 4 -b 0.0.0.0:8000 app:app
    ```
   - `-w 4` specifies 4 worker processes (adjust based on your system resources).
   - `-b 0.0.0.0:8000` binds the application to port 8000 and can be changed.
   - `app:app` refers to the file `app.py`.

7. (Optional) Run Gunicorn in the background:
    ```shell
    gunicorn -w 4 -b 0.0.0.0:8000 app:app --daemon
    ```
   - This allows Gunicorn to run as a background process.

8. (Optional) Restart Gunicorn if needed:
    ```shell
    pkill gunicorn
    gunicorn -w 4 -b 0.0.0.0:8000 app:app
    ```

9. Access the application by opening `http://localhost:8000` in your browser.
   

## Usage

Users can use the navigation bar to view the contents of all entity and intersection tables in the database.

Users can use the "Add" form on each page to manually add new data to the database.

Users can click "Edit" next to a data entry to edit the data entry.

Users can click "Delete" next to a data entry to delete the data entry.

## Screenshots
Homepage of the Item Sharing App.
![homepage](/screenshots/homepage.png)

Example READ/DELETE: Each page displays a table, showing all data stored in the database for the entity. The user can click the "Delete" link to remove an entity's instance from the database.
![read-user](/screenshots/read_users.png)

Example for ADD: Each page contains an "Add" form, allowing the user to add a new data entry for an entity.
![add-user](/screenshots/add_user.png)

Example for EDIT: Clicking the "Edit" link next to a data entry routes the user to an Edit page.
![edit-user](/screenshots/edit_user.png)

## Citations

<details>
  <summary>Show citations</summary>
Code in this application has beeen adapted from the following sources:

* flask-starter-app/database/db_connector.py
Retrieved on: 02/21/2025
URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/database/db_connector.py

* Canvas Week 4 - Intermediate SQL Assignment (on GradeScope)
Hints and Tips for Intermediate SQL Assignment
Retrieved on 02/04/2025
URL: https://canvas.oregonstate.edu/courses/1987790/assignments/9888499?module_item_id=25022993

* Canvas Week 5 - MySQL Cascade
Retrieved on 02/04/2025
URL: https://canvas.oregonstate.edu/courses/1987790/pages/exploration-mysql-cascade

* bsg_sample_data_manipulation_queries.sql
Provided on Canvas: Project Step 3 Draft Version: Design HTML Interface + DML SQL (Group / On Ed Discussion)
Section: One .SQL file should contain the Data Manipulation Queries:
Retrieved on 02/10/2025
URL: https://canvas.oregonstate.edu/courses/1987790/assignments/9888509?module_item_id=25023016

* W3 Schools: CSS Horizontal Navigation Bar
Retrieved on: 02/08/2025
URL: http://www.w3schools.com/css/css_navbar_horizontal.asp

* W3 Schools: CSS Tables
Retrieved on: 02/08/2025
URL: http://www.w3schools.com/css/css_table.asp

* W3 Schools: CSS Table Style
Retrieved on: 02/08/2025
URL: http://www.w3schools.com/css/css_table_style.asp

* Template Designer Documentation - Template Inheritance - Base Template
Retrieved on: 02/08/2025
URL: https://jinja.palletsprojects.com/en/stable/templates/#template-inheritance

* W3 Schools: CSS Navigation Bars
Retrieved on: 02/08/2025
URL: http://www.w3schools.com/css/css_navbar.asp

* W3 Schools: HTML Tables
Retrieved on: 02/08/2025
URL: http://www.w3schools.com/html/html_tables.asp

* W3 Schools: HTML `<button>` Tag
Retrieved on: 02/09/2025
URL: http://www.w3schools.com/tags/tag_button.asp

* W3 Schools: HTML `<form>` Tag
Retrieved on: 02/09/2025
URL: http://www.w3schools.com/tags/tag_form.asp

* W3 Schools: HTML Input Attributes
Retrieved on: 03/14/2025
URL: https://www.w3schools.com/html/html_form_attributes.asp

* W3 Schools: HTML `<select>` Tag
Retrieved on: 03/04/2025
URL: http://www.w3schools.com/tags/tag_form.asp

* Stackoverflow post "Set default value for select html element in Jinja template?"
Answer from User Matt Healy
Retrieved on: 03/14/2025
URL: https://stackoverflow.com/questions/29451208/set-default-value-for-select-html-element-in-jinja-template

* W3 Schools: HTML Form Elements
Retrieved on: 03/07/2025
URL: https://www.w3schools.com/html/html_form_elements.asp

* W3 Schools: HTML Input Types
Retrieved on: 03/07/2025
URL: https://www.w3schools.com/html/html_form_input_types.asp

* A delightful reference for HTML Symbols, Entities and ASCII Character Codes
Retrieved on: 03/10/2025
URL: https://www.toptal.com/designers/htmlarrows/

* MDN Web Docs - datetime-local
`<input type="datetime-local">`
Retrieved on: 03/14/2025
URL: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/datetime-local

* Template Designer Documentation - List of Control Structures - For - loop.index0
Retrieved on: 03/08/2025
URL: https://jinja.palletsprojects.com/en/stable/templates/#for
</details>


## Collaborators

- [Eva Griffin](https://github.com/evacgriffin)
- [Logan Anderson](https://github.com/lomacanderson)
