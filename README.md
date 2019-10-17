# Amazon Price Tracker

Email: amz.price.tracker.2019@gmail.com

(BeautifulSoup/Scrapy + SQLite/MongoDB + Flask)

- SQLite: serverless, lightweight, embedded
  - sqlite3 comes with Python installed
  - DBeaver GUI: universal database system, supporting all major RDBS such as MySQL, PostgreSQL, Oracle, SQL Server, SQLite, ...
  
- Heroku (deployment): (Heroku uses Postgres as its database)

  <b>git push heroku master</b>

  <b>git remote -v</b>

  1. Download Heroku CLI (Command Line Interface): to create and manage your Heroku app directly from terminal

  2. In terminal: <b>heroku login</b> or <b>heroku login -i</b>

  3. Add all dependencies: <b>pip freeze > requirements.txt</b>

  4. Add a **Procfile**: (so as Heroku knows how to execute the application)

     3.1. Before adding a Procfile, need to install a web server called Gunicorn (pip install gunicorn)

     3.2. Create a new file Procfile as the name and no extension. 

     Add this: <b>web: gunicorn app:app</b> (app:app specifies the module and application name; the first 'app' is the name of the script that launches Flask, i.e. app.run()) and <b>release: python db.py db upgrade</b> to populate the table schema from the database migration file into Heroku database

  5. Database: 