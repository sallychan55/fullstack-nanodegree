# fullstack-nanodegree
Full Stack Nanodegree Project

## Table of contents
- [Movies](#movies)
- [Portfolio_Site](#portfolio_site)
- [Multi_User_Blog](#multi_user_blog)
- [Tournament](#tournament)
- [Catalog](#catalog)

## Movies
This folder is for a project "Movie Trailer Website".
To open the movie trailer website, run entertaiment_center.py.
So that the page is came up and you can see movies and watch the trailers by clicking poster images. 

## Portfolio_Site
The folder contains all codes for "Portfolio Site" project. Index.html shows the page.

## Multi_User_Blog
This project codes are stored under multi_user_blog folder.

This project runs on Google Cloud Platform. You can visit [the page](https://hello-world-sally-158219.appspot.com) to see a sample.

From the top page, a user can:

1. view existing posts but cannot edit them until login
2. create a new account (/signup)
3. login (/login)

After logged in, a user can:

1. create a new post (/blog/newpost)
2. edit/delete posts that are owned by the user
3. create a new comment on posts
4. edit/delete comments that are owned by the user
5. like/unlike other users' posts
6. logout (/logout)

## Tournament
This folder contains one database configuration file and two python files.

* tournament.sql -  This file is used to set up database schema.
* tournament.py - This file is a library of functions to provide access to the database for adding, deleting or querying data from a client program.
* tournament_test.py - This is a client program to verify functions in the tournament.py.

To start this application:

1. Run tournament.sql from psql by following command "\i tournament.sql". That works to build a tournament database, players and matches tables.
2. Then run tournament_test.py to verify functions in tournament.py to manage players and games.
3. After running the test script, you will see results of 10 tests.

## Catalog
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
