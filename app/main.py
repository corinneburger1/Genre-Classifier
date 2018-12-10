# pythonspot.com
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, validators
import classify

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        if form.validate():
            try:
                query = request.form['name']
                flash(classify.classify(query))
            except:
                flash('Error: No song found.')
        else:
            flash('Error: All the form fields are required.')

    return render_template('index.html', form=form)

# if __name__ == "__main__":
#     app.run()
