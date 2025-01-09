import streamlit as st
from controle_de_acesso import *
from negocio import *
import pandas as pd
import pickle

def salvaClientes(df_clientes):
    with open("dados/clientes.pkl", "wb") as f:
        pickle.dump(df_clientes, f)
try:
    with open("dados/clientes.pkl", "rb") as f:
        df_clientes = pickle.load(f)
except:
    df_clientes = pd.DataFrame(columns=["ID","Cliente","Nome","Responsável","Telefone","Instalações"])
    salvaClientes(df_clientes)



def registraCliente():
    def limpa_formulario():
        st.session_state["nome-cliente"] = ""
        st.session_state["responsavel-cliente"] = ""
        st.session_state["tel-cliente"] = ""

    st.title("Registro de cliente")
    nome = st.text_input("Nome:", "", key="nome-cliente")
    responsavel = st.text_input("Responsável:", "", key="responsavel-cliente")
    tel = st.text_input("Telefone:", "", key="tel-cliente")
    if st.button("Criar Cliente"):
        if nome in df_clientes["Nome"].values:
            st.error("Cliente já cadastrado")
            return
        try:
            cliente = Cliente(nome=nome, responsavel=responsavel, tel=tel, instalacoes=[])
            st.success("Cliente criado com sucesso!")
            df_clientes.loc[len(df_clientes)] = {"ID":len(df_clientes)+1,
                                                 "Cliente":cliente,
                                                 "Nome":cliente.getNome(),
                                                 "Responsável":cliente.getResponsavel(),
                                                 "Telefone":cliente.getTel(),
                                                 "Instalações":cliente.getInstalacoes()}
            salvaClientes(df_clientes)
            limpa_formulario()
        except Exception as e:
            st.error(f"Erro ao criar cliente: {e}")

def registraInstalacao(cliente:Cliente):

    def limpa_formulario():
        st.session_state["nome-instalacao"] = ""
        st.session_state["endereco-instalacao"] = ""
        st.session_state["gps-instalacao"] = ""

    st.title("Registro de Instalações")
    nome = st.text_input("Nome:", "", key="nome-instalacao")
    endereco = st.text_input("Endereço:", "",key= "endereco-intalacao")
    gps = st.text_input("GPS:", "", key="gps-instalacao")
    if st.button("Registrar Instalação"):
        if nome in [instalacao for instalacao in cliente.getInstalacoes()]:
            st.error("Instalação já cadastrada")
            return
        try:
            instalacao = Instalacoes(nome=nome, endereco=endereco, gps=gps, andares=[])
            cliente.criar_intalacao(instalacao)
            st.success("Instalação registrada com sucesso!")
            salvaClientes(df_clientes)
            limpa_formulario()
        except Exception as e:
            st.error(f"Erro ao registrar instalação: {e}")

def registraAndar(instalacao:Instalacoes):
    def limpa_formulario():
        st.session_state["nome-andar"] = ""

    st.title("Registro de Divisão/Andar")
    st.write('Digite o nome da divisão ou o número do andar')
    nome_andar = st.text_input("Nome da divisão/andar:", "",key="nome-andar")
    if st.button("Registrar Divisão/Andar"):
        if nome_andar in [andar.getNome() for andar in instalacao.getAndares()]:
            st.error("Divisão/Andar já cadastrada")
            return
        andar = Andar(nome=nome_andar, portas=[], controladoras=[])
        instalacao.criaAndar(andar)
        st.success("Divisão/Andar registrada com sucesso!")
        st.success("Selecione a aba portas e controladora para incluir portas e controladoras nos andares/divisões criados")
        salvaClientes(df_clientes)
        limpa_formulario()


def selecionaAndar():
    cliente_opt = st.selectbox("Cliente:", df_clientes["Nome"].to_list())
    cliente = df_clientes[df_clientes["Nome"] == cliente_opt].iloc[0]["Cliente"]
    opt_instalacao = st.selectbox("Instalações:", cliente.getInstalacoes())
    instalacao = opt_instalacao
    opt_andar = st.selectbox("Andar:", instalacao.getAndares())
    andar = opt_andar
    return andar

def limpa_formulario_controladora():
    st.session_state["local-ctrl"] = ""
    st.session_state["nome-ctrl"] = ""
    st.session_state["marca-ctrl"] = ""
    st.session_state["modelo-ctrl"] = ""
    st.session_state["ip-ctrl"] = ""
    st.session_state["mascara-ctrl"] = ""
    st.session_state["gateway-ctrl"] = ""
    st.session_state["tec-ctrl"] = ""
    st.session_state["data-compra-ctrl"] = ""
    st.session_state["data-inst-ctrl"] = ""
    st.session_state["garantia-ctrl"] = ""

def limpa_formulario_porta():
    st.session_state["local-porta"] = ""
    st.session_state["tec-bot"] = ""
    st.session_state["data-compra-bot"] = ""
    st.session_state["data-inst-bot"] = ""
    st.session_state["garantia-bot"] = ""
    st.session_state["tec-ima"] = ""
    st.session_state["data-compra-ima"] = ""
    st.session_state["data-inst-ima"] = ""
    st.session_state["garantia-ima"] = ""
    st.session_state["tec-entrada"] = ""
    st.session_state["data-compra-entrada"] = ""
    st.session_state["data-inst-entrada"] = ""
    st.session_state["garantia-entrada"] = ""
    st.session_state["ip-entrada"] = ""
    st.session_state["mascara-entrada"] = ""
    st.session_state["gateway-entrada"] = ""
    st.session_state["tec-saida"] = ""
    st.session_state["data-compra-saida"] = ""
    st.session_state["data-inst-saida"] = ""
    st.session_state["garantia-saida"] = ""
    st.session_state["ip-saida"] = ""
    st.session_state["mascara-saida"] = ""
    st.session_state["gateway-saida"] = ""





#-----------------------------------------------------------------------------------------------
#                                Inicio da Aplicação Streamlit
#                          Pagina Inicial para escolher o que registrar 
#
#
#
#-----------------------------------------------------------------------------------------------"""



st.title("Controle de Acesso")

st.sidebar.title("Opções")
opcoes = ["Cliente","Controladora", "Porta"]
option = st.sidebar.selectbox("Escolha uma opção:", opcoes)



if option == "Cliente":
    if len(df_clientes) == 0:
        registraCliente()
    else:
        opcoes = df_clientes["Nome"].to_list()
        if "Novo Cliente" not in opcoes:
            opcoes.append("Novo Cliente")
        if "Nova Instalação" in opcoes: #coloca a opção de criação na última posição
            opcoes.remove("Nova Instalação")
            opcoes.append("Nova Instalação")
        opt_cliente = st.selectbox("Escolha Cliente:", opcoes)
        if opt_cliente == "Novo Cliente":
            registraCliente()
            
        cliente = df_clientes[df_clientes["Nome"] == opt_cliente].iloc[0]["Cliente"]
        if cliente.getInstalacoes() == []:
            registraInstalacao(cliente)
        else:
            opcoes_instalacoes = cliente.getInstalacoes()
            if "Nova Instalação" not in opcoes_instalacoes:
                opcoes_instalacoes.append("Nova Instalação")
            if "Nova Instalação" in opcoes_instalacoes:
                opcoes_instalacoes.remove("Nova Instalação")
                opcoes_instalacoes.append("Nova Instalação")
            opt_instalacao = st.selectbox("Escolha Instalação:", opcoes_instalacoes)
            if opt_instalacao == "Nova Instalação":
                registraInstalacao(cliente)
            else:
                instalacao = opt_instalacao
                registraAndar(instalacao)


elif option == "Controladora":
    andar = selecionaAndar()
    st.title("Controladora")
    local = st.text_input("Local:", "", key= "local-ctrl")
    nome = st.text_input("Nome:", "", key= "nome-ctrl")
    marca = st.text_input("Marca:", "", key= "marca-ctrl")
    modelo = st.text_input("Modelo:", "", key= "modelo-ctrl")
    ip = st.text_input("IP:", "", key= "ip-ctrl")
    mascara = st.text_input("Máscara de Sub-rede:", "", key= "mascara-ctrl")
    gateway = st.text_input("Gateway:", "", key= "gateway-ctrl")
    tec = st.text_input("Técnico:", "", tec= "tec-ctrl")
    data_compra = st.date_input("Data de Compra:", key= "data-compra-ctrl")
    data_instalacao = st.date_input("Data de Instalação:", key= "data-inst-ctrl")
    temp_garantia = st.number_input("Tempo de Garantia (meses):", min_value=3, key= "garantia-ctrl")
    
    if st.button("Criar Controladora"):
        try:
            bateria = Bateria(marca="teste", modelo="teste", local="teste")
            controladora = Controladora(local=local, 
                                        nome=nome, 
                                        marca=marca, 
                                        modelo=modelo, 
                                        bateria=bateria, 
                                        portas=[], 
                                        ip=ip, 
                                        mascara_sub_rede=mascara, 
                                        gateway=gateway, 
                                        tec=tec, 
                                        data_compra=data_compra.strftime("%d-%m-%Y"), 
                                        data_instalacao=data_instalacao.strftime("%d-%m-%Y"), 
                                        temp_garantia=temp_garantia)
            st.success("Controladora criada com sucesso!")
            st.write(controladora)
            andar.criaControladora(controladora)
            salvaClientes(df_clientes)
            limpa_formulario_controladora()
        except Exception as e:
            st.error(f"Erro ao criar controladora: {e}")

elif option == "Porta":
    st.title("Porta")
    andar = selecionaAndar()
    nome = st.text_input("Local:", "",key= "local-porta")
    #Seção Botoeira
    opt_botoeira = st.selectbox("Botoeira de Emergência", ["Padrão"])
    tec_bot = st.text_input("Técnico:", "",key= "tec-bot")
    data_compra_bot = st.date_input("Data de Compra:",key= "data-compra-bot")
    data_instalacao_bot = st.date_input("Data de Instalação:",key= "data-inst-bot")
    temp_garantia_bot = st.number_input("Tempo de Garantia (meses):", min_value=3,key= "garantia-bot")
    #Seção Imã
    opt_ima = st.selectbox("Eletroimã", ["Padrão 150kgf", "Padrão 300kgf"])
    inst_ima = st.text_input("Técnico:", "",key= "inst-ima")
    data_compra_ima = st.date_input("Data de Compra:",key= "data-compra-ima")
    data_instalacao_ima = st.date_input("Data de Instalação:",key= "data-inst-ima")
    temp_garantia_ima = st.number_input("Tempo de Garantia (meses):", min_value=3,key= "garantia-ima")
    tec_ima = st.text_input("Técnico:", "",key= "tec-ima")
    #Seção Leitor de Entrada
    opt_leitor_entrada = st.selectbox("Leitor de Entrada", ["Cartão", "Digital", "Facial 342","Facial 671"])
    data_compra_leitor_entrada = st.date_input("Data de Compra:",key= "data-compra-entrada")
    data_instalacao_leitor_entrada = st.date_input("Data de Instalação:",key= "data-inst-entrada")
    temp_garantia_leitor_entrada = st.number_input("Tempo de Garantia (meses):", min_value=3, key="garantia-entrada")
    tec_leitor_entrada = st.text_input("Técnico:", "",key= "tec-entrada")
    if opt_leitor_entrada in ["Facial 342","Facial 671"]:
        ip_leitor_entrada = st.text_input("IP:", "",key="ip-entrada")
        mascara_leitor_entrada = st.text_input("Máscara de Sub-rede:", "",key="mascara-entrada")
        gateway_leitor_entrada = st.text_input("Gateway:", "",key="gateway-entrada")
    else:
        ip_leitor_entrada = ""
        mascara_leitor_entrada = ""
        gateway_leitor_entrada = ""
    
    #Seção Leitor de Saida
    opt_leitor_saida = st.selectbox("Leitor de Saída", ["Botoeira", "Cartão", "Digital", "Facial 342","Facial 671"])
    data_compra_leitor_saida = st.date_input("Data de Compra:",key= "data-compra-saida")
    data_instalacao_leitor_saida = st.date_input("Data de Instalação:",key= "data-inst-saida")
    temp_garantia_leitor_saida = st.number_input("Tempo de Garantia (meses):", min_value=3, key="garantia-saida")
    tec_leitor_saida = st.text_input("Técnico Instalador:", "", key="tec-saida")
    if opt_leitor_saida in ["Facial 342","Facial 671"]:
        ip_leitor_saida = st.text_input("IP do Leitor de Saída:", "", key="ip-saida")
        mascara_leitor_saida = st.text_input("Máscara de Sub-rede:", "", key="mascara-saida")
        gateway_leitor_saida = st.text_input("Gateway do Leitor de Saída:", "", key="gateway-saida")
    else:
        ip_leitor_saida = ""
        mascara_leitor_saida = ""
        gateway_leitor_saida = ""
    

    botoeiras = {"Padrão":BotoeiraEmergencia(marca="Intelbras",
                                            modelo = "AS 2010",
                                            local=nome,
                                            tensao=12,
                                            data_instalacao=data_instalacao_bot,
                                            data_compra=data_compra_bot,
                                            temp_garantia=temp_garantia_bot,
                                            tec=tec_bot) }
    
    imas = {"Padrão 150kgf":Ima(marca="Intelbras",
                               modelo="FE 20150",
                               local=nome,
                               tensao=12,
                               kgf=150,
                               tec=tec_ima,
                               data_instalacao=data_instalacao_ima,
                               data_compra=data_compra_ima,
                               temp_garantia=temp_garantia_ima),
            "Padrão 300kgf":Ima(marca="Intelbras",
                               modelo="FE 10300",
                               local=nome,
                               tensao=12,
                               kgf=300,
                               tec=tec_ima,
                               data_instalacao=data_instalacao_ima,
                               data_compra=data_compra_ima,
                               temp_garantia=temp_garantia_ima)}
    
    leitores = {"Cartão":Leitor(nome=nome,
                              marca="Dormakaba",
                              modelo="cartão",
                              tipo="cartão",
                              ip="",
                              mascara_sub_rede="",
                              gateway="",
                              RS485=1,
                              local=nome,
                              tec=tec_leitor_entrada,
                              temp_garantia=temp_garantia_leitor_entrada,
                              data_compra=data_compra_leitor_entrada,
                              data_instalacao=data_instalacao_leitor_entrada),
                "Digital":Leitor(nome=nome,
                              marca="Dormakaba",
                              modelo="digital",
                              tipo="digital",
                              ip="",
                              mascara_sub_rede="",
                              gateway="",
                              RS485=1,
                              local=nome,
                              tec=tec_leitor_entrada,
                              temp_garantia=temp_garantia_leitor_entrada,
                              data_compra=data_compra_leitor_entrada,
                              data_instalacao=data_instalacao_leitor_entrada),
                "Facial 342":Leitor(nome=nome,
                              marca="Hikvision",
                              modelo="342",
                              tipo="Facial",
                              ip="",
                              mascara_sub_rede="",
                              gateway="",
                              RS485=1,
                              local=nome,
                              tec=tec_leitor_entrada,
                              temp_garantia=temp_garantia_leitor_entrada,
                              data_compra=data_compra_leitor_entrada,
                              data_instalacao=data_instalacao_leitor_entrada),
                "Facial 671":Leitor(nome=nome,
                              marca="Hikvision",
                              modelo="671",
                              tipo="Facial",
                              ip="",
                              mascara_sub_rede="",
                              gateway="",
                              RS485=1,
                              local=nome,
                              tec=tec_leitor_entrada,
                              temp_garantia=temp_garantia_leitor_entrada,
                              data_compra=data_compra_leitor_entrada,
                              data_instalacao=data_instalacao_leitor_entrada),
                "Botoeira":Leitor(nome=nome,
                              marca="Intelbras",
                              modelo="BT 3000 IN",
                              tipo="Botoeira",
                              ip="",
                              mascara_sub_rede="",
                              gateway="",
                              RS485=1,
                              local=nome,
                              tec=tec_leitor_entrada,
                              temp_garantia=temp_garantia_leitor_entrada,
                              data_compra=data_compra_leitor_entrada,
                              data_instalacao=data_instalacao_leitor_entrada)}
    
    botoeira = botoeiras[opt_botoeira]
    ima = imas[opt_ima]

    leitor_entrada = leitores[opt_leitor_entrada]
    leitor_entrada.setIp(ip_leitor_entrada)
    leitor_entrada.setMascaraSubRede(mascara_leitor_entrada)
    leitor_entrada.setGateway(gateway_leitor_entrada)

    leitor_saida = leitores[opt_leitor_saida]
    leitor_saida.setIp(ip_leitor_saida)
    leitor_saida.setMascaraSubRede(mascara_leitor_saida)
    leitor_saida.setGateway(gateway_leitor_saida)

    
    try:
        if st.button("Criar Porta"):
            porta = Porta(nome=nome, botoeira_emerg=botoeira, ima=ima, leitor_entrada=leitor_entrada, leitor_saida=leitor_saida)
            st.success("Porta criada com sucesso!")
            andar.criaPorta(porta)
            limpa_formulario_porta()
            salvaClientes(df_clientes)
    except Exception as e:
        st.error(f"Erro ao criar porta: {e}")
    