from django import forms
from core.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Để lại bình luận",'class': "form-control"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']