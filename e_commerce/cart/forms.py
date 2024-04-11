from django import forms
from users.models import CustomUser

class CheckoutForm(forms.ModelForm):
    class Meta:
        model =CustomUser
        fields = ['full_name', 'address', 'pincode'] 