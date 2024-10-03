from django.shortcuts import render
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .forms import ContactForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Montando os dados do e-mail
            email_message = '''
            From:\n\t\t{}\n
            Message:\n\t\t{}\n
            Email:\n\t\t{}\n
            '''.format(name, message, email)
            
            # Definindo o e-mail
            msg = MIMEMultipart()
            msg['From'] = 'glbfaria42@gmail.com'
            msg['To'] = 'guiloubrandt@hotmail.com'
            msg['Subject'] = 'Portfolio: Você recebeu uma mensagem!'

            # Codificar o corpo do e-mail em UTF-8
            msg.attach(MIMEText(email_message, 'plain', 'utf-8'))

            try:
                # Enviando o e-mail via servidor SMTP do Gmail
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login('glbfaria42@gmail.com', os.getenv('EMAIL_PASSWORD'))
                    server.sendmail(msg['From'], msg['To'], msg.as_string())
                print("Email enviado com sucesso")
                messages.success(request, "Obrigado " + name + ", entraremos em contato em breve!")
            except Exception as e:
                print("Erro ao enviar o email:", str(e))
                messages.error(request, 'Erro ao enviar o email. Tente novamente.')

    return render(request, 'home.html', {'form': form})