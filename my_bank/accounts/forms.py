
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constants import ACCOUNT_TYPE, GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserBankAccount, UserAddress

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'account_type', 'birth_date', 'gender', 'street_address', 'postal_code', 'city', 'country']

        # form.save()
    
    def save(self, commit=True):
        our_user = super().save(commit=False) # ami databse e data save korba na akhon
        if commit == True:
            our_user.save() # user model e data save korlam
            account_type = self.cleaned_data.get('account_type')
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            street_address = self.cleaned_data.get('street_address')
            postal_code = self.cleaned_data.get('postal_code')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')

            UserAddress.objects.create(
                user = our_user,                
                street_address = street_address,
                postal_code = postal_code,
                city = city,
                country =country,
            )

            UserBankAccount.objects.create(
                user = our_user,
                account_type = account_type,
                account_no = 100000+ our_user.id,
                birth_date = birth_date,
                gender = gender                
            )
        return our_user