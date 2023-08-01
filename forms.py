from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name:', validators=[DataRequired()])
    recipe_description = TextAreaField('Description:', validators=[DataRequired()])
    recipe_ingredients = TextAreaField('Ingredients:', validators=[DataRequired()])
    recipe_directions = TextAreaField('Directions:', validators=[DataRequired()])
    recipe_servings = StringField('Servings:', validators=[DataRequired()])
    recipe_picture = FileField('Picture:', validators=[FileRequired()])

