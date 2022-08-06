from .models import *
from django import forms


class createListing(forms.ModelForm):
    class Meta:
        model = listing
        fields = ['title', 'description', 'image', 'category']
        widgets = {
            'image': forms.URLInput(attrs={
                'placeholder': "Image's url",
            })
        }

class createBid(forms.ModelForm):
    class Meta:
        model = bid
        fields = ['bid']

class createComment(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(),
        }