from django.template.loader import render_to_string
from django.views.generic import View
from django.http import HttpRequest
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import ContactForm, QuoteForm


class QuoteView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        form = QuoteForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            ruc = form.cleaned_data['ruc']
            message = form.cleaned_data['message']
            products = message.split(',')

            html_msg = render_to_string('contact/quote.html', {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'ruc': ruc,
                'products': products,
            })
            try:
                send_mail(
                    subject='Cotización solicitada',
                    message=html_msg,
                    html_message=html_msg,
                    from_email='atencionalcliente@filtroswillybusch.com.pe',
                    recipient_list=[email],
                )
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        return JsonResponse({'success': False, 'errors': form.errors})


class EmailView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
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
                    recipient_list=[
                        'atencionalcliente@filtroswillybusch.com.pe'
                    ],
                    fail_silently=False,
                )
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
