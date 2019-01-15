from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if email in User.objects.values_list('email', flat=True):
            raise forms.ValidationError("This email already belongs to another account")
        return email

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        if '@' in username:
            raise forms.ValidationError("This @ special charater is not allowed")
        else:
            return username

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('purchased', 'returned', 'store')

class PrintTagItemsForm(forms.ModelForm):
    class Meta:
        model = PrintTagItems
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ReturnPolicyForm(forms.ModelForm):
    class Meta:
        model = ReturnPolicy
        fields = '__all__'
