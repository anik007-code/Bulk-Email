from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings


def send_bulk_email(request):
    if request.method == 'POST':
        recipients = request.POST.getlist('recipients')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipients  # Use the list of recipients
        )

        attachment = request.FILES.get('attachment')
        if attachment:
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        try:
            email.send()
            return render(request, 'success.html')
        except Exception as e:
            return render(request, 'error.html', {'error': str(e)})
    return render(request, 'send_email.html')
