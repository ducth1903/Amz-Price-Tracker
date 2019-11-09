# Amazon Price Tracker

Email: amz.price.tracker.2019@gmail.com

(BeautifulSoup/Scrapy + SQLite for initial dev, but then switch to PostgreSQL for local dev and PostgreSQL for production + Flask)

To run the app:

- Make sure PostgreSQL database is created in your system (i.e. locally, use DBeaver to create db), then type: **flask create_tables** to create tables (schema) for databases (i.e. products, prices, emails). This is implemented from Web_app/commands.py. Normally, we need to create from cmd by importing db and models, then db.create_all(). *Note: before doing this, we may need to manually **create database <name_db>** from postgresql cmd*
- **flask run** or **python run.py**: to run the web app
- **python main_tracker.py**: to run the scraping
- **NOTE**: Error in db_utils ("Multiple classes on path..."). To solve this, comment out the db.relationship() portions in db_utils as these only use when initializing relationship of tables.
- To run script on Heroku:
  - Add **worker: python <path-to-script>** on Procfile
  - Commit and push to Heroku
  - Type this in local command line: **heroku ps:scale worker=1** (only need to do once at first)
- To run debug locally: app.run(host='0.0.0.0') then python run.py and access with machine's IP address. Otherwise, in production, app.run(), type flask run

---

- Flask-Migrate explained: http://www.patricksoftwareblog.com/relational-database-migrations-using-flask-migrate/

- SQLite: serverless, lightweight, embedded
  - sqlite3 comes with Python installed
  - DBeaver GUI: universal database system, supporting all major RDBS such as MySQL, PostgreSQL, Oracle, SQL Server, SQLite, ...
  
- .env: to store private key; .flaskenv: to store public key. The whole idea is instead of running "export ..." for each machine that runs the app, these files will configure the environment variables to run the app. **Make sure the .env file is not committed to Git as it is not supposed to be shared...**

  ---

- PostgreSQL (installed locally): pass is postgres

  - pgAdmin
  - psql command line

- Heroku (deployment): (Heroku uses Postgres as its database)

  <b>git push heroku master</b>

  <b>git remote -v</b>

  <b>heroku open; heroku ps</b> (check dyno hours on Heroku)

  **heroku run bash**: to run bash on heroku server from local machine

  1. Download Heroku CLI (Command Line Interface): to create and manage your Heroku app directly from terminal

  2. In terminal: <b>heroku login</b> or <b>heroku login -i</b>

  3. Add all dependencies: <b>pip freeze > requirements.txt</b>

  4. Add a **Procfile**: (so as Heroku knows how to execute the application)

     3.1. Before adding a Procfile, need to install a web server called Gunicorn (pip install gunicorn)

     3.2. Create a new file Procfile as the name and no extension. 

     Add this: 

     <b>web: gunicorn app:app</b> (app:app specifies the module and application name; the first 'app' is the name of the script that launches Flask, i.e. app.run()) **(NOTE: script to launch Flask has to be at the root directory)**, and 

     <b>release: python db.py db upgrade</b>.  The command *db upgrade* populates the table schema from the database migration file into Heroku database

  5. **Migrate**: (to update database's schema in the future)
  
     1. python manage.py db init: create migrations folder 
   2. python manage.py db migrate
     3. python manage.py db upgrade
  
     