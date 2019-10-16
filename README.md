# Amazon Price Tracker

Email: amz.price.tracker.2019@gmail.com

(BeautifulSoup/Scrapy + SQLite/MongoDB + Flask)

- SQLite: serverless, lightweight, embedded
  - sqlite3 comes with Python installed
  - DBeaver GUI: universal database system, supporting all major RDBS such as MySQL, PostgreSQL, Oracle, SQL Server, SQLite, ...
  
- Heroku (deploy):

  1. Download Heroku CLI (Command Line Interface): to create and manage your Heroku app directly from terminal

  2. In terminal: <b>heroku login</b> or <b>heroku login -i</b>

  3. Add all dependencies: <b>pip freeze > requirements.txt</b>

  4. Add a Procfile: 

     3.1. Before adding a Procfile, need to install a web server called Gunicorn (pip install gunicorn)

     3.2. Create a new file Procfile as the name and no extension. Add this: <b>web: gunicorn app:app</b> and <b>release: python db.py db upgrade</b> to populate the table schema from the database migration file into Heroku database 

  5. Now we are ready for deployment: heroku create <name-application>. The output will be Heroku git remote repository where our application lives on Heroku. We then have to push our application to the master branch.

  6. Database: 