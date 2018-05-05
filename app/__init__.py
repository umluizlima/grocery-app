import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(app.instance_path, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app.model import db, ma, migrate
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from app.controller import main, api
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)

    app.add_url_rule('/', endpoint='index')

    return app


'''
app = Flask(__name__)
# Configs
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
        'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB
db = SQLAlchemy(app)
# Object serialization
ma = Marshmallow(app)
# DB Migration
migrate = Migrate(app, db)


# Models
class Item(db.Model):
    ""
    CREATE: db.session.add(item) -> db.session.commit()
    READ: Item.query.all() or Item.query.filter_by(key=value).first()
    UPDATE: item = Item.query.filter_by(key=value).first() -> item.key = value\
    -> db.session.commit()
    DELETE: db.session.delete(item) -> db.session.commit()
    ""
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
    return render_template('index.html', title="Compras Natércia")


@app.route('/list', methods=["POST"])
def create_item():
    data = request.get_json()
    if 'content' not in data.keys():
        abort(400)
    item = Item(content=data['content'])
    db.session.add(item)
    db.session.commit()
    return ItemSchema().jsonify(item)


@app.route('/list', methods=["GET"])
def read_items():
    items = ItemSchema(many=True).dump(Item.query.all()).data
    return jsonify(sorted(items, key=itemgetter('done')))


@app.route('/list/<int:id>', methods=["GET"])
def read_item(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return abort(404)
    return ItemSchema().jsonify(item)


@app.route('/list/<int:id>', methods=["PUT"])
def update_item(id):
    print("Entrou no PUT")
    item = Item.query.filter_by(id=id).first()
    print(item)
    if not item:
        return abort(404)
    data = request.get_json()
    print(data)
    if 'content' not in data.keys() or 'done' not in data.keys():
        return abort(400)
    item.content = data['content']
    item.done = data['done']
    db.session.commit()
    return ItemSchema().jsonify(item)


@app.route('/list/<int:id>', methods=["DELETE"])
def delete_item(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return abort(404)
    db.session.delete(item)
    db.session.commit()
    return "", 204
'''
