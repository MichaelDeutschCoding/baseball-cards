from app.models import Comment, Offer
from django.forms import ModelForm, Select, NumberInput
from django.forms.widgets import Textarea

class CreateOfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['card', 'price']
        widgets = {
            'card': Select(attrs={'class': "form-control w-75"}),
            'price': NumberInput(attrs={'class': "form-control w-75"})
        }

class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': Textarea(attrs={'class': "form-control w-75"})}

