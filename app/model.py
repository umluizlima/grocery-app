from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


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
