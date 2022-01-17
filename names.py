from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'

db = SQLAlchemy(app)


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(100), default="Κανένας")

    def __repr__(self):
        return f"Calendar('{self.date}', '{self.name}')"


@app.route('/')
def home():
    if 'dt' in request.args:
        year = int(request.args['dt'].split("-")[0])
        month = int(request.args['dt'].split("-")[1])
        day = int(request.args['dt'].split("-")[2])
        return Calendar.query.filter(Calendar.date == datetime(year, month, day)).first().name
    else:
        return Calendar.query.filter(Calendar.date == datetime(datetime.today().year,
                                                               datetime.today().month,
                                                               datetime.today().day)).first().name


if __name__ == "__main__":
    app.run(debug=True)
