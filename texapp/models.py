from django.db import models
from django.forms import ModelForm, TextInput, CheckboxInput, Textarea, DateInput, ChoiceField, Select, RadioSelect

from django.contrib.auth.models import User

import datetime

# user profiles:
# Extending User Model Using a One-To-One Link

class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # letter info
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    street_number = models.IntegerField()
    zip_code = models.IntegerField()
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class ProfileUserForm(ModelForm):
    class Meta:
        model = ProfileUser
        #fields = '__all__'  
        exclude = ['user']
        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': '', 
                'class': 'form-control'
            }),
            'last_name': TextInput(attrs={
                'placeholder': '',
                'class': 'form-control',
            }),
            'street_address': TextInput(attrs={
                'placeholder': '', 
                'class': 'form-control'
            }),
            'street_number': TextInput(attrs={
                'type': 'number',
                'placeholder': '', 
                'class': 'form-control'
            }),
            'zip_code': TextInput(attrs={
                'type': 'number',
                'placeholder': '', 
                'class': 'form-control'
            }),
            'city': TextInput(attrs={
                'placeholder': '', 
                'class': 'form-control'
            })
        }

# texapp

class ProfileAddressee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    # also for letter
    first_name = models.CharField(max_length=20)
    preferred_name = models.CharField(max_length=20, blank=True)
    formal_relationship = models.BooleanField()
    salutation = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    street_number = models.IntegerField()
    zip_code = models.IntegerField()
    city = models.CharField(max_length=50)

    def __str__(self):
        if self.formal_relationship:
            str = '%s %s %s' % (self.salutation, self.first_name, self.last_name)
        else: 
            if self.preferred_name:
                str = '%s "%s" %s' % (self.first_name, self.preferred_name, self.last_name)
            else:
                str = '%s %s' % (self.first_name, self.last_name)
        return str

class AddresseeForm(ModelForm):
    class Meta:
        model = ProfileAddressee
        #fields = '__all__'
        exclude = ['user']
        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': '', 
                'class': 'form-control'
            }),
            'formal_relationship': CheckboxInput(attrs={
                'class': 'form-check',
            }),
            'salutation': TextInput(attrs={
                'placeholder': 'Ms', 
                'style': 'width: 300px;', 
                'class': 'form-control'
            }),
            'last_name': TextInput(attrs={
                'placeholder': '', 
                'class': 'form-control'
            }),
            'street_address': TextInput(attrs={
                'placeholder': '', 
                'class': 'form-control'
            }),
            'street_number': TextInput(attrs={
                'placeholder': '', 
                'type': 'number', 
                'class': 'form-control'
            }),
            'zip_code': TextInput(attrs={
                'placeholder': '', 
                'type': 'number',
                'class': 'form-control'
            }),
            'city': TextInput(attrs={
                'placeholder': '', 
                'class': 'form-control'
            })
        }

class Letter(models.Model):
    addressee = models.ForeignKey(ProfileAddressee, on_delete=models.CASCADE, blank=True, null=True, default='') 

    reference = models.CharField(max_length=100)
    reference_bit = models.BooleanField()
    greeting = models.CharField(max_length=50, blank=True, default='Dear')
    body = models.CharField(max_length=1000)
    sign_off = models.CharField(max_length=50, blank=True, default='Best')
    ps = models.CharField(max_length=250, blank=True, default='') 
    enclosed = models.CharField(max_length=100, blank=True, default='')
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return '%s' % (self.reference)

    class Admin:
        pass

class LetterForm(ModelForm):
    class Meta:
        model = Letter
        fields = '__all__'
        #fields = ['reference', 'reference_bit', 'salutation', 'body', 'sign_off', 'ps', 'enclosed', 'date']
        #exclude = ['addressee']
        widgets = {
            'addressee': RadioSelect(attrs={
                'placeholder': '', 
            }),
            'reference': TextInput(attrs={
                'placeholder': '', 
                'class': 'form-control'
            }),
            'reference_bit': CheckboxInput(attrs={
                'class': 'form-check',
            }),
            'salutation': TextInput(attrs={
                'placeholder': 'Dear ', 
                'style': 'width: 300px;', 
                'class': 'form-control'
            }),
            'body': Textarea(attrs={
                'placeholder': '', 
                'class': 'form-control'
            }),
            'sign_off': TextInput(attrs={
                'placeholder': 'Best,', 
                'style': 'width: 300px;', 
                'class': 'form-control'
            }),
            'ps': Textarea(attrs={
                'placeholder': '', 
                'style': 'height: 100px;',
                'class': 'form-control'
            }),
            'enclosed': TextInput(attrs={
                'placeholder': 'Comma, separated, default is blank', 
                'class': 'form-control'
            }),
            'date': DateInput(attrs={
                'style': 'width: 300px;', 
                'class': 'form-control',
                'type': 'date',
            }),
        }
