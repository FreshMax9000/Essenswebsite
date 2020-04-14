from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django import forms
from django.forms.models import inlineformset_factory
from django.forms.models import ModelForm

from . import custom_ingredient_layout
from . import models


class CreateIngredientForm(ModelForm):

    class Meta:
        model = models.Ingredient
        exclude = ('recipe',)


class CreateRecipeForm(ModelForm):

    class Meta:
        model = models.Recipe
        exclude = ('author', 'avg_rating')

    def __init__(self, *args, **kwargs):
        super(CreateRecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                Field('description'),
                Field('preparation'),
                Field('work_time'),
                Fieldset('Add titles',
                         custom_ingredient_layout.IngredientFormset('ingredients')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )


CreateIngredientFormset = inlineformset_factory(
    models.Recipe, models.Ingredient, form=CreateIngredientForm,fields=['grocerie', 'quantity'],
    extra=1, can_delete=True)
