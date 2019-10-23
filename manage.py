from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from Web_app import app, db

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Initialize the manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()