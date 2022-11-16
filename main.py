from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from csv import reader

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired(), URL()])
    open = StringField("Opening Time", validators=[DataRequired()])
    closing = StringField("Closing Time", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=[(0, ''), (1, '☕'), (2, '☕☕'), (3, '☕☕☕'),
                                                          (4, '☕☕☕☕'), (5, '☕☕☕☕☕')])
    wifi_rating = SelectField("WiFi Strength Rating", choices=[(0, ''), (1, '💪'), (2, '💪💪'), (3, '💪💪💪'),
                                                               (4, '💪💪💪💪'), (5, '💪💪💪💪💪')])
    power_rating = SelectField("Power Rating", choices=[(0, ''), (1, '🔌'), (2, '🔌🔌'), (3, '🔌🔌🔌'),
                                                        (4, '🔌🔌🔌🔌'), (5, '🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', newline='', encoding='UTF8') as csv_file:
            coffee_rating = int(form.coffee_rating.data) * '☕'
            wifi_rating = int(form.wifi_rating.data) * '💪'
            power_rating = int(form.power_rating.data) * '🔌'
            csv_file.write(f"\n{form.cafe.data}," 
                           f"{form.location.data}," 
                           f"{form.open.data}," 
                           f"{form.closing.data},"
                           f"{coffee_rating}," 
                           f"{wifi_rating}," 
                           f"{power_rating}")
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
