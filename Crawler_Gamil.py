from __future__ import print_function
import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import csv
import base64


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

Data = []
Assunto = []
Email = []
Texto = []



def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    

    #Get Messages
    #results = service.users().messages().list(userId='me', labelIds='UNREAD').execute()
    results = service.users().messages().list(userId='me', labelIds=['UNREAD', 'INBOX'], q="category:primary").execute()
    messages = results.get('messages', [])

    message_count = 3
    for message in messages[:message_count]:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()

        PP = (msg['payload']['headers'])

        oi =(msg['payload'])
        #print(oi)

        #print(msg)
        #print('\n'*2)
        te = (msg)
        #print('\n'*2)
        #print(msg['payload']['headers'])
        titulo = (msg['payload']['headers'])
        #print(titulo)
        titu = (titulo[16]['value']) # titulo
        #print(msg['payload']['headers'])


         ###########################e-mail DATA

        repete = 'não'
        valorD = 1
        while repete == 'não':
            if "'name': 'Date', 'value':" in str(PP[valorD]):
                print(PP[valorD])
                hora = PP[valorD]['value']
                #print('ok')
                repete = 'sim'
                valorD = 1
            else:
                #print('não')
                #print(oi[valor])
                valorD += 1
                if valorD == 50:
                    print('erro')
                    repete = 'sim'



        ###########################e-mail TITULO

        repete = 'não'
        valorT = 1
        while repete == 'não':
            if "'name': 'Subject', 'value':" in str(PP[valorT]):
                print(PP[valorT])
                titu = PP[valorT]['value']
                #print('ok')
                repete = 'sim'
                valorT = 1
            else:
                #print('não')
                #print(oi[valor])
                valorT += 1
                if valorT == 50:
                    print('erro')
                    repete = 'sim'


        PP = (msg['payload']['headers'])
        #print('ID= ',msg['id']) # ID
        #print(oi)

        ######################## e-mail

        repete = 'não'
        valor = 1
        while repete == 'não':
            if "'name': 'From', 'value'" in str(PP[valor]):
                print(PP[valor])
                e_mail = PP[valor]['value']
                
                print('ok')
                repete = 'sim'
                valor = 1
            else:
                #print('não')
                #print(oi[valor])
                valor += 1
                if valorT == 50:
                    print('erro')
                    repete = 'sim'

        #emaai = (oi['value']) #email
        oi =(msg['payload']['parts'])
        txt = oi[0]# txt
        html1 = oi[1]
        html = html1['body']['data']
        print()
        print('======================'*2,'TITULO','======================'*2)
        oi2 = txt['body']['data']
        texto = base64.urlsafe_b64decode(oi2).decode('utf-8') # txt
        #print(texto)
        #print(html)
        HTML = base64.urlsafe_b64decode(html).decode('utf-8')
        #print(HTML)

        cont_te = HTML.count('"title"')
        print(cont_te)
        HTML_separa = HTML

        cont = 0

        while cont < cont_te:

            primero = (HTML_separa.find('"title"'))
            comeca = primero+10 # onde termina
            final = (HTML_separa[comeca:]).find('"')
            tet = comeca
            #print(HTML_separa[comeca:])
            print(final)
            texo = (HTML_separa[comeca:primero+13+(final-3):])
            print(texo)
            HTML_separa = HTML_separa[comeca:]
            cont += 1

        print('======================'*2,'TITULO','======================'*2)
        print()
        print()
        print('======================'*2,'DESCRIÇÃO','======================'*2)
        cont_descri = 0

        cota_D = HTML.count('"description":')
        print(cota_D)

        descricao = HTML
        
        while cont_descri < cota_D:

            primero_D = (descricao.find('"description":'))
            comeca_D = primero_D+16 # onde termina
            final_D = (descricao[comeca_D:]).find('"')
            tet = comeca_D
            #print(HTML_separa[comeca_D:])
            print(final_D)
            texo_D = (descricao[comeca_D:primero_D+19+(final_D-3):])
            print(texo_D)
            descricao = descricao[comeca_D:]
            cont_descri += 1

        print('======================'*2,'DESCRIÇÃO','======================'*2)
        print()
        print()
        print('======================'*2,'URL','======================'*2)
        cont_url = 0

        cota_U = HTML.count('"url":')
        print(cota_U)

        URL = HTML

        while cont_url < cota_U:
            primero_U = (URL.find('"url":'))
            comeca_U = primero_U + 8 # onde termina
            final_U = (URL[comeca_U:]).find('"')
            tet = comeca_U
            #print(URL[comeca_U:])
            print(final_U)
            texo_U = (URL[comeca_U:primero_U + 11 + (final_U - 3):])
            print(texo_U)
            URL = URL[comeca_U:]
            cont_url += 1

        print('======================'*2,'URL','======================'*2)

        #email = (msg['snippet']) #texto

        Assunto.append(titu)
        Data.append(hora)
        Email.append(e_mail)
        Texto.append(msg['snippet'])


        dados ={
            'Data': Data,
            'E-mail': Email,
            'Assunto': Assunto,
            'Texo': Texto       
        }

        emais = pd.DataFrame(data=dados)
        print(emais)

        #emais.to_csv('Emails.csv')

        #print(Texto)
        time.sleep(3)
        print("timer")
        #print(f'{email}\n')

if __name__ == '__main__':
    main()