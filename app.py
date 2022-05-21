from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from marshmallow import Schema, fields, post_load
from bson import objectid


app = Flask(__name__)
app.config['MONGODB_DB'] = 'authors'
db = MongoEngine(app)

Schema.TYPE_MAPPING[objectid] = fields.String

class Authors(db.Document):
    name = db.StringField()
    specialisation = db.StringField()


class AuthorsSchema(Schema):
    name = fields.String(required=True)
    specialisation = fields.String(required=True)


@app.route('/authors', methods=['GET'])
def index():
    get_authors = Authors.objects.all()
    author_schema = AuthorsSchema(
        many=True,
        only=['id', 'name', 'specialisation']
    )
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))


if __name__ == "__main__":
    app.run(debug=True)
