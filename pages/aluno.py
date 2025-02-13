#Importações das Biblioteca
import streamlit as st
from firebase_admin import firestore
import time
import datetime
from streamlit_autorefresh import st_autorefresh


#Configurações da Pagina
st.set_page_config(
    page_title="Projecto",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)



#------------------ Funções ---------------------

#Função Para Criar um Div
def criar_div(titulo, texto,tempo):
        st.markdown(
            f"""
            <div style="
                background-color: #262730;
                padding: 10px 10px 4px;
                border-radius: 10px;
                margin: 10px 0;
            ">
                <h2 style="color: white;">{titulo}</h2>
                <p style="color: white;">{texto}</p>
                <p style="color: #717275;text-align:right">{tempo}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


#Verificação se existe um user ou não
if "user" in st.session_state:
    user = st.session_state.user["email"]
    def inicio():

        tab1, tab2 = st.tabs(["Enviar", "Histórico",])
        db = firestore.client()

        with tab1:
            with st.form("formulario"):
                st.header("Compartilhar")
                option = st.selectbox("",("Ideia", "Reclamação"),label_visibility="hidden",key="Reclamação")
                txt = st.text_area("Digite algo :")
                enviar = st.form_submit_button("Enviar")
                if enviar:
                    status = st.empty()
                    if txt:
                        dados = {
                            "tipo": option,
                            "texto":txt ,
                            "email": st.session_state.user["email"],
                            "tempo":f"{datetime.date.today()} {datetime.datetime.now().time().hour}:{datetime.datetime.now().time().minute}:{datetime.datetime.now().time().second}:{datetime.datetime.now().time().microsecond}"
                            
                        }
                        db.collection("arquivos").add(dados)
                        
                        status.success("Enviado com sucesso!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        status.error("Escreve alguma coisa")
                        time.sleep(1)
                        status.empty()
        with tab2:
        
            arquivo_ref = db.collection("arquivos")
            arquivo = arquivo_ref.where("email", "==", st.session_state.user["email"]).stream()
            count = 0
            for arquivo in arquivo:
                arquivo_dict = arquivo.to_dict()
                criar_div(arquivo_dict["tipo"], arquivo_dict["texto"],arquivo_dict["tempo"])
                count+=1
            if count < 1:
                st.write("Nenhum arquivo encontrado")
    
                
        
    def chat():
        st_autorefresh(interval=3000, key="chat_update")
        db = firestore.client()
        countt = 0
        txt = st.chat_input("Diz alguma coisa")
        if txt:
            dados = {
                "to": "psicologa",
                "texto":txt ,
                "from": st.session_state.user["email"],
                "tempo":firestore.SERVER_TIMESTAMP
                            
                }
            db.collection("mensagens").add(dados)
            
            
        mensagens_from = db.collection("mensagens").where("from", "==", st.session_state.user["email"]).stream()

        
        mensagens_to = db.collection("mensagens").where("to", "==", st.session_state.user["email"]).stream()


        mensagens = list(mensagens_from) + list(mensagens_to)
        mensagens_ordenadas = sorted(
        mensagens, 
        key=lambda x: x.to_dict().get("tempo", ""),  
        reverse=False
    )
        
        for arquivo in mensagens_ordenadas:
            countt+=1
            arquivo_dict = arquivo.to_dict()
            if arquivo_dict["to"] == "psicologa":
        
                eu = st.chat_message("🙂") 
                eu.markdown(arquivo_dict["texto"])   
            else:
                eu = st.chat_message("👩🏻‍⚕️") 
                eu.markdown(arquivo_dict["texto"]) 
        if countt < 1:
            st.info("Escreve Algo Para Começar")
            
            
    

    if "pagina" not in st.session_state:
        st.session_state.pagina = 0

    sidebar = st.sidebar

    if sidebar.button("Inicio",use_container_width=True):
        st.session_state["pagina"]  = 0
    if sidebar.button("Psicologa",use_container_width=True):
        st.session_state["pagina"]  = 1

    if st.session_state["pagina"]  == 0:
        inicio()
    else: 
        chat()
else:
    st.switch_page("home.py")