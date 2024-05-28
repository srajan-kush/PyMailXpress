from django.shortcuts import render,HttpResponse,redirect
from django.core.mail import send_mail
from django.conf import settings
import ast
import re

# Create your views here.

def index(request):
    if request.method == "POST":
        data = request.POST
        sender_mail = data.get('sender_mail')
        sender_mail_pass = data.get('sender_mail_pass')
        list_of_email_recipients = ast.literal_eval(data.get('list_of_email_receivers'))
        string_of_variables = data.get('variables')
        _mail = data.get('full_mail')


        
        # Extracting variables from string_of_variables into var

        pattern = r'(\w+)\s*=\s*(?:(?P<list>\[.*?\])|(?P<string>.*?))(?:,\s*|\Z)'
        matches = re.findall(pattern, string_of_variables)

        var = {'subject': ''}

        # print(matches)

        for match in matches:
            variable_name = match[0]
            if match[1]:
                try:
                    variable_value = ast.literal_eval(match[1])
                except (SyntaxError, ValueError):
                    variable_value = match[1].strip("'")
            elif match[2]:  # Accessing the "string" group
                variable_value = match[2].strip("'")  # Extracting the string value
            else:
                variable_value = None

            var[variable_name] = variable_value

        # print(var)

        # dynamically set the email settings
        # Note: It's better to use environment variables or a dedicated settings module for sensitive data

        settings.EMAIL_HOST_USER = sender_mail
        settings.EMAIL_HOST_PASSWORD = sender_mail_pass



        # string of each mails formating into f-string and sending their corressponding mails

        for itt in range(0,len(list_of_email_recipients)):

            _email_list = [list_of_email_recipients[itt]]

            dynamic_Var = var.copy()

            # print(dynamic_Var)

            for __var in dynamic_Var:
                if type(dynamic_Var[__var]) == list:

                    # print(dynamic_Var[__var])
                    dynamic_Var[__var] = dynamic_Var[__var][itt]

                    # print(dynamic_Var[__var])

            try:
                full_mail = _mail.format(**dynamic_Var)
            except Exception as e:
                message = f"Failed to send email due to error in mail box - {str(e)}"
                return render(request,'index.html',{'massage':message})

            
            print(full_mail)
            # print(list_of_email_recipients[itt])

            # context = None

            try:
                send_email_to_client(var, full_mail,_email_list)
                message = "Email sent successfully!"
            except Exception as e:
                message = f"Failed to send email: {str(e)}"
            
        return render(request, 'index.html')

    return render(request, 'index.html', context=None)


def setting(request):
    return render(request,'setting.html')
    # return HttpResponse("This is setting Page")


def send_email_to_client(var, full_mail, list_of_email_recipients):
    subject = var['subject']    
    message = full_mail
    from_email = settings.EMAIL_HOST_USER
    recipient_list = list_of_email_recipients
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
