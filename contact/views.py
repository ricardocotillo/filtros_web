from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import ContactForm

class EmailView(View):
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            html_msg = render_to_string('contact/email.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone
            })
            try:
                send_mail(
                    subject='Nuevo mensaje de contacto',
                    message='',
                    html_message=html_msg,
                    from_email='atencionalcliente@filtroswillybusch.com.pe',
                    recipient_list=['atencionalcliente@filtroswillybusch.com.pe'],
                    fail_silently=False,
                )
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})

            return JsonResponse({'success': True})
        else:
            print(form.errors.as_json())
            return JsonResponse({'success': False, 'errors': form.errors})
            
            