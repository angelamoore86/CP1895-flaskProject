from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from werkzeug.utils import secure_filename


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


app.config['UPLOAD_FOLDER'] = os.path.join('static', 'data_dir', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir', '')


def load_data(recipe_file):
    if os.path.exists(recipe_file):
       return pd.read_csv(recipe_file)
    return pd.DataFrame(columns=['Name', 'Ingredients', 'Instructions', 'Servings'])


def image_file(filename):
    if request.method == "POST":
        return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recipes')
def recipes():
    recipe_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.csv')]
    recipes = []
    for file in recipe_files:
        df = load_data(os.path.join(app.config['UPLOAD_FOLDER'], file))
        recipes.append(df)
    return render_template('recipes.html', recipes=recipes)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        servings = request.form.get('servings')
        image = request.files['image'] if 'image' in request.files else None

        if name and ingredients and instructions and servings:
            recipe_data = {
            'Name': [name],
            'Ingredients': [ingredients],
            'Instructions': [instructions],
            'Servings': [servings]
            }
            recipe_df = pd.DataFrame(recipe_data)

            if image and image_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['SUBMITTED_IMG'], filename))
                recipe_df['Image'] = [filename]

            recipe_file = os.path.join(app.config['UPLOAD_FOLDER'], f'{name.lower()}.csv')
            recipe_df.to_csv(recipe_file, index=False)
            return redirect(url_for('recipes'))

    return render_template('upload.html')


@app.route('/delete/<recipe_name>', methods=['GET', 'POST'])
def delete(recipe_name):
    recipe_file = os.path.join(app.config['UPLOAD_FOLDER'], f'{recipe_name.lower()}.csv')
    if os.path.exists(recipe_file) and request.method == 'POST':
        os.remove(recipe_file)
        return redirect(url_for('recipes'))
    return render_template('delete.html', recipe_name=recipe_name)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        search_results = []

        if keyword:
            recipe_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.csv')]
            for file in recipe_files:
                df = load_data(os.path.join(app.config['UPLOAD_FOLDER'], file))
                filtered_df = df[df.apply(lambda row: keyword.lower() in row['Name'].lower() or keyword.lower() in row['Ingredients'].lower(), axis=1)]
                if not filtered_df.empty:
                    search_results.append(filtered_df)

            return render_template('search.html', keyword=keyword, search_results=search_results)

    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
