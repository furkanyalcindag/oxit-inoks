from django import forms
from django.forms import ModelForm

from inoks.models import Profile

CHOICES_WITH_BLANK = (
    ('', '--------'),

)


class ProfileForm(ModelForm):
    isContract = forms.BooleanField(required=True)

    class Meta:
        model = Profile

        fields = (
            'profileImage', 'address', 'mobilePhone', 'gender', 'tc', 'birthDate', 'job', 'city', 'educationLevel',
            'sponsor', 'district', 'isContract', 'iban','ibanAdSoyad')
        widgets = {
            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'placeholder': 'Adres', 'rows': '2', 'required': 'required'}),
            'mobilePhone': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Telefon Numarası', 'required': 'required',
                       'maxlength': '10', 'minlength': '10'}),
            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),
            'tc': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'T.C. Kimlik Numarası', 'required': 'required',
                       'maxlength': '11', 'minlength': '11'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'type': 'date', 'autocomplete': 'off',
                       }),

            'sponsor': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; ', 'required': 'required'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required', "onChange": 'ilceGetir()'}),

            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id'}
                                     ),

            'job': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                       'style': 'width: 100%;', 'required': 'required'}),

            'educationLevel': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                  'style': 'width: 100%;', 'required': 'required'}),

            'iban': forms.TextInput(
                attrs={'class': 'form-control iban', 'placeholder': 'iban',

                       'required': 'required',
                       'maxlength': '11', 'minlength': '11'}),
            'ibanAdSoyad': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Hesap Adı ve Soyadı', 'required': 'required'

                       })

        }
