from database import db, ma
from sqlalchemy_json import NestedMutableJson
from sqlalchemy import func

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String)
    parameters = db.Column(NestedMutableJson)
    data_parameters = db.Column(NestedMutableJson)
    solution = db.Column(NestedMutableJson)
    solution_path_file = db.Column(db.String)
    creation_date = db.Column(db.TIMESTAMP(timezone=True), server_default=func.now())
    last_edit = db.Column(db.TIMESTAMP(timezone=True))
    file_solution_text = db.Column(db.String)

class ModelSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "name", "parameters", "solution", "data_parameters", "creation_date", "last_edit", "solution_path_file", "file_solution_text")
        model = Model

model_schema = ModelSchema()
models_schema = ModelSchema(many=True)