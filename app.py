import os
from flask import Flask, render_template, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from operator import itemgetter

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Configs
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
        'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB
db = SQLAlchemy(app)
ma = Marshmallow(app)
# DB Migration
migrate = Migrate(app, db)


# Models
class Item(db.Model):
    """
    CREATE: db.session.add(item) -> db.session.commit()
    READ: Item.query.all() or Item.query.filter_by(key=value).first()
    UPDATE: item = Item.query.filter_by(key=value).first() -> item.key = value\
    -> db.session.commit()
    DELETE: db.session.delete(item) -> db.session.commit()
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Item {self.id}>"


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'done')


# Views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list', methods=["GET"])
def read_items():
    items = ItemSchema(many=True).dump(Item.query.all()).data
    return jsonify(sorted(items, key=itemgetter('done')))


@app.route('/list', methods=["POST"])
def create_item():
    return "POST on /list"


@app.route('/list/<int:id>', methods=["GET"])
def read_item(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return abort(404)
    return ItemSchema().jsonify(item)


@app.route('/list/<id>', methods=["PUT"])
def update_item(id):
        return f"PUT on /list/{id}"


@app.route('/list/<id>', methods=["DELETE"])
def delete_item(id):
        return f"DELETE on /list/{id}"


if __name__ == '__main__':
    app.run(host='localhost',
            port=5000,
            debug=True)
