#Importações das Biblioteca
import firebase_admin._auth_client
import firebase_admin.auth
import streamlit as st
import firebase_admin
from firebase_admin import credentials
import requests
import jwt  
from jwt import DecodeError

#Mudar a cor do site [branco , vinho , Preto]
#



#Configurações da Pagina
st.set_page_config(
    page_title="Projecto",
    page_icon="🧊",
    layout="wide",
 
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


# Configuração do Firebase 
firebaseConfig = {
    "apiKey": "AIzaSyBFIMnD7uOvASP08_a9Zp6px_ub4DWl2aI",
    "authDomain": "anotherproject-5e811.firebaseapp.com",
    "projectId": "anotherproject-5e811",
    "storageBucket":"anotherproject-5e811.firebasestorage.app",
    "messagingSenderId": "1069155836636",
    "appId": "1:1069155836636:web:8aa2ce0c80a4320d584a19",
    "databaseURL": ""
}


# Criação do Firebase Com as Credencias
if not firebase_admin._apps:
    cred = credentials.Certificate("another/anotherproject-5e811-firebase-adminsdk-fbsvc-407565d917.json")
    default_app=firebase_admin.initialize_app(cred)


#------------------ Variaveis Golbais ---------------------


REDIRECT_URI = "https://listaa.streamlit.app"
url = "https://static.wixstatic.com/media/cd3bb0_75d00a426f3a490cad3623afffe0de08~mv2.png/v1/fill/w_238,h_77,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/logo_esprominho_versao%20Horizontal.png"
psicologa = []
associação = ["brg-6330@esprominho.pt"]


#------------------ Funções ---------------------


#Descofificar o Token Para Depois Ser Lido
def decode_firebase_token(id_token):
    try:
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        return decoded_token  # Retorna o JSON decodificado
    except DecodeError:
        return {"error": "Token inválido"}


#Função para gerar a URL de autenticação do Google
def get_google_auth_url():
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id=1069155836636-ekve034mfjluv4s6icus6kb7bi3ltpnr.apps.googleusercontent.com&redirect_uri=https://listaa.streamlit.app&response_type=code&scope=email profile&prompt=select_account"
    return auth_url


#Função para trocar o código de autorização por um token de acesso
def exchange_code_for_token(code):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": "1069155836636-ekve034mfjluv4s6icus6kb7bi3ltpnr.apps.googleusercontent.com",
        "client_secret": "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",
        "redirect_uri": "https://listaa.streamlit.app",
        "grant_type": "authorization_code",
    
    }
    
    response = requests.post(token_url, data=data)
  
    # Exibe a resposta completa e o status
   
    
    
    return response.json()


#Função Para verificar a Entrada na pagina condicional(caso for escolar e caso não for)
def entrada_condicional():
    if st.session_state.user:
        if "@esprominho.pt" in st.session_state.user["email"]:
            st.switch_page("pages/aluno.py")
        else: 
            st.error("Email Inválido! Tente com um Email Escolar")
        #if st.session_state.user["email"].split("@")[1] == "esprominho.pt":
            #pass
        #else:
            #st.write()
            #
            #st.session_state.user = None
            

#Função de Personalização do Botão
def botao_personalizado(auth_url):
    st.markdown(
            """
            <style>
            .google-button {
                background-color: #4285F4;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                margin:0 auto;
            
            
            }
            .google-button:hover {
                background-color: #357ABD;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Exibir o botão
    if st.markdown(
            f'<a href="{auth_url}" target="_self"><button class="google-button">Entrar com o Google</button></a>',
            unsafe_allow_html=True,
        ):
            pass


#Função para Criar e Decodificar o Token
def criar_decodificar_token(query_params):
    if "code" in query_params:
            code = query_params["code"]
        

            # Trocar o código por um token de acesso
            token_response = exchange_code_for_token(code)
            if "id_token" in token_response:
                
                id_token = token_response["id_token"]
            
                # Autenticar o usuário no Firebase
                user_email = decoded_json = decode_firebase_token(id_token)
                if user_email:
                    st.session_state.user = user_email
                    st.rerun()  # Atualiza a página para refletir o login
            else:
                pass





#------------------ Interface do Streamlit ---------------------





#imagem
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;margin-bottom:30px">
        <img src="{url}" width="200">
    </div>
    """,
    unsafe_allow_html=True
)

#Texto
st.text("""🗣️ Sua voz importa!

Este é o espaço onde você pode compartilhar ideias, sugestões e preocupações sobre a escola. Juntos, podemos criar um ambiente melhor para todos!

💡 Como funciona?
✔ Faça login com sua conta Google Escolar.
✔ Envie suas sugestões e problemas.
✔ Colabore para encontrar soluções!
✔ Converse anonimamente com a psicóloga escolar""")

#Verificar se o estado já existe  ou não
if "user" not in st.session_state:
    st.session_state.user = None

#Entrada na pagina condicional(caso for escolar e caso não for)
entrada_condicional()

# Gerar a URL de autenticação do Google
auth_url = get_google_auth_url()

# Botão bonito para autenticação com o Google
botao_personalizado(auth_url)

st.markdown(
        f'<p style="text-align:center">Feito Pela associação de estudante <b>Outra Coisa</b></p>',
        unsafe_allow_html=True,
    )


# Capturar o código de autorização retornado pelo Google
query_params = st.query_params

#Criar e Decodificar o Token
criar_decodificar_token(query_params=query_params)
