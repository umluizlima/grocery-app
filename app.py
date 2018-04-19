import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Configs
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB
db = SQLAlchemy(app)
# DB Migration
migrate = Migrate(app, db)

# Models
class Item(db.Model):
    """
    CREATE: db.session.add(item) -> db.session.commit()
    READ: Item.query.all() or Item.query.filter_by(key=value).first()
    UPDATE: item = Item.query.filter_by(key=value).first() -> item.key = value -> db.session.commit()
    DELETE: db.session.delete(item) -> db.session.commit()
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Item {self.id}>"

# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list', methods=["GET", "POST"])
def list():
    if request.method == "POST":
        return "POST on /list"
    else:
        return "GET on /list"

@app.route('/list/<id>', methods=["GET", "PUT", "DELETE"])
def list_id(id):
    if request.method == "PUT":
        return f"PUT on /list/{id}"
    elif request.method == "DELETE":
        return f"DELETE on /list/{id}"
    else:
        return f"GET on /list/{id}"

if __name__ == '__main__':
    app.run(host='localhost',
            port=5000,
            debug=True)
