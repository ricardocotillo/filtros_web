from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length=100)
    last_name = forms.CharField(label='Apellido', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Teléfono', max_length=100)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)
