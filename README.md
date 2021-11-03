# Libman
#### Description:
```
libman is a library management web application with flask
```
I usually buy and lend a lot of books,
so I needed a program to manage my library,
and I chose this idea for the final project.

Libman was created using this technology and languages:
- flask
- python
- sqlite3
- javascript
- jQuery
- html
- css
- bootstrap

Libman consists of several parts,
First, welcome to user and a brief description about the project and a famous quote,
then user should register on the site and logs in.
my forms doesn't used the GET method, which includes our form’s data in the URL

as said in cs50 Sessions are how web servers remembers information about each user,
which enables features like allowing users to stay logged in. I also use sessions in this project and
In Flask, we can use the flask_session library to manage this for us.
We’ll configure the session library to use the IDE’s filesystem, and use session like a dictionary to store a user’s name.
It turns out that Flask will use HTTP cookies for us,
to maintain this session variable for each user visiting our web server.
Each visitor will get their own session variable, even though it appears to be global in our code.
For our default ** / ** route, we’ll redirect to ** /welcome ** if there’s no name set in session for the user yet, and otherwise show a default html template.

The error message template, meanwhile, will just display the message:
then there are multiple choice:
** Add **
in the /add
user can Add books to his library and in add page,
user should insert title and author of the book, Once we’ve validated the request, we can use INSERT INTO to add a row,
if user post empty value error should be thrown to user.
when user click the button data will be post to database and will be saved.
then he will be redirect to My library in / route and could see books in the library
add use
** remove **
in the /remove
when user want to remove a book just enter the title of the book and book will be removed
from the library with a sql query and user will be redirect to home page.

**lend**
in the /lend
user also can lend book to a friend or someone, user put the title of the book and the name of
person that wanna lend the book to, then server check that if user doesn't has that book error should be handeld to user.
Once we’ve validated the request, we can use INSERT INTO to add a row,
and after lend user should be redirect to lended page which could see a page log for books he lended to people.

**lended**
in the /lended
in lended user could see a list of books that he lended to people.

**search**
in the /search
in search he could instantly search for books in his library by searching title or author.
With JavaScript, we can show a partial list of results as we type.
We’ll use another library, JQuery, to make requests more easily.
We’ll listen to changes in the input element, and use $.get, which calls a JQuery library function to make a GET request with the input’s value.
Then, the response will be passed to an anonymous function as the variable shows, which will set the DOM with generated <li> elements based on the response’s data.
$.get is an AJAX call, which allows for JavaScript to make additional HTTP requests after the page has loaded,
to get more data.Since the network request might be slow, the anonymous function we pass to $.get is a callback function,
which is only called after we get a response from the server. In the meantime, the browser can run other JavaScript code.

**about**
in the /about
in about user could see a about this project and a little about me!

and also first time user logged in see **welcome** which user 3d party api for quote

for the front end I use the format of [cs50 finance](https://cs50.harvard.edu/x/2021/psets/9/finance/). problem set!

**about layouts: **

In html pages we have some repeated HTML code. With just HTML,
we aren’t able to share code between files, but with Flask templates (and other web frameworks), we can factor out such common content.
so I use jinja for layout and Flask supports Jinja, a templating language, which uses the {% %} syntax to include placeholder blocks,
or other chunks of code. Here we’ve named our block body since it contains the HTML that should go in the <body> element.

**css**
as brian said : It turns out that there are many libraries that other people have already written that can make the styling of a webpage even simpler.
One popular library that we’ll use throughout the course is known as bootstrap. also bootstrap used here.
