# Message Flow

**Responsável:** Cayo Slowik <br>
**ID:** 779168 <br>
**E-mail:** cayo.slowik@brf.com <br>

## Descrição

Essa é uma biblioteca python para ser utilizada com o intuito de facilitar o envio de dashboards do Power BI ou messagens de texto através do Microsoft Teams, Outlook e WhatsApp. 

## Funcionalidades

- Envio de dashboards do Power BI.
- Envio de mensagens de texto.
- Compátivel com Microsoft Teams, Outlook e WhatsApp.

## Instalação

### Clone o repositório:

 ```sh
    pip install git+https://{REPO_PASSWORD}@dev.azure.com/brf-corp/Analytics-DataScience/_git/message-flow
 ```


## Uso

1. Importe as classes que for utilizar :

```sh
from message_flow import export_report__to_image
from message_flow import BlobUploader
from message_flow import MS_Teams 
from message_flow import Email_Message
from message_flow import Chat_Message
from message_flow import WhatsAppMessage
```

2. Crie um arquivo .env

```env
CLIENT_ID=0000000000001
CLIENT_SECRET=**********
TENANT_ID=0000000000002
USERNAME=email.exemplo@brf.com # email do usuário de serviço vinculado ao Azure AD
PASSWORD=****** # senha do usuário de serviço vinculado ao Azure AD
CONNECT_STR=my-connection-string
SAS_TOKEN=******************************************
```

3. Crie váriavéis com o conteúdo do .env:

```sh
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
connect_str = os.getenv("CONNECT_STR")
sas_token = os.getenv("SAS_TOKEN")
```

4. Exemplo de export_report__to_image:

```sh
# definindo os parâmetros
report_id = '00000001'
visual_name = '000000002'
page_name = 'ReportSection00000001'
container_name = "my-container-name"
filter ="Tabela/Coluna eq 'VALOR'"

# chamando o método
report_image_generator = export_report__to_image(
    client_id, tenant_id, username, password)
file_name = report_image_generator.get_report_image(
    report_id, visual_name, page_name, filter)
 ```

5. Exemplo de BlobUploader:

```sh
# chamando o método
blob_uploader = BlobUploader(connect_str, container_name, file_name)
upload_success = blob_uploader.upload_file_to_blob()
if upload_success:
        print("Arquivo enviado para o blob com sucesso!")
    else:
        print("Erro ao enviar o arquivo para o blob. Verifique os logs para mais detalhes.")
```

6. Exemplo de MS_Teams:

```sh
# definindo parâmetros de texto (utilize se quiser enviar apenas texto)
# message = 'exemplo de mensagem'
# payload = {
#         "body": {
#             "contentType": "html",
#                     "content": message
#         }
#     }

# baixando a imagem
def read_image_file(file_name):
    with open(file_name, 'rb') as file:
        encoded_image = base64.b64encode(file.read()).decode('utf-8')
    return encoded_image

image_content = read_image_file(file_name)

# definindo parâmetros
payload = {
    "body": {
        "contentType": "html",
        "content": '<div><div><div><span><img src="../hostedContents/1/$value" style="max-width: 100%; max-height: 100%; vertical-align:bottom;"></span></div></div></div>'
    },
    "hostedContents": [{
        "@microsoft.graph.temporaryId": "1",
            "contentBytes": image_content,
        "contentType": "image/png"
    }]
}

# chamando método
my_teams_instance = MS_Teams(client_id, client_secret, tenant_id, username, password)
my_teams_instance.main(payload=payload, emails='exemplo.email@brf.com')
```

8. Exemplo de Email_Message:

```sh
# definindo parâmetros de texto (utilize se quiser enviar apenas texto)
# message = 'exemplo de mensagem'
# payload = {
#         "message": {
#             "subject": subject,
#             "body": {
#                 "contentType": "html",
#                 "content": message
#         },
#             "toRecipients": [
#                 {
#                     "emailAddress": {
#                         "address": email
#                     }
#                 }
#             ]
#         },
#         "saveToSentItems": "false"
# }


# baixando a imagem
def read_image_file(file_name):
    with open(file_name, 'rb') as file:
        encoded_image = base64.b64encode(file.read()).decode('utf-8')
    return encoded_image

image_content = read_image_file(file_name)

# definindo parâmetros com imagem 
payload = {
    "message": {
        "subject": "Test",
        "body": {
            "contentType": "html",
            "content": "teste"
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": "email.exemplo@brf.com"
                        }
            }
        ],
        "attachments": [
            {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": "image.png",
                "contentType": "image/png",
                "contentBytes": image_content
            }
        ]
        
    },
    "saveToSentItems": "false"
}
    
# chamando método
email = Email_Message(client_id, tenant_id, username, password)
email.send_message_email(payload)
```

9. Exemplo de Chat_Message:

```sh
# definindo os parâmetros de texto (utilize se quiser enviar apenas texto)
# message = 'exemplo de mensagem'
# body = [
#     {
#         "type": "TextBlock",
#         "text": message
#     }
# ]

# definindo os parâmetros com imagem
image_url = f'https://blob-acount/{container_name}/{file_name}?{sas_token}'
body = [
    {
        "type": "TextBlock",
        "text": message
    },    
    {
        "type": "Image",
        "url": image_url
    }
]
        
# chamando o método
chat_teams_message = Chat_Message(webhook, "as")
chat_teams_message.send_message_to_chat(body)
```

10. Exemplo de WhatsAppMessage(possuí custos):

```sh
# definindo os parâmetros
from_number = '999999999'
to_number = '99999998'
template_name = 'nome-do-template' # seguir o passo a passo do infobip para criar o template (processo feito com o time de BOTs)
template_data = {json:'conteúdo a ser enviado nos padrões do template'}
language = "pt_BR"
        
# chamando método
whatsapp_message = WhatsAppMessage(
    from_number, to_number, template_name, template_data, language, authorization)
response = whatsapp_message.send()
```


## Métodos

### `export_report__to_image`

A classe `export_report__to_image` é responsável por exportar relatórios do Power BI para imagens. Ela autentica o usuário, faz requisições à API do Power BI e baixa os arquivos exportados.

#### Métodos Privados

- `__obter_token()`: Obtém o token de acesso.
- `__post_export_to_file_api(url, payload)`: Faz uma requisição POST para exportar o relatório.
- `__get_status(url)`: Verifica o status de uma requisição de exportação.
- `__download_file_exported(url)`: Baixa o arquivo exportado.

#### Função Principal

- `get_report_image(report_id, visual_name, page_name, filter)`: Exporta um relatório do Power BI para uma imagem PNG. Este método faz a requisição de exportação, verifica o status até a conclusão e baixa o arquivo exportado, salvando-o localmente com um nome baseado na data e hora atuais.

### `BlobUploader`

A classe `BlobUploader` é responsável por fazer o upload de arquivos para um container do Azure Blob Storage. Ela gerencia a conexão com o serviço de armazenamento e realiza o upload dos arquivos especificados.

#### Métodos Privados

- `__upload_blob(file_path)`: Faz o upload de um arquivo para o Azure Blob Storage.

#### Função Principal

- `upload_file_to_blob()`: Realiza o upload de um arquivo para o Azure Blob Storage. Este método obtém o caminho do arquivo, chama o método privado para fazer o upload e lida com possíveis exceções, registrando mensagens de erro se necessário.

### `MS_Teams` 

A classe `MS_Teams` é responsável por gerenciar a autenticação e comunicação com a API do Microsoft Teams. Ela obtém tokens de acesso, busca usuários e envia mensagens.

#### Métodos Privados

- `get_headers(bearer_token)`: Retorna os cabeçalhos necessários para as chamadas à API do Microsoft Graph.
- `get_token_for_user_application()`: Obtém um token de acesso em nome de um usuário usando nome de usuário e senha.
- `get_token_for_client_application()`: Obtém um token de acesso em nome de uma aplicação cliente usando client_secret e client_id.
- `get_signedin_user_data(bearer_token)`: Obtém os dados do usuário autenticado.
- `get_ms_teams_users(bearer_token, filters)`: Busca usuários do Microsoft Teams com base em filtros.
- `send_message_to_ms_teams_user(bearer_token, sender_ms_team_id, user_ms_teams_id, payload)`: Envia uma mensagem para um usuário do Microsoft Teams em duas etapas: cria um chat e envia a mensagem.
- `get_ms_teams_users_using_emails(bearer_token, emails)`: Busca usuários do Microsoft Teams usando seus emails.

#### Função Principal

- `main(payload, emails)`: Gerencia o fluxo principal de autenticação, busca de usuários e envio de mensagens. Obtém tokens de acesso, busca o usuário autenticado, procura usuários pelo email e envia a mensagem para o primeiro usuário encontrado.

Se precisar de mais alguma coisa, estou à disposição!

### `Email_Message`

A classe `Email_Message` é responsável por enviar emails usando a API do Microsoft Graph. Ela autentica o usuário, obtém um token de acesso e envia mensagens de email.

#### Métodos Privados

- `__obter_token()`: Obtém o token de acesso.

#### Função Principal

- `send_message_email(payload)`: Envia um email usando a API do Microsoft Graph. Este método faz uma requisição POST com o payload do email e os cabeçalhos de autorização, registrando mensagens de sucesso ou erro conforme o status da resposta.

### `Chat_Message`

A classe `Chat_Message` é responsável por enviar mensagens para um chat do Microsoft Teams usando um webhook. Ela configura a mensagem no formato de um Adaptive Card e a envia para o chat especificado.

#### Função Principal

- `send_message_to_chat(body)`: Envia uma mensagem para um chat do Microsoft Teams. Este método cria uma mensagem no formato de um Adaptive Card com o corpo fornecido e a envia usando o webhook configurado.

### `WhatsAppMessage`

A classe `WhatsAppMessage` é responsável por enviar mensagens de template via WhatsApp usando a API do Infobip. Ela configura a mensagem com os dados fornecidos e a envia para o número especificado.

#### Função Principal

- `send()`: Envia uma mensagem de template via WhatsApp. Este método cria o payload da mensagem com os dados fornecidos, faz uma requisição POST para a API do Infobip e retorna a resposta da requisição.

### Observações adicionais

Para utilizar os recursos da Microsoft, é necessário criar um **Microsoft Entra ID** (anteriormente conhecido como Azure AD). Consulte o artigo [Registrar um aplicativo do Microsoft Entra e criar uma entidade de serviço](https://learn.microsoft.com/pt-br/entra/identity-platform/howto-create-service-principal-portal) para orientações detalhadas.

O **Microsoft Entra ID** precisará ter as seguintes permissões de API:

- **Microsoft Graph:**
    - Chat.Create
    - Chat.Read
    - Chat.ReadBasic
    - Chat.ReadWrite
    - Chat.ReadWrite.All
    - Mail.Send
    - User.Read
    - User.Read.All

Para mais informções sobre o a API do Microsoft Graph, consulte o artigo [Visão Geral do Microsoft Graph](https://learn.microsoft.com/pt-br/graph/overview).

- **Power BI Rest API:**
    - Dataset.Read.All
    - Dataset.ReadWrite.All
    - Report.Read.All
    - Report.ReadWrite.All

Para mais informações sobre a Rest API do Power BI, consulte o artigo [Power BI Rest API](https://learn.microsoft.com/en-us/rest/api/power-bi/reports).

Precisaremos utilizar um usuário adicionado ao grupo do Microsoft Entra ID. Recomendamos o uso de um usuário de serviço (ele precisará ter acesso aos workspaces onde os dashboards estão armazenadas e também será responsável por enviar as mensagens via Teams e Outlook).

Também é necessário utilizar uma conta para armazenar blobs. Para mais informações, veja o artigo [Introdução ao armazenamento de blobs do Azure](https://learn.microsoft.com/pt-br/azure/storage/blobs/storage-blobs-introduction).

Para o envio no WhatsApp, utilizamos a API do Infobip. Consulte a documentação [Send WhatsApp template message](https://www.infobip.com/docs/api/channels/whatsapp/whatsapp-outbound-messages/send-whatsapp-template-message). É necessário realizar a criação do número e do template com o time de BOTs.
