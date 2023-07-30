from flask import Flask, redirect, url_for, request, render_template
from forms import RecipeForm
from werkzeug.utils import secure_filename
import pandas as pd
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir', '')


@app.route('/')
def welcome_greeting():
    """
    Function Welcoming for main page
    :return:
    """
    return render_template('index.html')


@app.route('/add_recipe', methods=['POST', 'GET'])
def add_recipe():
    """
    Function to add recipe
    :return:
    """
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        recipe_description = form.recipe_description.data
        recipe_ingredients = form.recipe_ingredients.data
        recipe_directions = form.recipe_directions.data
        recipe_servings = form.recipe_servings.data
        pic_filename = recipe_name.lower().replace(" ", "_") + '.' + secure_filename(form.recipe_picture.data.filename).split(".")[-1]
        form.recipe_picture.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        df = pd.DataFrame([{'name': recipe_name, 'description': recipe_description, 'ingredients': recipe_ingredients, 'directions': recipe_directions, 'servings': recipe_servings, 'picture': pic_filename}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        print(df)
        return redirect(url_for('hello_world'))
    else:
        return render_template('add_recipe.html', form=form)


@app.route('/display_recipe/<name>')
def render_information(name):
    df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + name.lower().replace(" ", "_") + '.csv'), index_col=False)
    return render_template('view_recipe.html', recipe=df.iloc[0])


@app.route('/input', methods=['POST', 'GET'])
def information():
    if request.method == 'POST':
        info = request.form['info']
        return redirect(url_for('hello_guest', guest=info))
    else:
        return redirect(url_for('welcome_greeting'))


if __name__ == '__main__':
    app.run(debug=True)
