from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe location on Google maps (URL)", validators=[DataRequired(), URL()])
    open = StringField("Opening time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing time e.g. 5:30 PM", validators=[DataRequired()])
    cofeeRating = SelectField("Cofee rating", choices=["1", "2", "3", "4", "5"], validators=[DataRequired()])
    wifiRating = SelectField("Wifi strength rating", choices=["1", "2", "3", "4", "5"], validators=[DataRequired()])
    powerRating = SelectField("Power socket availability", choices=["1", "2", "3", "4", "5"], validators=[DataRequired()])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a") as csvFile:
            csvFile.write(
                f"\n{form.cafe.data},"
                f"{form.location.data},"
                f"{form.open.data},"
                f"{form.close.data},"
                f"{form.cofeeRating.data},"
                f"{form.wifiRating.data},"
                f"{form.powerRating.data},"
            )
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
