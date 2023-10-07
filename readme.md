# CS50W: Web Programming with Python and JavaScript - Manage Vocabulary App

- [CS50W Final Project - Manage Vocabulary App](#cs50w-web-programming-with-python-and-javascript---manage-vocabulary-app)
  - [Overview](#overview)
  - [Distinctiveness and Complexity](#distinctiveness-and-complexity)
  - [Models](#models)
  - [Routes](#routes)
    - [Index `/`](#index)
    - [Authentication `/authentication`](#authentication)
  - [Login `/login`](#login)
  - [Register `/register`](#register)
  - [Logout `logout`](#authentication-logout)
  - [Validate Username `/validate-username`](#validate-username)
  - [Validate Email `/validate-email`](#validate-email)
  - [Active `/active`](#authentication-active)
  - [Reset Password `/reset-password`](#authentication-reset-password)
  - [Reset Password with Token `/reset`](#authentication-reset-password-with-token)
  - [Password Reset Complete `/password-reset-conplete`](#authentication-password-reset-complete)
    - [Add vocabulary `/add-vocabulary`](#add-vocabulary)
    - [Vocabulary Detail `/dictionary/<word_name>`](#vocabulary-detail)
    - [Vocabulary Edit `/dictionary/<word_name>/edit`](#vocabulary-edit)
    - [Search `/search`](#search)
    - [History `/history`](#history)
  - [How to run the application](#how-to-run-the-application)

## Overview

As an English learner, I have invested a lot of time and effort into learning and remembering vocabulary. However, much later, I feel frustrated when I forget some vocabulary words that I had previously learned. For this reason, I have decided to create a vocabulary management website that can help every English learner create their own dictionary by adding new words over time as they learn them.

My web application was built using Django, JavaScript, Gulp, Cronjob and Bootstrap.

## Distinctiveness and complexity

According the the specification, my project must adhere to the following guidelines:

> Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.

I believe that my project meets this requirement for the following reasons:

1. My project is based on an original idea, that solves a real-life personal problem which has no similarity to any of the projects built as part of the CS50W course.
2. On the [Register](#register) function, I have implemented dynamic validation based on JavaScript code, which can accurately validate user data input before inserting it into the database.
3. I build the 'Forgot password' function on the [Login](#login) page, which will send an email to the user containing a dynamic token code link.
4. I set up the configurations for sending mail via `.env` on my localhost project, and I configured those settings through **SECRET VARIABLES** on GitHub.
5. I built a simple cron job that sends a daily email with five random vocabulary words, along with their definitions and examples, based on the user's dictionary.

> Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.

My application was built using Django, including 5 models on the back-end. All generated information is saved in a database (SQLite by default).

> Your web application must be mobile-responsive

Every page and feature of the web application is mobile-responsive and this is achieved using Bootstrap and custom CSS.

## Models

There are 5 models for the Manage Vocabulary database:

1. `User` - An extension of Django's `AbstractUser` model.
2. `Word` - Stores word names and sets each word name has a unique value.
3. `WordOnwership` - Creates a `OneToMany` relationship with `User` and a `OneToMany` relationship with `Word`for one word has many users. Stores `added_date` which will automictically store the current date.
4. `WordEntry` - Creates a `OneToMany` relationship with `User` and a `OneToMany` relationship with `Word`for one word has many users. Stores `word_type`, `definition`, `example` for each word and each user.
5. `Contact` - Stores `name`, `email`, `title`, `message`.

## Routes

### Index `/`

When a user is not logged in, it will display `index.html` from the `templates\manage_vocabulary` folder. Otherwise, it will display `index_user_is_authenticated.html`. On the latter page, it shows a list of links for the first letter of each distinct word in their vocabulary. When a user clicks on one of those links, it will scroll to the corresponding letter section and display a list of vocabulary words that begin with that letter.

### Authentication `/authentication`

I created a separate project named `authentication` to easily manage different tasks.

#### Login `/login`

User can log into the website using a valid username and password.

#### Register `/register`

User must enter their username, email address, first name, lastname, email, username, password and confirm password. The page has the following validation:

1. The password must match the confirm password field
2. There is no existing user with the username provided

If the details are valid, a new user is created in the `User` model with the `is_active` flag set to `False`. An email containing an activation link is automatically sent to the user's email.

#### Logout `/logout`

If the user clicks `Logout` in the navigation bar, it will log the user out and redirect to the [Index](#index) page

#### Validate Username `/validate-username`

This page is a function that is called by `register.min.js` to validate whether the username is unique. It responds with JSON data for the `register.min.js` file to display an error if the username is invalid.

#### Validate Email `/validate-email`

This page works in a similar way to [validate username](#validate-username), but it only checks for unique email addresses.

#### Active `/active`

When the user clicks on the link from an email after register successfully, it will check the token link and redirect to the [Login](#login) page.

#### Reset Password `/reset-password`

When a user forgets their password, they can click on the `/reset-password` link from the [Login](#login) page. It will display a form containing an email input where the user can type their email. Based on that email, the system will send a reset link with a unique token. It will continue redirect to `password_reset_send.html` from `templates/authentication`.

#### Password Reset Complete `/password-reset-complete`

When the user clicks on the link from an email, it will check the token link and redirect to the `password_reset_done.html` from `templates/authentication`.

### Add vocabulary `/dictionary/add-vocabulary`

From this page, users can create a new vocabulary word by providing a word name, part of speech, definition, example, and they can add multiple types of parts of speech or definitions for that word by clicking on the 'Add other definition' button. By using the 'click' event when a user clicks on the DOM element with the id `add_other_definition`, it will clone the div named `clone_div` and append it as a new child within the `form_entries` class. These functions manipulate from `add-new-definition.min.js` file. After clicked on the _Save_ button, it will redirect to the [Index](#index) page.

### Vocabulary edit `/dictionary/<word_name>vocabulary-edit`

From this page, users can easily edit their vocabulary word. After clicked on the _Save_ button, it will redirect to the [Index](#index) page.

### Search `/search`

That is the search page with the method `GET` which will get the word name and return the search result.

### History `/history`

This page displays list of word names base on each year and each month along with the total number of words for each month.

## How to run the application

1. Copy the repo to your system.
2. Verify you have Python, Django, Gulp, and Node.js installed on your system. If not you will need to install them.
3. To install all of the packages from `requirements.txt`, you need to run the command:
   ```
   pip install -r requirements.txt
   ```
4. Go to the directory `vocabulary/static` and run the command bellow:
   ```bash
   gulp
   ```

````
5. Go to the root directory of the Django project and run the following command to start up the web server:
   ```python
   python manage.py runserver
````
