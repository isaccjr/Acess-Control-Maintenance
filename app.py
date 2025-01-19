import streamlit as st
from controle_de_acesso import *
from negocio import *
import pandas as pd
import pickle
from datetime import date

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

    def criaCliente():
        if nome in df_clientes["Nome"].values:
            st.error("Cliente já cadastrado")
            return
        try:
            cliente = Cliente(nome=nome, responsavel=responsavel, tel=tel, instalacoes={})
            st.success("Cliente criado com sucesso!")
            df_clientes.loc[len(df_clientes)] = {"ID":len(df_clientes)+1,
                                                 "Cliente":cliente,
                                                 "Nome":cliente.getNome(),
                                                 "Responsável":cliente.getResponsavel(),
                                                 "Telefone":cliente.getTel(),
                                                 "Instalações":cliente.getInstalacoes()}
            salvaClientes(df_clientes)
        except Exception as e:
            st.error(f"Erro ao criar cliente: {e}")
        limpa_formulario()

    st.title("Registro de cliente")
    nome = st.text_input("Nome:", "", key="nome-cliente")
    responsavel = st.text_input("Responsável:", "", key="responsavel-cliente")
    tel = st.text_input("Telefone:", "", key="tel-cliente")
    if st.button("Criar Cliente", on_click=criaCliente):
      return
    
def registraInstalacao(cliente:Cliente):

    def limpa_formulario():
        st.session_state["nome-instalacao"] = ""
        st.session_state["endereco-instalacao"] = ""
        st.session_state["gps-instalacao"] = ""

    def criaInstalacao():
        if nome in cliente.getInstalacoes().keys():
            st.error("Instalação já cadastrada")
            return
        try:
            instalacao = Instalacoes(nome=nome, endereco=endereco, gps=gps, andares={})
            cliente.criar_intalacao(instalacao)
            st.success("Instalação registrada com sucesso!")
            salvaClientes(df_clientes)
        except Exception as e:
            st.error(f"Erro ao registrar instalação: {e}")
        
        limpa_formulario()
   
    st.title("Registro de Instalações")
    nome = st.text_input("Nome:", "", key="nome-instalacao")
    endereco = st.text_input("Endereço:", "",key= "endereco-intalacao")
    gps = st.text_input("GPS:", "", key="gps-instalacao")
    if st.button("Registrar Instalação", on_click=criaInstalacao):
        return

def registraAndar(instalacao:Instalacoes):
    def limpa_formulario():
        st.session_state["nome-andar"] = ""
    
    def criaAndar():
        nome_andar = st.session_state["nome-andar"]
        if nome_andar in instalacao.getAndares().keys():
            st.error("Divisão/Andar já cadastrada")
            return
        andar = Andar(nome=nome_andar, portas={}, controladoras={})
        if instalacao.criaAndar(andar):
            st.success("Divisão/Andar registrada com sucesso!")
            st.success("Selecione a aba portas e controladora para incluir portas e controladoras nos andares/divisões criados")
            salvaClientes(df_clientes)
        else:
            st.error("Erro ao registrar divisão/andar")
            return
        limpa_formulario()

    st.title("Registro de Divisão/Andar")
    st.write('Digite o nome da divisão ou o número do andar')
    nome_andar = st.text_input("Nome da divisão/andar:",key="nome-andar")
    st.button("Registrar Divisão/Andar", on_click=criaAndar)

def selecionaAndar():
    cliente_opt = st.selectbox("Cliente:", df_clientes["Nome"].to_list())
    cliente:Cliente = df_clientes[df_clientes["Nome"] == cliente_opt].iloc[0]["Cliente"]
    opt_instalacao = st.selectbox("Instalações:", cliente.getInstalacoes().keys())
    instalacao = cliente.getInstalacoes()[opt_instalacao]
    andares = instalacao.getAndares()
    if andares:
        opt_andar = st.selectbox("Andar:", andares.keys())
        return andares[opt_andar]
    else:
        st.write("Lista de andares vazia vai em clientes para registrar andares e divisões")
        return False    

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

def deletaAndar(instalacao:Instalacoes,andar:Andar):
    st.session_state['nome_andar_confirma'] = st.text_input( "Digite o nome do andar para confirmar a exclusão", value=st.session_state['nome_andar_confirma'] )
    if st.button("Confirmar"):
        st.write(f"Nome digitado: {st.session_state['nome_andar_confirma']}")
        st.write(f"Nome do andar a ser deletado: {andar.getNome()}")
        if st.session_state['nome_andar_confirma'] == andar.getNome():
            if instalacao.delAndar(st.session_state['nome_andar_confirma']):
                st.success("Andar deletado com sucesso!")
                salvaClientes(df_clientes)
            else:
                st.warning(f"Erro ao deletar o andar {andar.getNome()}")
        else:
            st.warning("Nome do andar incorreto")

def selecionaCliente()->Cliente:
    opcoes = df_clientes["Nome"].to_list()
    if "Novo Cliente" not in opcoes:
        opcoes.append("Novo Cliente")
    if "Nova Instalação" in opcoes: #coloca a opção de criação na última posição
        opcoes.remove("Nova Instalação")
        opcoes.append("Nova Instalação")
    opt_cliente = st.selectbox("Escolha Cliente:", opcoes)
    if opt_cliente == "Novo Cliente":
            registraCliente()
            
    cliente:Cliente = df_clientes[df_clientes["Nome"] == opt_cliente].iloc[0]["Cliente"]
    return cliente

def selecionaInstalacao(cliente:Cliente)->Instalacoes:
    opcoes_instalacoes = list(cliente.getInstalacoes().keys())
    if "Nova Instalação" not in opcoes_instalacoes:
        opcoes_instalacoes.append("Nova Instalação")
    if "Nova Instalação" in opcoes_instalacoes:
        opcoes_instalacoes.remove("Nova Instalação")
        opcoes_instalacoes.append("Nova Instalação")
        opt_instalacao = st.selectbox("Escolha Instalação:", opcoes_instalacoes)
    if opt_instalacao == "Nova Instalação":
        registraInstalacao(cliente)
    else:
        instalacao = cliente.getInstalacoes()[opt_instalacao]
        return instalacao

def getAndar(instalacao:Instalacoes)->Andar:
    opcoes_andares = list(instalacao.getAndares().keys())
    if "Novo Andar" not in opcoes_andares:
        opcoes_andares.append("Novo Andar")
    if "Novo Andar" in opcoes_andares:
        opcoes_andares.remove("Novo Andar")
        opcoes_andares.append("Novo Andar")
        opt_andar = st.selectbox("Escolha o Andar", opcoes_andares)
    if opt_andar == "Novo Andar":
        registraAndar(instalacao)
    else:
        andar = instalacao.getAndares()[opt_andar]
        return andar

def deletaAndarDIRETO(instalacao,andar):
    instalacao.delAndar(andar.getNome())
    salvaClientes(df_clientes)
    st.success("Andar deletado com sucesso!")

def cria_leitor(marca, modelo, tipo, **kwargs):
    """Cria um objeto Leitor com os argumentos fornecidos."""
    return Leitor(marca=marca, modelo=modelo, tipo=tipo, **kwargs)

def cria_dicionario_leitores(nome, tec_leitor_entrada, temp_garantia_leitor_entrada, data_compra_leitor_entrada, data_instalacao_leitor_entrada):
    """Cria e retorna o dicionário de leitores usando kwargs."""

    parametros_comuns = { # Parâmetros comuns a todos os leitores
        "nome": nome,
        "tec": tec_leitor_entrada,
        "temp_garantia": int(temp_garantia_leitor_entrada), # Converte para int aqui
        "data_compra": data_compra_leitor_entrada,
        "data_instalacao": data_instalacao_leitor_entrada,
        "ip": "",
        "mascara_sub_rede": "",
        "gateway": "",
        "RS485": 1,
        "local": nome,
    }

    return {
        "Cartão": cria_leitor(marca="Dormakaba", modelo="cartão", tipo="cartão", **parametros_comuns),
        "Digital": cria_leitor(marca="Dormakaba", modelo="digital", tipo="digital", **parametros_comuns),
        "Facial 342": cria_leitor(marca="Hikvision", modelo="342", tipo="Facial", **parametros_comuns),
        "Facial 671": cria_leitor(marca="Hikvision", modelo="671", tipo="Facial", **parametros_comuns),
        "Botoeira": cria_leitor(marca="Intelbras", modelo="BT 3000 IN", tipo="Botoeira", **parametros_comuns),
    }

def cria_ima(modelo,kgf,**kwargs):
    return Ima(modelo=modelo,kgf=kgf,**kwargs)

def cria_dicionario_ima(inst_ima, temp_garantia_ima, data_compra_ima, data_instalacao_ima, local):
    parametros_comuns = { # Parâmetros comuns a todos os leitores
        "tec": inst_ima,
        "temp_garantia": int(temp_garantia_ima), # Converte para int aqui
        "data_compra": data_compra_ima,
        "data_instalacao": data_instalacao_ima,
        "local": local,
        "tensao": 12,
        "marca": "Intelbras",
    }
    return {"Padrão 150kgf": cria_ima("FE 20150",150,**parametros_comuns),
            "Padrão 300kgf": cria_ima("FE 10300",300,**parametros_comuns)}

def opcao_cliente():
    st.dataframe(df_clientes)

    if len(df_clientes) == 0:
        registraCliente()
    else:  
        cliente = selecionaCliente()
        if not cliente.getInstalacoes():#Se não existe instalações registradas
            registraInstalacao(cliente)
        else:
            instalacao:Instalacoes = selecionaInstalacao(cliente)   
            if not instalacao.getAndares():#Se não ha andares/divisões registrado
                registraAndar(instalacao)
            else:
                andar:Andar = getAndar(instalacao)
                if andar:
                    # Adicionar CSS para estilizar botões
                    #Cria 3 colunas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("DELETAR ANDAR", use_container_width=True):
                            if 'nome_andar_confirma' not in st.session_state: 
                                st.session_state['nome_andar_confirma'] = ''
                            deletaAndarDIRETO(instalacao,andar)
                    with col2:
                        if st.button('REGISTRAR PORTA', use_container_width=True):
                            pass
                    with col3:
                        if st.button('REGISTRAR CONTROLADORA', use_container_width=True):
                            pass

def expander_fonte_timer(local):
    with st.expander("Fonte Timer", expanded=True):
        opt_fonte_timer = st.selectbox("Fonte Timer", ["Padrão"])
        tec_fonte_timer = st.text_input("Técnico:", "",key=f"tec-fonte-timer-{local}")
        data_compra_fonte_timer = st.date_input("Data de Compra:", value=date.today(), key=f"data-compra-fonte-timer-{local}")
        data_instalacao_fonte_timer = st.date_input("Data de Instalação:", value=date.today(), key=f"data-inst-fonte-timer-{local}")
        temp_garantia_fonte_timer = st.number_input("Tempo de Garantia (meses):", value=3, min_value=3, key=f"garantia-fonte-timer-{local}")
    st.markdown("---")
    return opt_fonte_timer,tec_fonte_timer,data_compra_fonte_timer,data_instalacao_fonte_timer,temp_garantia_fonte_timer

def expander_botoeira(local):
    with st.expander("Botoeira de Emergência", expanded=True):
        opt_botoeira = st.selectbox("Botoeira de Emergência", ["Padrão"])
        tec_bot = st.text_input("Técnico:", "",key= f"tec-bot-{local}")
        data_compra_bot = st.date_input("Data de Compra:", value=date.today(), key=f"data-compra-bot-{local}")
        data_instalacao_bot = st.date_input("Data de Instalação:",value=date.today(), key= f"data-inst-bot-{local}")
        temp_garantia_bot = st.number_input("Tempo de Garantia (meses):", value=3, min_value=3,key= f"garantia-bot-{local}")
    st.markdown("---")
    return opt_botoeira,tec_bot,data_compra_bot,data_instalacao_bot,temp_garantia_bot

def expander_ima(local):
    with st.expander("Imã", expanded=True):
        opt_ima = st.selectbox("Eletroimã", ["Padrão 150kgf", "Padrão 300kgf"])
        inst_ima = st.text_input("Técnico:", "",key= f"inst-ima-{local}")
        data_compra_ima = st.date_input("Data de Compra:",value=date.today(),key= f"data-compra-ima-{local}")
        data_instalacao_ima = st.date_input("Data de Instalação:",value=date.today(),key= f"data-inst-ima-{local}")
        temp_garantia_ima = st.number_input("Tempo de Garantia (meses):", value=3, min_value=3,key= f"garantia-ima-{local}")
    st.markdown("---")
    return opt_ima,inst_ima,data_compra_ima,data_instalacao_ima,temp_garantia_ima

def expander_leitor_entrada(local):
    with st.expander("Leitor de Entrada", expanded=True):
        opt_leitor_entrada = st.selectbox("Leitor de Entrada", ["Cartão", "Digital", "Facial 342","Facial 671"])
        data_compra_leitor_entrada = st.date_input("Data de Compra:",value=date.today(),key= f"data-compra-entrada-{local}")
        data_instalacao_leitor_entrada = st.date_input("Data de Instalação:",value=date.today(),key= f"data-inst-entrada-{local}")
        temp_garantia_leitor_entrada = st.number_input("Tempo de Garantia (meses):", value=3, min_value=3, key=f"garantia-entrada-{local}")
        tec_leitor_entrada = st.text_input("Técnico:", "",key= "tec-entrada-{local}")
        if opt_leitor_entrada in ["Facial 342","Facial 671"]:
            ip_leitor_entrada = st.text_input("IP:", "",key=f"ip-entrada-{local}")
            mascara_leitor_entrada = st.text_input("Máscara de Sub-rede:", "",key=f"mascara-entrada-{local}")
            gateway_leitor_entrada = st.text_input("Gateway:", "",key=f"gateway-entrada-{local}")
        else:
            ip_leitor_entrada = ""
            mascara_leitor_entrada = ""
            gateway_leitor_entrada = ""
    st.markdown("---")
    return opt_leitor_entrada,tec_leitor_entrada,temp_garantia_leitor_entrada,data_compra_leitor_entrada,data_instalacao_leitor_entrada,ip_leitor_entrada,mascara_leitor_entrada,gateway_leitor_entrada

def expander_leitor_saida(local):
    with st.expander("Leitor de Saída", expanded=True):
        opt_leitor_saida = st.selectbox("Leitor de Saída", ["Botoeira", "Cartão", "Digital", "Facial 342","Facial 671"])
        data_compra_leitor_saida = st.date_input("Data de Compra:",value=date.today(),key= f"data-compra-saida-{local}")
        data_instalacao_leitor_saida = st.date_input("Data de Instalação:",value=date.today(),key= f"data-inst-saida-{local}")
        temp_garantia_leitor_saida = st.number_input("Tempo de Garantia (meses):", value=3, min_value=3, key=f"garantia-saida-{local}")
        tec_leitor_saida = st.text_input("Técnico:", "", key=f"tec-saida-{local}")
        if opt_leitor_saida in ["Facial 342","Facial 671"]:
            ip_leitor_saida = st.text_input("IP do Leitor de Saída:", "", key=f"ip-saida-{local}")
            mascara_leitor_saida = st.text_input("Máscara de Sub-rede:", "", key=f"mascara-saida-{local}")
            gateway_leitor_saida = st.text_input("Gateway do Leitor de Saída:", "", key=f"gateway-saida-{local}")
        else:
            ip_leitor_saida = ""
            mascara_leitor_saida = ""
            gateway_leitor_saida = ""
    st.markdown("---")
    return opt_leitor_saida,tec_leitor_saida,temp_garantia_leitor_saida,data_compra_leitor_saida,data_instalacao_leitor_saida,ip_leitor_saida,mascara_leitor_saida,gateway_leitor_saida

def cria_dicionario_de_modelos(data_instalacao_fonte_timer,data_compra_fonte_timer,temp_garantia_fonte_timer,tec_fonte_timer,
                               data_instalacao_bot,data_compra_bot,temp_garantia_bot,tec_bot,
                               inst_ima,temp_garantia_ima,data_compra_ima,data_instalacao_ima,
                               tec_leitor_entrada,temp_garantia_leitor_entrada,data_compra_leitor_entrada,data_instalacao_leitor_entrada,
                               nome):
    
    fonte_timer = {"Padrão": FonteTimer(marca="IPEC",
                                        tec=tec_fonte_timer,
                                        modelo="A2070",
                                        data_instalacao=data_instalacao_fonte_timer,
                                        data_compra=data_compra_fonte_timer,
                                        temp_garantia=temp_garantia_fonte_timer,
                                        local=nome)}
    
    botoeiras = {"Padrão":BotoeiraEmergencia(marca="Intelbras",
                                            modelo = "AS 2010",
                                            local=nome,
                                            tensao=12,
                                            data_instalacao=data_instalacao_bot,
                                            data_compra=data_compra_bot,
                                            temp_garantia=temp_garantia_bot,
                                            tec=tec_bot) }
    
    imas = cria_dicionario_ima(inst_ima=inst_ima,
                               temp_garantia_ima=temp_garantia_ima,
                               data_compra_ima=data_compra_ima,
                               data_instalacao_ima=data_instalacao_ima,
                               local=nome)
    
    leitores = cria_dicionario_leitores(nome=nome,
                                        tec_leitor_entrada=tec_leitor_entrada,
                                        temp_garantia_leitor_entrada=temp_garantia_leitor_entrada,
                                        data_compra_leitor_entrada=data_compra_leitor_entrada,
                                        data_instalacao_leitor_entrada=data_instalacao_leitor_entrada)
    
    return fonte_timer,botoeiras,imas,leitores

def seta_rede_leitor(leitor:Leitor,ip,mascara,gateway):
    leitor.setIp(ip)
    leitor.setMascaraSubRede(mascara)
    leitor.setGateway(gateway)

def opcao_porta():
    def registraPorta(andar:Andar):
        nome = st.text_input("Local:", "",key= "local-porta")
        opt_fonte_timer,tec_fonte_timer,data_compra_fonte_timer,data_instalacao_fonte_timer,temp_garantia_fonte_timer = expander_fonte_timer(nome)
        #Seção Botoeira
        opt_botoeira,tec_bot,data_compra_bot,data_instalacao_bot,temp_garantia_bot = expander_botoeira(nome)
        #Seção Imã
        opt_ima,inst_ima,data_compra_ima,data_instalacao_ima,temp_garantia_ima = expander_ima(nome)
        #Seção Leitor de Entrada
        opt_leitor_entrada,tec_leitor_entrada,temp_garantia_leitor_entrada,data_compra_leitor_entrada,data_instalacao_leitor_entrada,ip_leitor_entrada,mascara_leitor_entrada,gateway_leitor_entrada = expander_leitor_entrada(nome)
        #Seção Leitor de Saida
        opt_leitor_saida,tec_leitor_saida,temp_garantia_leitor_saida,data_compra_leitor_saida,data_instalacao_leitor_saida,ip_leitor_saida,mascara_leitor_saida,gateway_leitor_saida = expander_leitor_saida(nome)
        #Cria dicionarios de modelos
        fonte_timer, botoeiras, imas, leitores = cria_dicionario_de_modelos(
                                                                #fonte timer
                                                                data_instalacao_fonte_timer=data_instalacao_fonte_timer,
                                                                data_compra_fonte_timer=data_compra_fonte_timer,
                                                                temp_garantia_fonte_timer=temp_garantia_fonte_timer,
                                                                tec_bot=tec_fonte_timer,
                                                                #botoeira
                                                                data_instalacao_bot=data_instalacao_bot,
                                                                data_compra_bot=data_compra_bot,
                                                                temp_garantia_bot=temp_garantia_bot,
                                                                tec_bot=tec_bot,
                                                                #ima
                                                                inst_ima=inst_ima,
                                                                temp_garantia_ima=temp_garantia_ima,
                                                                data_compra_ima=data_compra_ima,
                                                                data_instalacao_ima=data_instalacao_ima,
                                                                #leitor
                                                                tec_leitor_entrada=tec_leitor_entrada,
                                                                temp_garantia_leitor_entrada=temp_garantia_leitor_entrada,
                                                                data_compra_leitor_entrada=data_compra_leitor_entrada,
                                                                data_instalacao_leitor_entrada=data_instalacao_leitor_entrada,
                                                                nome=nome)
        fonte_timer = fonte_timer[opt_fonte_timer]
        botoeira = botoeiras[opt_botoeira]
        ima = imas[opt_ima]
        leitor_entrada = leitores[opt_leitor_entrada]
        leitor_saida:Leitor = leitores[opt_leitor_saida]
        leitor_saida._setCompra(data_compra_leitor_saida)
        leitor_saida._setInstalador(tec_leitor_saida)
        leitor_saida._setInstalacao(data_instalacao_leitor_saida)
        leitor_saida._setTempGarantia(temp_garantia_leitor_saida)

        #Seta paremetros de rede nos leitores
        seta_rede_leitor(leitor_entrada,ip_leitor_entrada,mascara_leitor_entrada,gateway_leitor_entrada)
        seta_rede_leitor(leitor_saida,ip_leitor_saida,mascara_leitor_saida,gateway_leitor_saida)
        
        try:
            nome_reg = nome
            if st.button("Criar Porta"):
                porta = Porta(nome=nome_reg, fonte_timer=fonte_timer, botoeira_emerg=botoeira, ima=ima, leitor_entrada=leitor_entrada, leitor_saida=leitor_saida)
                st.success("Porta criada com sucesso!")
                andar.criaPorta(porta)
                salvaClientes(df_clientes)
        except Exception as e:
            st.error(f"Erro ao criar porta: {e}")

    st.title("Registra Porta")
    andar = selecionaAndar()
    if not andar.getPortas(): #Se não existe porta registrada
        registraPorta(andar)
    else:
        portas = list(andar.getPortas().keys())
        if "Nova Porta" not in andar.getPortas().keys():
            portas.append("Nova Porta")
        if "Nova Porta" in andar.getPortas().keys():
            portas.remove("Nova Porta")
            portas.append("Nova Porta")
        opt_porta = st.selectbox("Escolha a porta:", portas)
        if opt_porta == "Nova Porta":
            registraPorta(andar)
        else:
            st.write(andar.getPortas()[opt_porta])

def opcao_controladora():
    def registra_controladora(andar:Andar):
        st.title("Controladora")
        local = st.text_input("Local:", "", key= "local-ctrl")
        nome = st.text_input("Nome:", "", key= "nome-ctrl")
        marca = st.text_input("Marca:", "", key= "marca-ctrl")
        modelo = st.text_input("Modelo:", "", key= "modelo-ctrl")
        ip = st.text_input("IP:", "", key= "ip-ctrl")
        mascara = st.text_input("Máscara de Sub-rede:", "", key= "mascara-ctrl")
        gateway = st.text_input("Gateway:", "", key= "gateway-ctrl")
        tec = st.text_input("Técnico:", "", key= "tec-ctrl")
        data_compra = st.date_input("Data de Compra:", value=date.today(), key= "data-compra-ctrl")
        data_instalacao = st.date_input("Data de Instalação:", value=date.today(), key= "data-inst-ctrl")
        temp_garantia = st.number_input("Tempo de Garantia (meses):", min_value=3, key= "garantia-ctrl")
        
        local_reg,nome_reg,marca_reg,modelo_reg,ip_reg,mascara_reg,gateway_reg,tec_reg,data_compra_reg,data_instalacao_reg,temp_garantia_reg = local,nome,marca,modelo,ip,mascara,gateway,tec,data_compra,data_instalacao,temp_garantia

        if st.button("Criar Controladora"):
            try:
                bateria = Bateria(marca="teste", modelo="teste", local="teste")
                controladora = Controladora(local=local_reg, 
                                            nome=nome_reg, 
                                            marca=marca_reg, 
                                            modelo=modelo_reg, 
                                            bateria=bateria, 
                                            portas=[], 
                                            ip=ip_reg, 
                                            mascara_sub_rede=mascara_reg, 
                                            gateway=gateway_reg, 
                                            tec=tec_reg, 
                                            data_compra=data_compra_reg.strftime("%d-%m-%Y"), 
                                            data_instalacao=data_instalacao_reg.strftime("%d-%m-%Y"), 
                                            temp_garantia=temp_garantia_reg)
                st.success("Controladora criada com sucesso!")
                st.write(controladora)
                andar.criaControladora(controladora)
                salvaClientes(df_clientes)
            except Exception as e:
                st.error(f"Erro ao criar controladora: {e}")
    andar = selecionaAndar()
    if not andar.getControladoras():
        registra_controladora(andar)
    else: #Se existe controladoras registradas
        controladoras = list(andar.getControladoras().keys())
        controladoras.append("Nova Controladora")
        opt_controladora = st.selectbox("Escolha a controladora:", controladoras)
        if opt_controladora == "Nova Controladora":
            registra_controladora(andar)
        else:
            st.write(andar.getControladoras()[opt_controladora])

def opcao_manutencao():
    andar = selecionaAndar()
    col1,col2 = st.columns(2)
    with col1: #Coluna controladora
        controladoras = list(andar.getControladoras().keys())
        controladoras = [controladora + " - " + andar.getControladoras()[controladora].getLocal() for controladora in controladoras]
        if controladoras == []:
            st.write("Não há controladora registrada nesse andar/divisão")
        else:
            opt_controladora = st.selectbox("Escolha a controladora:", controladoras)
            opt_controladora = opt_controladora.split(" - ")[0]
            if st.button("REGISTRAR MANUTENÇÃO"):
                controladora:Controladora = andar.getControladoras()[opt_controladora]
                form_manutencao = st.form("Manutenção")
                with form_manutencao:
                    tec = st.text_input("Técnico respónsavel:",key=f"tec-manutencao-{opt_controladora}")
                    data = st.date_input("Data da manutenção:",value=date.today(),key=f"data-manutencao-{opt_controladora}")
                    tensao_entrada = st.number_input("Tensão de entrada:",value=127,key=f"tensao-entrada-{opt_controladora}")
                    tensao_saida = st.number_input("Tensão de saída:",value=12,key=f"tensao-saida-{opt_controladora}")
                    defeito = st.text_input("Defeito:",key=f"defeito-{opt_controladora}")
                    registra_manutencao_ctrl = st.form_submit_button("Registrar", key=f"registra-manutencao-ctrl-{opt_controladora}")
                    if registra_manutencao_ctrl:
                        controladora.manutencao(tec=tec,data=data,tensao_entrada=tensao_entrada,tensao_saida=tensao_saida,defeito=defeito)
    #Coluna da Manutenção da Porta
    with col2:
        portas = list(andar.getPortas().keys()) #Lista as portas registradas
        if portas == []: #Se não houver portas registras avisa
            st.write("Não há portas registradas nesse andar/divisão")
        else: #Se tiver portas mostra a seleção de portas com a lista
            opt_porta = st.selectbox("Escolha a porta:", portas)
            
            if st.button("REGISTRAR MANUTENÇÃO", key=f"manutencao-porta-{opt_porta}"):
                st.session_state.manutencao_ativa = True
           
            if st.session_state.get('manutencao_ativa', False): # Verifica se a manutenção está ativa
                porta:Porta = andar.getPortas()[opt_porta]
                tec = st.text_input("Técnico responsável:",key=f"tec-manutencao-porta-{opt_porta}")
                data = st.date_input("Data da manutenção", key=f"data-manutencao-porta-{opt_porta}")
                st.write("Em quais foram feito manutenção:")
                tem_fonte_timer = isinstance(porta.getFonteTimer(),FonteTimer)
                equipamentos_porta = ["Imã","Botoeira de Emergência","Leitor de Entrada","Leitor de Saída"]
                if tem_fonte_timer:
                    equipamentos_porta.extend(["Fonte Timer","Bateria da Fonte Timer"])               
                
                # Inicializa o estado dos checkboxes no session_state
                for equipamento in equipamentos_porta:
                    chave_checkbox = f"checkbox_{equipamento}_{opt_porta}"
                    if chave_checkbox not in st.session_state:
                        st.session_state[chave_checkbox] = False
                    st.checkbox(equipamento, key=chave_checkbox)

                if st.button("Registrar Escopo Manutenção", key=f"registra-escopo-porta-{opt_porta}"):
                    st.session_state.escopo_manutencao_ativo = True 
                
                if st.session_state.get('escopo_manutencao_ativo', False): # Verifica se a manutenção está ativa  
                    campos_defeitos = {}
                    for equipamento in equipamentos_porta:
                        chave_checkbox = f"checkbox_{equipamento}_{opt_porta}"
                        if st.session_state[chave_checkbox]:
                            chave_defeito = f"defeito_{equipamento}_{opt_porta}"
                            label_defeito = f"Defeito no(a) {equipamento}"
                            if chave_defeito not in st.session_state:
                                st.session_state[chave_defeito] = ""
                            st.text_input(label_defeito, key=chave_defeito)
                            campos_defeitos[equipamento] = st.session_state[chave_defeito]
                        if equipamento == "Bateria da Fonte Timer":
                            chave_tensao = f"tensao_{equipamento}_{opt_porta}"
                            label_tensao = "Tensão da bateria da fonte timer"
                            if chave_tensao not in st.session_state:
                                st.session_state[chave_tensao] = 12
                            st.number_input(label_tensao, value=st.session_state[chave_tensao], key=chave_tensao)   
                            campos_defeitos[equipamento] = {"tensao": st.session_state[chave_tensao],
                                                            'defeito': st.session_state[chave_defeito]}
                            
                    if st.button("Registra Manutenção", key=f"registra-manutencao-porta-{opt_porta}"):
                        for equipamento, defeito in campos_defeitos.items(): #Itera pelos defeitos registrados
                            if equipamento == "Imã":
                                porta.getIma().manutencao(tec=tec, data=data, defeito=defeito)
                            elif equipamento == "Botoeira de Emergência":
                                porta.getBotoeira_emerg().manutencao(tec=tec, data=data, defeito=defeito)
                            elif equipamento == "Leitor de Entrada":
                                porta.getLeitorEntrada().manutencao(tec=tec, data=data, defeito=defeito)
                            elif equipamento == "Leitor de Saída":
                                porta.getLeitorSaida().manutencao(tec=tec, data=data, defeito=defeito)
                            elif equipamento == "Fonte Timer" and tem_fonte_timer:
                                porta.getFonteTimer().manutencao(tec=tec, data=data, tensao_entrada=12, tensao_saida=12, defeito=defeito)
                            elif equipamento == "Bateria da Fonte Timer" and tem_fonte_timer:
                                chave_tensao = f"tensao_{equipamento}_{opt_porta}"
                                porta.getFonteTimer().getBateria().manutencao(tec=tec, data=data, tensao=st.session_state[chave_tensao], defeito=defeito)
                        salvaClientes(df_clientes)
                        st.success("Manutenção registrada com sucesso!")
                        st.session_state.manutencao_ativa = False
                        st.session_state.escopo_manutencao_ativo = False
                        st.rerun()

                if st.button("Cancelar Manutenção", key=f"cancela-manutencao-porta-{opt_porta}"):
                    st.session_state.manutencao_ativa = False
                    st.session_state.escopo_manutencao_ativo = False
                    st.rerun()

def opcao_historico():
    andar = selecionaAndar()
    portas = list(andar.getPortas().keys()) #Lista as portas registradas
    if portas == []: #Se não houver portas registras avisa
        st.write("Não há portas registradas nesse andar/divisão")
    else: #Se tiver portas mostra a seleção de portas com a lista
        opt_porta = st.selectbox("Escolha a porta:", portas)
        porta:Porta = andar.getPortas()[opt_porta]
        
        leitor_entrada:Leitor = porta.getLeitorEntrada()
        leitor_saida:Leitor = porta.getLeitorSaida()
        ima:Ima = porta.getIma()
        botoeira:BotoeiraEmergencia = porta.getBotoeira_emerg()
        equipamentos_porta = [leitor_entrada,leitor_saida,ima,botoeira]
        if isinstance(porta.getFonteTimer(),FonteTimer):
            fonte_timer:FonteTimer = porta.getFonteTimer()
            bat_fonte_timer:Bateria = fonte_timer.getBateria()
            equipamentos_porta.append(fonte_timer,bat_fonte_timer)  

        for equipamento in equipamentos_porta:
            df_historico_manutencao:pd.DataFrame = equipamento._historico_manutencao
            st.dataframe(df_historico_manutencao)

        




#-----------------------------------------------------------------------------------------------
#                                Inicio da Aplicação Streamlit
#                          Pagina Inicial para escolher o que registrar 
#
#
#
#-----------------------------------------------------------------------------------------------"""

option_dict = {
    "Cliente": opcao_cliente,
    "Controladora": opcao_controladora,
    "Porta": opcao_porta,
    "Manutenção": opcao_manutencao,
    "Histórico": opcao_historico
}
st.title("Controle de Acesso")
st.sidebar.title("Opções")
option = st.sidebar.selectbox("Escolha uma opção:", option_dict.keys())
#Executa a opção
option_dict[option]()