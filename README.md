![Logo](./static/logo.png)

# BLOG

A place to share your thoughts with like-minded individuals

## Description

BLOG is a full-stack web application that allows you to:

- Create an account.
- Customize your profile.
- Write posts and share them on a global wall.
- Remove previously published posts.
  BLOG's structure is divided into two main aspects: the front-end implemented using HTML5, Tailwindcss, and JavaScript, and the backend where the application logic is managed via Flask, an easy to learn python framework for developing web servers, and the data is stored in a MongoDB database.

Both aspects are explained in more detail in the next section.

## Dissection

### Front-end

In the project folder you'll find a directory `templates/` which holds the project's HTML files, each file represents a page in the website as follows:

- **`layout.html`** is the main **template** for the pages the user can view _before_ they log into their account. it contains the pages' global metadata (icon, stylesheets, external fonts, etc.) a navbar and Jinja placeholders for the `<title>` and `<main>` blocks whose values depend on the page the user is currently on.

- **`layout_logged.html`** is another **template** but for the pages the user can view _after_ they have logged into their account. with a slight difference in the appearance of the navbar.

- **`index.html`** is the page you are first greeted with when you navigate to the website's url. It contains navigation links to the **register** and **login** pages.

- **`register.html`** allows new visitors to create accounts on the website by filling the following fields:

  - username
  - email
  - password
  - re-enter passpord
    The data entered is then sent to the server and validated before getting stored in the database.

- **`login.html`** allows each user to log into their account and enjoy the website's full features.

- **`feed.html`** is considered the _home_ page for logged users. It's where all users' posts are grouped and displayed according to their publish date descendingly (Top -> recent, Bottom -> earlier). Each post is displayed in a `<div>` which includes: - author's pfp - author's username - publish date - body (text)
  with each request to this page the database is queried to display all stored posts.
- **`editor.html`** simply contains a `<textArea>` to write the post body in and a `<button>` of `type='submit'` to send the text to the server, perform some processing, store in the database and finally display it on the **feed** page.
- **`profile.html`** is the user profile where they can display their details including their:
  - username
  - description
  - profile picture
  - cover picture
  - previously published posts
    The user can then add/edit their description through a hidden `<textArea>` that is displayed when the user clicks on the **edit description** icon.

This concludes the website **pages** that are displayed to the user. Next, is the eapplication logic executed behind the scenes.

### Back-end

As mentioned, the back-end is divided into two sections. The application logic, mainly implemented in `app.py` and the data stored in a mongoDB database.

**`app.py`** is the python program resposible for: routing requests, validation, verification, processing, and more. It provies the user with the ablitity to communicate with the server using **http** protocol. The program also utilises several functionalities from external libraries which are all included in the `requirements.txt` file in the project folder. Inisde `app.py` there are multiple functions help this application become more dynamic and achieve its purpose including:

- **`@app.route('/path', methods)`**: A built-in decorator function that takes a route path from a request the user made through a link `<a href='/path'>` or possibly a form `<form action='/path'>` after the request had been routed to this function, the decorated function is then executed.

- **`@login_required(route_function)`**: Another decorator function (user-defined). this function doesn't allow the execution of the decorated function until the user has logged into their account. If the user requests a page route that is wrapped by the `login_required()` function, they will be redirected to `login.html` where they will be prompted to login first. This functions performs its validation by checking if the user's **username** is stored in the `session` variable.

Each route in the application has its own function that receives the user request and does the and does the needed processessing, validation, verification, and database querying. The `def login():` function for example:

- If the route was requested using `GET`, the server checks if the user's username is stored in the `session` variable. If it is indeed stored, this means the user is logged in and is redirected to the `/feed` path (the home page for logged in users).
- If the request was made using `POST`, that means the user is trying to login. The server then checks if the user had entered their email and their password, if not, an error message "_Must Enter Email Address_" and "_Must Enter Password_".
- After the server has ensured the email and password have not been left blank, it hashes the password then compares the user-provided info with the documents in the database. If a match is found, the user's username gets stored in the session variable. If not, the login page is reloaded with an added error message "_Wrong Email Or Password_".

[!TIP]
Along with project files, in the `data/` directory, you will find 2 JSON files containing 2 MongoDB collections **blog.users.json** and **blog.posts.json** for you to quickly the application logic.

## Run Locally

Clone the project

```bash
  git clone https://github.com/SharqyCode/Blog-CS50-Final-Project.git
```

Go to the project directory

```bash
  cd Blog-CS50-Final-Project-master
```

Open Visual Studio Code in your project's folder.

Open Python terminal:

<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>

In the terminal, run the following:

```keyboard
python -m venv venv
source venv/bin/activate
```

Install project dependencies

```bash
  pip Install -r requirements.txt
```

Install Tailwindcss. note that `tailwindc.config.js` file already exists.

```bash
  npm install -D tailwindcss
```

To run the server, type in the terminal

```bash
  flask run
```

or

```bash
  python -m flask run
```

## Project Demo

[Demo](https://youtu.be/ktU7fFlNp1I)
