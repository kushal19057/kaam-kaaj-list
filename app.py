from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///kaam.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class KaamKaaj(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self)->str:
        return f"Kaam #{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        upcoming_entry = KaamKaaj(title=title, desc=desc)
        db.session().add(upcoming_entry)
        db.session().commit()
        print(request.form)

    return  render_template('index.html', all_kaam=KaamKaaj.query.all())

# @app.route("/delete/<int:sno>")
# def delete():
#     deleted_kaam = KaamKaaj.query.filter_by(sno=sno).first()
#     db.session().delete(deleted_kaam)
#     db.session().commit()
#     return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=8000)