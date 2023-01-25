from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#CREATE DB TABLE MODEL
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable = False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} : {self.description}"


@app.route('/')
def index():
    return "Welcome to the DRINKS API. To view all available drinks data, just add /drinks to the url"

#QUERY ALL DRINKS IN TABLE AND DISPLAY INFORMATION FOR EACH
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)

    return{"drinks": output}

#SEARCH FOR SPECIFIC DRINK USING ID
@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return ({"name": drink.name, "description": drink.description})

#ADD A NEW DRINK
@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id, 'name': drink.name}

#DELETE A DRINK USING ID
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "Drink not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "Drink successfully removed"}
