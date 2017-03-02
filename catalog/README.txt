# Catalog

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users have the ability to post, edit and delete their own items.

To start this application:

1. Run database_setup.py to setup shop, shopping item and user database.
2. Run sample_data_sets.py to set sample data if you want.
3. Run project.py and access http://localhost:5001/ to see the website.

From the top page, a user can:

1. view existing posts but cannot edit them until login/sign up
2. create a new account
3. login

After logged in, a user can:

1. create a new shop (/blog/newpost)
2. edit/delete shop that are owned by the user
3. create a new shopping item in a shop
4. edit/delete items that are owned by the user
5. logout
