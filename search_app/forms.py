from django import forms 
from .models import Product 

class SearchForm(forms.Form): 
    query = forms.CharField( 
        label='検索キーワード', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'})    
    ) 

class ProductForm(forms.ModelForm): 
    class Meta: 
        model = Product 
        fields = ['name', 'description', 'price', 'category','thumbnail'] 

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
