from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["MAIL_SERVER"] = os.getenv("HOST")
app.config["MAIL_PORT"] = os.getenv("PORT")
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")

db = SQLAlchemy(app)
mail = Mail(app)


# Make database model
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        occupation = request.form["occupation"]

        # Insert data in the database
        form = Form(first_name=first_name, last_name=last_name, email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        msg_body = (f"Thank you for your submission {first_name}.\n\n"
                    f"Here are your data: \n{first_name}\n{last_name}\n{date}\n"
                    f"Thank you !")

        message = Message(subject='New Form Submission',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email],
                          body=msg_body)
        mail.send(message)

        flash("Your form was submitted successfully", "succes")

    return render_template("index.html")


if __name__ == '__main__':
    with app.app_context():
        # check if exists database, if not create it
        db.create_all()
        app.run(debug=True, port=5001)
