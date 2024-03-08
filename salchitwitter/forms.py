from django import forms
from .models import Salchitweet

class TweetForm(forms.ModelForm):
    # we inherit from django's ModelForm
    body = forms.CharField(  # In this line we pass the field that you want the form to render.
        required=True,  # below lines creates the text area with bulma
        widget = forms.widgets.Textarea(attrs={
            "placeholder": "Salchitweet something funy...", 
            "class": "textarea is-success is-medium", }),
        label="Write here your SalchiTweet",
        )  
    
    class Meta:
        # with the Meta class we pass information that is not a model field, and will omit this when django
        # creates the form
        model = Salchitweet
        exclude = ("user", )  # add a coma after user, for python to creates a tuple