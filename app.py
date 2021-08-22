from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cache.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDoItem(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        upcoming_entry = ToDoItem(title=title, desc=desc)
        db.session().add(upcoming_entry)
        db.session().commit()

    return render_template('index.html', todolist=ToDoItem.query.all())

@app.route("/delete/<int:sno>")
def delete(sno):
    deleted_kaam = ToDoItem.query.filter_by(sno=sno).first()
    db.session().delete(deleted_kaam)
    db.session().commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        updated_kaam = ToDoItem.query.filter_by(sno=sno).first()
        updated_kaam.title = title
        updated_kaam.desc = desc
        db.session().add(updated_kaam)
        db.session().commit()
        return redirect("/")
    
    updated_kaam = ToDoItem.query.filter_by(sno=sno).first()
    return render_template('update.html', updated_kaam=updated_kaam)

if __name__ == '__main__':
    app.run(debug=False, port=8000)