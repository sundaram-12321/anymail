from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
import sendgrid
import os,random
from sendgrid.helpers.mail import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

key='{"access_token": null, "client_id": "104741969451609727742", "client_secret": null, "refresh_token": null, "token_expiry": null, "token_uri": "https://oauth2.googleapis.com/token", "user_agent": null, "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "id_token": null, "token_response": null, "scopes": [], "token_info_uri": null, "invalid": false, "assertion_type": null, "_service_account_email": "mailany@ferrous-aleph-229415.iam.gserviceaccount.com", "_scopes": "https://spreadsheets.google.com/feeds https://www.googleapis.com/auth/drive", "_private_key_id": "fa27c6f09d8be19df4e72a9e5a740a7b248b8ecc", "_user_agent": null, "_kwargs": {}, "_private_key_pkcs8_pem": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4XbGXXZaw6S5G\\neDo9vw+h6XY4AmIBqF4N5nVdAQ8Qm0v/WHVTrJBOZkkJRK7wOmpfkwV2it5/7jVe\\nfPLGONAQ7T+uxlv7BBSyj0qi2w8Gwl6KFqZuEaG8uoIKIZUoZEOEfBbvpfy57GlW\\nglpoRG8FIxh3Lv0gIqiYTCu/e5XHCkFOZ3nSgRMRJMWbPkiL+Rq/mFlpou5R+VYG\\nFxyGOSd3fnVgefL53RvW2hbZWLnh/KQ12jVTuf/0XKE5tKRAw2uXohxDELVKIpU2\\nVnB07LWcSPE1K3UJuNiCfzgU8RshMROuZxvpfdl1SB7edl9Mc+qNkTWr4WgBUWcK\\npen8oxAZAgMBAAECggEAELIFXsJuHrujAeUpywUmBoDEgJpwoxtK1yHnP2KU6WlS\\nxr8NMuRV1g+rrf/vApiboOeIr10wfG/HG/UfLAWhi+LcKTjTxAWw1SGmPdyt/ev0\\nkTcvX5jPp25RT9cOMY/w0ErHbfC/U9vdhyS7SKVn01SEBuj1qacR0ubU8Fxh6hnz\\nHHhvYBAT12BR/Yc1+JhayTtBXVES4gJNleAEJ88n2ZNzV4ltG6i6vKzF55u+oLrD\\nmPxUujbnfVQiWa/ZtApmHD4j7isC7rrokFAf8W6njSMbzA1aYt3dcgI62qh2lRPp\\nBI/XDHqIchvBOLRkwRAtluar9Z+0OFvMdo7AUXaafQKBgQD72U0odGv7gjH36FPH\\n04SsHDAftb74CoT1YiI+XO1uXYBq6dVgVQd0gawvKvaWx9xK3GVgsPn2w5kka5KN\\nIMJduju+yZe5fGjxARYHSPQV3mMqFf6JvpasbiVqqHyIdWCSQIqjqp74YsW7xDeg\\n1flfS675r3OQ2TK0cmtUj2JLjQKBgQC7Z6R3f+cij1yvnkRSgkinjV+uLUx7b4fO\\nXABtSFRPnSI5e2MTYP/z5yD1+ZsOK+nrTKBmOlARdmam0P43hlFYShzdd3Kd4vn0\\neWBdBs42IgJAEUpBDHfLREchbLNTOjo/sQIXEYrM0F+ghNFdP1fjejUwv0mwSee6\\nkfcEUc+tvQKBgQDRCSAdv+QQsZO/7Ln9Vfb807it2TBUuIZ7FaTOllsMC9eW5dcR\\nSgISFb9QtxxNMj4KdLxAcSRISTlHHXJaaSJqoTUNuk2Qy05fG0OpcEgIDrnIKNFI\\ni0SMgi/UQ1x59tLdEW0BQ5EHIRR2MPrrKC7/hdYJsDL/uwd29rFXUluH0QKBgBl9\\nZV9jpDqNKVwxuLVIRz2S+xqjyq1XZC9rUBuNJPqXMtqCr90o6mdwXolWZAKvcmew\\nynhdIhrd8eRqtMk0mcfafMaawpo7DyhzgenlTRML2SaBs4nZeknJhatEL7f4SYf0\\nOYaNukVVakxZBGkcfoXQT3/L5Of3hW9Y/zI1Nnw5AoGAPa+1Qv2nP3caFh8P/aQC\\nl5GlKjxnFidguqLSnfNdLY0tOzziMMAlLGebz+ONskJNR1idJHV6A9tOVR3H/d3k\\nHE55kug0qr4DxEKOlQsuuL+2GuccQwdLzOOWquyiBwBMPph56Xh4hFJdocO8Lkh7\\n/qIp7iwHeh2xIg4+lJFNg2A=\\n-----END PRIVATE KEY-----\\n", "_class": "ServiceAccountCredentials", "_module": "oauth2client.service_account"}'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json(key)
client = gspread.authorize(creds)
sheet = client.open('entries').sheet1

def index(request):
    global scope,creds,client,sheet,key
    context={}
    if(request.method == 'GET'):

        r_otp = request.GET.get('otp')
        sender = Email(request.GET.get('sender'))

        r_mail = request.GET.get('reciever')
        reciever = Email(request.GET.get('reciever'))
        subject = request.GET.get('subject')
        content = Content("text/plain", request.GET.get('content'))
        x=True

        mail=request.session['mail']
        m_mail=mail
        print(mail,r_mail)
        if(r_mail == None):
            print("none")
            x=True
        else:
            if(r_mail.split("@")[-1] != mail.split("@")[-1]):
                context['status_code'] = 1
                context['mail_end']=mail.split("@")[-1]
                print("wrong mail")
                x=False
        otp=request.session['otp']
        print(otp,r_otp)
        if(str(r_otp) != str(otp)):
            context['status_code'] = 2
            print("wrong otp")
            x=False

        if(x):
            api_keys_list=['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','SG.Okv55E0rTEqBGbmtGRWsWg.pt_EBsKBbeObqf54bfrjxs1cKBlNMRG5-SfgMTlDbmA','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','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']
            if(True):
                print(sender,r_mail,subject,content)
                sg = sendgrid.SendGridAPIClient(apikey=api_keys_list[random.randint(0,3)])
                print(1)
                mail = Mail(sender, subject, reciever, content)
                print(2,mail.get())
                response = sg.client.mail.send.post(request_body=mail.get())
                print(3)
                print("Status Code = ",response.status_code)
                context['status_code']=int(response.status_code)

                row = [str(datetime.datetime.now()),str(m_mail),str(sender.email),str(reciever.email),subject,str(content.value)]
                sheet.insert_row(row)
            """
            except Exception as e:
                context['status_code']=400
                print(e)
                pass
            """


        #print(sender,reciever,subject,content)
        if(r_mail==None):
            context['status_code']=0
    return render(request,'mailany/index.html',context)

def verify(request):
    context={}

    if(request.method == 'GET'):
        otp = random.randint(100000,999999)
        mail =request.GET.get('email')
        request.session['otp']=otp
        request.session['mail']=mail
        reciever = Email(request.GET.get('email'))
        sender = Email("verify@anymail.com")
        subject = 'OTP for verification From Any MAIL'
        content = Content("text/plain", "Your OTP is " + str(otp))
        try:
            #print(sender,reciever,subject,content)
            sg = sendgrid.SendGridAPIClient(apikey='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')
            print(1)
            mail = Mail(reciever, subject, reciever, content)
            print(2)
            print(mail.get())
            response = sg.client.mail.send.post(request_body=mail.get())
            print(3)
            print("Status Code = ",response.status_code)
            context['status_code']=int(response.status_code)
            return redirect('/mailany/index1')
        except Exception as e:
            context['status_code']=400
            print(e)
            pass


    #context['graph'] = div
    return render(request,'mailany/home.html',context)

