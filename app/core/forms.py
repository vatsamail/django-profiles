from django import forms
from core.models import Post

#forms.Form is an unbound form
#forms.ModelForm is a bound form

class HomeForm(forms.ModelForm):
    #post = forms.CharField(required=True)
    post = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write a post ...',
        }
    ))

    class Meta:
        model = Post
        fields = ('post', )
