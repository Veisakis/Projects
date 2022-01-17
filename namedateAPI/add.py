import pandas as pd
from names import db, Calendar
from datetime import date

df = pd.read_csv("calendar", sep=",")

db.drop_all()
db.create_all()
for i in range(df.shape[0]):
    db.session.add(Calendar(date=date.fromisoformat(df['date'][i]), name=df['name'][i]))

db.session.commit()
