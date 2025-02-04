from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import re


class Equipamento:
    """Classe generica de equipamentos
    \n Recebe
    \n *tipo do equipamento
    \n *marca do equipamento
    \n *modelo do equipamento
    \n *local de instalação
    \n *tensão de funcionamento
    \n *dc se o equipamento é AC ou CC
    \n*instalador, o técnico responsável pela instalação.
    \n*data de compra no formato - dd-mm-aa
    \n*temp de garantia em meses
    \n*data de instalação no formato - dd-mm-aa
    """
    def __init__(self, 
                 tipo:str,
                 marca:str,
                 modelo:str,
                 local:str, #Local de instalação
                 tensao:int =None,
                 dc:bool = True,#Tipo de alimentação Corrente Continua ou Alternada, por padrão Continua DC 
                 instalador=None,
                 data_compra=None,
                 temp_garantia:int=3, #Tempo de garantia em meses
                 data_instalacao=None,):
        
        self._tipo = tipo
        self._marca = marca
        self._modelo = modelo
        self._local = local
        self._tensao = tensao
        self._dc = dc
        self._temp_garantia = temp_garantia

        if instalador:
            self._instalador = instalador
        else:
            self._instalador = None

        if data_instalacao:
            if isinstance(data_instalacao,str):
                self._data_instalacao = datetime.strptime(data_instalacao, "%d-%m-%Y")
            elif isinstance(data_instalacao,datetime) or isinstance(data_instalacao,date):
             self._data_instalacao = data_instalacao
        else:
            self._data_instalacao = None

        if data_compra:
            if isinstance(data_compra,str):
                self._data_compra = datetime.strptime(data_compra, "%d-%m-%Y")
            elif isinstance(data_compra,datetime) or isinstance(data_compra,date):
                self._data_compra = data_compra
        else:
            self._data_compra = None
        
        self._data_ultimo_defeito = None
        self._ultimo_defeito = None
        self._tec_ultima_manutencao =None
        self._historico_manutencao = pd.DataFrame(columns=["Data", "Tec","Defeito"])

    #Getters e Setters
    def getTipoEquipamento(self)->str:
        """Retorna o tipo do equipamento"""
        return self._tipo
    
    def getMarca(self)->str:
        """Retorna a marca do equipamento"""
        return self._marca
    
    def getModelo(self)->str:
        """Retorna o modelo do equipamento"""
        return self._modelo
    
    def getLocal(self)->str:
        """Retorna o local de instalação do equipamento"""
        return self._local
    def _setLocal(self,local):
        self._local = local

    def getTensao(self)->int:
        """Retorna a tensão de funcionamento do equipamento"""
        return self._tensao
    def _setTensao(self,tensao:int):
        self._tensao = tensao

    def isDC(self):
        """Retorna se o equipamento é AC ou DC"""
        return self._dc
    
    def getTempGarantia(self)->int:
        return self._temp_garantia
    def _setTempGarantia(self,temp_garantia:int):
        self._temp_garantia = temp_garantia

    def getInstalador(self)->str:
        """Método que retorna o nome do instalador do equipamento"""
        return self._instalador
    
    def _setInstalador(self,instalador:str):
        self._instalador = instalador
    
    def getCompra(self):
        """Método que retorna a data de compra do equipamento"""
        if self._data_compra: 
            return self._data_compra
        else:
            return f"Não foi definida a data de compra do(a) {self.getTipoEquipamento()}"
    def _setCompra(self,data_compra):
        if isinstance(data_compra,str):
                self._data_compra = datetime.strptime(data_compra, "%d-%m-%Y")
        elif isinstance(data_compra,datetime):
            self._data_compra = data_compra
    
    def getInstalacao(self):
        """Método que retorna a data de instalação"""
        try:
            return self._data_instalacao
        except:
            return f"Não foi definida a data de instalação do(a) {self.getTipoEquipamento()}"
    def _setInstalacao(self,data_instalacao):
        if isinstance(data_instalacao,str):
            self._data_instalacao = datetime.strptime(data_instalacao, "%d-%m-%Y")
        elif isinstance(data_instalacao,datetime):
            self._data_instalacao = data_instalacao
    
    def getDataUltimaManutencao(self):
        try:
            return self._data_ultima_manutencao
        except:
            return "não houve manutenções ainda"
        
    def getTecUltimaManutencao(self):
        if self._tec_ultima_manutencao:
            return self._tec_ultima_manutencao
        else:
            return "não houve manutenções ainda"
    
    def _setUltimoDefeito(self,data,desc_defeito):
        self._ultimo_defeito = desc_defeito
        self._data_ultima_medicao = data
    
    def IsForaDaGarantia(self):
        """Método que informa se esta dentro do prazo de garantia.
        \n Se a uma tempo de garantia definido retorna True ou False.
        \n Se não há informa que não há garantia.
        """
        if self._data_compra:
            if self._data_compra + relativedelta(months=self.getTempGarantia()) < datetime.now():
                return True
            else:
                return False
        else:
            if self.getTempGarantia():
                return f"Não foi definida a data de compra do(a) {self.getTipoEquipamento()}"
            else:
                return "Não foi informado o tempo de garantia"
    
    def reinstalacao(self,instalador,local,data,tensao=None):
        """Método para registrar uma reinstalação do equipamento"""
        if isinstance(data,str):
            self._data_instalacao = datetime.strptime(data, "%d-%m-%Y")
        elif isinstance(data,datetime):
            self._data_instalacao = data
        self._setInstalador(instalador)
        self._setLocal(local)
        if tensao:
            self._setTensao(tensao)

    def manutencao(self,tec,data,defeito):
        """Método para registrar manutenção
        \nRecebe
        \n*Nome do técnico responsavel
        \n*Data da manutenção no formato dd-mm-aa
        \n*Descrição do defeito se há algum
        """
        if isinstance(data,str):
            self._data_ultima_manutencao = datetime.strptime(data, "%d-%m-%Y")
        if isinstance(data,datetime):
            self._data_ultima_manutencao = data
        self._tec_ultima_manutencao = tec
        if defeito:
            self._setUltimoDefeito(self.getDataUltimaManutencao(),defeito)
        nova_medicao = pd.DataFrame({'Data':[self.getDataUltimaManutencao()], 'Tec':[self.getTecUltimaManutencao()], "Defeito":[defeito]})
        self._historico_manutencao = pd.concat([self._historico_manutencao, nova_medicao], ignore_index=True)

class Bateria(Equipamento):
    """
    Classe Bateria

    Recebe: Tudo que um equipamento gênerico tem

    Recebe: 
    Tensão de ciclo (tensão que a bateria flutua em funcionamento)

    Tensão de carregamento (tensão que deve ser usada para carregamento da bateria)

    Histórico de manutenção inclui a tensão medida da bateria mesmo que não esteja com defeito
            
    
    """
    def __init__(self, 
                 marca,
                 modelo,
                 local, #Local de instalação
                 medicao_inicial=12.8, 
                 tensao_ciclo=(13.5,13.8), 
                 tensao_carregamento=(14.3,14.8),
                 tensao =None,
                 dc = True,#Tipo de alimentação Corrente Continua ou Alternada, por padrão Continua DC 
                 instalador=None,
                 data_compra=None,
                 temp_garantia=3, #Tempo de garantia em meses
                 data_instalacao=None,
                 ):
        super().__init__(tipo="Bateria",
                         marca=marca,
                         modelo=modelo,
                         local=local,
                         tensao=None,
                         dc=True,
                         instalador=instalador,
                         data_compra=data_compra,
                         temp_garantia=temp_garantia,
                         data_instalacao=data_instalacao,
                         )
        
        self._tensao_ciclo = tensao_ciclo
        self._tensao_carregamento = tensao_carregamento
        self._tensao_ultima_manutencao = medicao_inicial
        self._data_ultima_manutencao = self._data_instalacao
        if self._data_ultima_manutencao:
            self._prox_medicao = self._data_ultima_manutencao + relativedelta(months=3)
        else:
            self._prox_medicao = None
        self._tensao_baixa = False
        self._historico_manutencao = pd.DataFrame(data={"Data":[self._data_instalacao],
                                                   "Tec":[self._instalador],
                                                   "Defeito":["Nenhum"],
                                                   "Tensão":[medicao_inicial]})

    def __str__(self):
        output=f"""Marca: {self.getMarca()}
Data de Compra: {self.getCompra()}
Data Instalação: {self.getInstalacao()}
Última Medição: {self.getDataUltimaManutencao()}
Tensão de Ciclo: {self.getTensaoCiclo()}
Tensão de Carregamento: {self.getTensaoCarregamento()}"""
        return output

    # Getters and Setters
    def getTensaoCiclo(self):
        """Retorna tensão de ciclo da bateria"""
        return self._tensao_ciclo

    def getTensaoCarregamento(self):
        """Retorna tensão de carregamento da bateria
        """
        return self._tensao_carregamento

    def getTensao(self):
        """Retorna última tensão medida na bateria"""
        return self._tensao_ultima_manutencao

    def IsLowVoltage(self):
        """
        Retorna se a tensão esta baixa
        """
        return self._tensao_baixa

    def getProxManutencao(self):
        """
        Retorna a data da próxima manutenção
        por padrão 3 meses
        """
        if self._prox_manutencao:
            return self._prox_manutencao
        else:
            return "Não há data da última medição"

    def _setTensao(self, tensao):
        if tensao < self.getTensaoCiclo()[0]:
            self._tensao_baixa = True
        self._tensao_ultima_medicao = tensao

    def _proximaManutencao(self): # Adiciona 3 meses à data da última medicão
        self._prox_manutencao = self._data_ultima_manutencao + relativedelta(months=3)
        return self._prox_manutencao

    def manutencao(self, tec, data:str, tensao:float, defeito:str):
        """
        Registra a manutenção
        \nRecebe: 
        \n*Técnico responsável pela manutenção
        \n*Data da manutenção no formato dd-mm-aaaa
        \n*Tensão medida da bateria
        \n*Defeito encontrado na bateria (Não é necessário relatar baixa tensão)
        """
        if isinstance(data,str):
            self._data_ultima_manutencao = datetime.strptime(data, "%d-%m-%Y")
        elif isinstance(data,datetime) or isinstance(data,date):
            self._data_ultima_manutencao = data

        self._tec_ultima_manutencao = tec
        if defeito:
            self._setUltimoDefeito(self.getDataUltimaManutencao(),defeito)
        self._setTensao(tensao)
        nova_medicao = {"Data":self.getDataUltimaManutencao(), 
                        "Tec":self.getTecUltimaManutencao(), 
                        "Defeito":defeito, 
                        "Tensão":tensao}
        df = self._historico_manutencao
        df.loc[len(df)] =nova_medicao
        self._historico_manutencao = df 
        self._prox_manutencao = self._proximaManutencao()

    def getHistorico(self)->pd.DataFrame:
        return self._historico_manutencao
    
class FonteTimer(Equipamento):
    """"
    Classe que define uma FonteTimer
    \nFonteTimer são UPS que tem uma bateria interna e recebem um sinal em um entrada de botoeira e 
    \ncomandam um canal de rele por determinado tempo programado nelas.
    \nRecebe: Tudo que um equipamento gêrico tem
    \nRecebe: Bateria, tensão de saída (geralmente 12V)
    """
    def __init__(self,tec,local:str,marca:str,modelo:str,bateria:Bateria,tensao_saida=12,tensao_entrada=127,data_instalacao=None,temp_garantia=None,data_compra=None):
        super().__init__(tipo="FonteTimer",
                         marca=marca,
                         modelo=modelo,
                         local=local,
                         tensao=tensao_entrada,
                         dc=False,
                         instalador=tec,
                         data_compra=data_compra,
                         data_instalacao=data_instalacao,
                         temp_garantia=temp_garantia)
        #Individuais de uma FonteTimer
        self._bateria = bateria
        self._tensao_saida = tensao_saida
        self._ultima_tensao_saida = self._tensao_saida
        self._ultima_tensao_entrada = self._tensao

    def setBateria(self,bateria:Bateria):
        self._bateria = bateria
    def getBateria(self)->Bateria:
        """Retorna o objeto bateria da fonte timer
        """
        return self._bateria
    
    def getTensaoSaida(self):
        """Recebe tensão de saída da fonte Timer
        \nTensão usada para carregamento da bateria
        """
        return self._tensao_saida
    
    def getUltimaTensaoEntrada(self):
        """Retorna a última tensão medida na entrada da fonte timer"""
        return self._ultima_tensao_entrada
    
    def manutencao(self,tec,data,tensao_entrada=None, tensao_saida=None,defeito=None):
        if tensao_entrada: #Se a tensão de entrada foi medida na manutenção
            self._ultima_tensao_entrada = tensao_entrada
        if tensao_saida: #Se a tensão de saída foi medida na manutenção
            self._tensao_saida = tensao_saida
            if self.getTensaoSaida() < self.getBateria().getTensaoCarregamento()[0]: #Se a tensão da fonte timer esta abaixo da tensão de carregamento da bateria
                defeito += f"\n Tensão da fonte timer abaixo da tensão de carregamento da bateria"
            if self.getTensaoSaida() > self.getBateria().getTensaoCarregamento()[1]: #Se a tensão da fonte timer esta acima da tensão de carregamento da bateria
                defeito += f"\n Tensão da fonte timer acima da tensão de carregamento da bateria"
        
        tensao_ref = self.getTensao()
        tensao_medida = self.getUltimaTensaoEntrada()
        if tensao_ref - tensao_medida > (tensao_ref*0.07) : #Queda de tensão maxima permitida pela NBR5410
            defeito=f"\n Tensão de entrada ({tensao_medida} V) abaixo de {self.getTensao()*0.93}V (-7% do previsto)"
        super().manutencao(tec=tec,data=data,defeito=defeito)

def valida_ipv4(ip:str):
    """Valida se o ip esta dentro do range valido
    \nRecebe uma string com o ip 
    \nRetorna None se o ip é invalido e o ip se for válido
    """ 
    regex = re.compile(r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$") 
    return regex.match(ip) is not None

class EquipamentoDeRede:
    """
Classe EquipamentoDeRede
\nA classe define uma equipamento de rede gênerico com ip,mascara de subrede e gateway
    """
    def __init__(self,ip,mascara_sub_rede,gateway):
        """
        Inicializador da classe Equipamento de Rede
        \nRecebe IP, mascara de sub rede e gateway (todos como string)
        """
        if valida_ipv4(ip):
            self._ip = ip
        if valida_ipv4(mascara_sub_rede):
            self._mascara_sub_rede = mascara_sub_rede
        if valida_ipv4(gateway):
            self._gateway = gateway

    def getIp(self)->str:
        """
    Retorna o IP do Equipamento de Rede
    """
        return self._ip
    def setIp(self,ip:str):
        """
Define IP do equipamento
\nRecebe string com ip
        """
        self._ip = valida_ipv4(ip)
    
    def getMascaraSubRede(self)->str:
        return self._mascara_sub_rede
    def setMascaraSubRede(self,mascara_sub_rede):
        self._mascara_sub_rede = valida_ipv4(mascara_sub_rede)

    def getGateway(self)->str:
        return self._gateway
    def setGateway(self,gateway):
        self._gateway = valida_ipv4(gateway) 

class Leitor(Equipamento,EquipamentoDeRede):
    """Classe Leitor
    A Classe Leitor define uma leitor generico para controle de acesso.
    \nTanto um leitor de cartão,um leitor de digital ou facial.
    \n Recebe um nome, a marca, o modelo do leitor, tipo(cartão,digital,facial),
    \n ip,mascara de subrede,gatewat,RS485, local de instalação, técnico instalador,
     \n tensão de funcionamento, dc (Se é ou não um equipamento com fonte DC), tempo de garantia.
    """
    def __init__(self,
                 nome:str,
                 marca:str,
                 modelo:str,
                 tipo:str,
                 ip:str,
                 mascara_sub_rede:str,
                 gateway:str,
                 RS485:int,
                 local:str,
                 tec:str,
                 tensao=12,
                 dc=True,
                 temp_garantia=3,
                 data_compra:str=None,
                 data_instalacao:str=None):
        
        EquipamentoDeRede.__init__(self,
                                   ip=ip,
                                   mascara_sub_rede=mascara_sub_rede,
                                   gateway=gateway)
        
        Equipamento.__init__(self,
                             tipo=tipo,
                             marca=marca,
                             modelo=modelo,
                             local=local,
                             tensao=tensao,
                             dc=dc,
                             temp_garantia=temp_garantia,
                             instalador=tec,
                             data_compra=data_compra,
                             data_instalacao=data_instalacao)
        self._nome = nome #nome do Leitor
        self._RS485 = RS485 #Endereço RS485 do leitor
     
    def getNome(self)->str:
        """
        Retorna o nome dado ao Leitor
        """
        return self._nome
    def setNome(self,nome:str):
        """
        Define o nome do Leitor
        """
        self._nome = nome
    
    def getRS485(self)->int:
        """Retorna endereço RS485"""
        return self._RS485
    def setRS485(self,RS485):
        """Define o endereço RS485 """
        self._RS485 = RS485
    
    def getIp(self)->str:
        """Retorna o IP do Equipamento de Rede
        \n Se não tem ip retorna falso"""
        try:
            return self._ip
        except:
            return False

class BotoeiraEmergencia(Equipamento):
    """Classe Botoeira de Emergência
    \nBotoeiras de Emergência são usadas para abrirem portas em caso de falha do equipamento.
    \nRecebe marca,modelo,local de instalação,técnico instalador, tensão de funcionamento, padrão 12,
    data de compra, data de instalação e tempo de garantia.
    """
    def __init__(self,marca,modelo,local,tec,tensao=12,data_compra=None, data_instalacao=None,temp_garantia=3):
        super().__init__(tipo="Botoeira de Emergência",
                         marca=marca,
                         modelo=modelo,
                         local=local,
                         tensao=tensao,
                         dc=True,
                         temp_garantia=temp_garantia,
                         instalador=tec,
                         data_instalacao=data_instalacao,
                         data_compra=data_compra)

class Ima(Equipamento):
    """Classe Imã
    \n A Classe Imã define um eletroimã usado para controle de acesso
    \n Recebe marca, modelo,local de instalação,tensao de funcionamento,força do eletroimã,
    \ntécnico responsável pela instalação,data de compra, data de instalação e tempo de garantia.
    """
    def __init__(self,marca:str,modelo:str,local:str,tensao:int,kgf:int,tec,data_compra=None,data_instalacao=None,temp_garantia=3):
        super().__init__(tipo="Eletroimã",
                         marca=marca,
                         modelo=modelo,
                         local=local,
                         tensao=tensao,
                         dc=True,
                         instalador=tec,
                         data_compra=data_compra,
                         data_instalacao=data_instalacao,
                         temp_garantia=temp_garantia)
        self._kgf = kgf

    def getKgf(self)->int:
        """Retorna a força do eletroimã em kgf"""
        return self._kgf
    def setKgf(self,kgf:int):
        self._kgf = int(kgf)

class Porta:
    """Classe Porta
    \n A classe porta define uma porta com controle de acesso.
    \n Toda porta controlada tem um nome definido, uma botoeira de emergência, e um leitor de entrada
    \n algumas portas tem leitor de saída.
    """
    def __init__(self,
                 nome:str,
                 botoeira_emerg:BotoeiraEmergencia,
                 ima:Ima,
                 leitor_entrada:Leitor,
                 leitor_saida:Leitor=None,
                 fonte_timer:FonteTimer=None):
        self._nome = nome

        if isinstance(botoeira_emerg,BotoeiraEmergencia):
            self._botoeira_emerg = botoeira_emerg
        else:
            raise TypeError("O argumento botoeira_emerg deve ser do tipo BotoeiraEmergencia")
        
        if isinstance(ima,Ima):
            self._ima = ima
        else:
            raise TypeError("O argumento ima deve ser do tipo Ima")
        
        if isinstance(leitor_entrada,Leitor):
            self._leitor_entrada = leitor_entrada
        else:
            raise TypeError("O argumento leitor_entrada deve ser do tipo Leitor")
        
        if isinstance(leitor_saida,Leitor) or leitor_saida is None:
            self._leitor_saida = leitor_saida
        else:
            raise TypeError("O argumento leitor_saida deve ser do tipo Leitor")
        
        if isinstance(fonte_timer,FonteTimer) or fonte_timer is None:
            if fonte_timer:
                self._fonte_timer = fonte_timer
            else:
                self._fonte_timer = "Não tem fonte timer"
        else:
            raise TypeError("O argumento fonte_timer deve ser do tipo FonteTimer ou None")
        
        
    

    def getNome(self)->str:
        """Retorna nome da porta"""
        return self._nome
    def setNome(self,nome:str):
        """Define nome da porta"""
        self._nome = nome
   
    def getBotoeira_emerg(self)->BotoeiraEmergencia:
        """Retorna objeto Botoeira de Emergência"""
        return self._botoeira_emerg
    def setBoteira_emerg(self,botoeira):
        """Define Botoeira de Emergência da Porta
        \nRecebe objeto Botoeira de Emergência
        """
        self._botoeira_emerg = botoeira
   
    def getIma(self)->Ima:
        """Retorna objeto eletroimã"""
        return self._ima
    def setIma(self,ima):
        """Define eletroimã da porta
        \nRecebe objeto eletroimã
        """
        self._ima = ima
   
    def getLeitorEntrada(self)->Leitor:
        """Retorna objeto Leitor da Entrada"""
        return self._leitor_entrada
    def setLeitorEntrada(self,leitor):
        self._leitor_entrada = leitor
   
    def getLeitorSaida(self)->Leitor:
        """Retorna objeto Leitor da Saída"""
        if self._leitor_saida:
            return self._leitor_entrada
        else:
            return "Não existe leitor de saída"
    def setLeitorSaida(self,leitor:Leitor):
        """Define leitor de saída
        Recebe objeto leitor
        """
        self._leitor_entrada = leitor
    def getFonteTimer(self)->FonteTimer:
        """Retorna objeto Fonte Timer"""
        try:
            return self._fonte_timer
        except:
            return "Não tem fonte timer"
    def _setFonteTimer(self,fonte_timer:FonteTimer):
        """Define Fonte Timer
        \nRecebe objeto Fonte Timer
        """
        if isinstance(fonte_timer,FonteTimer):
            self._fonte_timer = fonte_timer
            return True
        else:
            return False
    def getFonteTimer(self):
        """Retorna Fonte Timer"""
        try:
            return self._fonte_timer
        except:
            return "Não tem fonte timer"
        

    def __str__(self):
        return self.__dict__.__str__()

class Controladora(FonteTimer,Equipamento):
    """Classe Controladora
    \n Define uma controladora generica, que recebe uma lista de portas a qual controla.
    \nControladoras geralmente são equipamentos de rede ethernet. Então recebe parametros de rede.
    \n IP, mascara de subrede e gateway.
    \n Como todo equipamento recebe a marca, modelo, local de instalação, técnico instalador, data de compra,data de instalação e tempo de garantia.
    \n As portas devem ser passadas em uma lista.
    """
    def __init__(self,
                 local:str,
                 nome:str,
                 marca:str,
                 modelo:str,
                 bateria:Bateria,
                 portas:dict,
                 ip:str,
                 mascara_sub_rede:str,
                 gateway:str,
                 tec,
                 tensao_saida=12,
                 tensao_entrada=127,
                 data_instalacao=None,
                 temp_garantia=None,
                 data_compra=None,
                 quant_portas=4,
                 ):
        
        FonteTimer.__init__(self=self,
                        local=local,
                         marca=marca,
                         modelo=modelo,
                         bateria=bateria,
                         tensao_saida=tensao_saida,
                         tensao_entrada=tensao_entrada,
                         data_instalacao=data_instalacao,
                         data_compra=data_compra,
                         temp_garantia=temp_garantia,
                         tec=tec)
        EquipamentoDeRede.__init__(self,ip=ip,mascara_sub_rede=mascara_sub_rede,gateway=gateway)
        if not isinstance(portas,dict):
            raise TypeError("As portas devem ser passadas em um dicionário")
        for porta in portas:
            if not isinstance(porta,Porta):
                raise TypeError("As portas devem ser do tipo Porta")
        if len(portas) <= quant_portas:
            self._portas = portas
        else:
            raise ValueError("A quantidade de portas passadas deve ser igual ou menor ao definido em quant_portas")
        self._nome = nome
        self._data_ultima_manutencao = self._data_instalacao
        self._portas_restantes = quant_portas - len(portas)


    def getNome(self)->str:
        return self._nome
    def setNome(self,nome:str):
        self._nome = nome

    def getPortas(self)->dict[Porta]:
        """Retorna lista de portas"""
        return self._portas
    def getPorta(self,nome:str)->Porta:
        return self._portas[nome]
    def setPorta(self,porta:Porta):
        """Define a lista de portas da controladora."""
        if isinstance(porta,Porta):
            self._portas[porta.getNome()] = porta

            return True
        else:
            return False


    def getIPs(self)->list[str]:
        """ Retorna os Ips de todos os leitores"""
        ip_leitores=[]
        for porta in self.getPortas():
            if isinstance(porta.getLeitorEntrada(),Leitor):
                ip_leitores.append(porta.getLeitorEntrada().getIp())
            else: 
                ip_leitores.append(porta.getLeitorEntrada())
            if isinstance(porta.getLeitorSaida(),Leitor):
                ip_leitores.append(porta.getLeitorSaida().getIp())
            else: 
                ip_leitores.append(porta.getLeitorSaida())
        return ip_leitores
    
    def getRS485Adresses(self)->list[int]:
        """Retorna os endereços RS485 de todos os leitores"""
        RS485_leitores=[]
        for porta in self.getPortas():
            entrada, saida = porta.getLeitorEntrada(), porta.getLeitorSaida()
            for leitor in [entrada,saida]:
                if isinstance(leitor,Leitor):
                    RS485_leitores.append(leitor.getRS485())
                else:
                    RS485_leitores.append(leitor)
        return RS485_leitores
    
    def _getConflitoEndereco(self,list_end:list[str])->list[(int,str)]:
        conflitantes = []
        for idx,ip in enumerate(list_end):
            list_end.remove(ip)
            if ip in list_end:
                conflitantes.append((idx,ip))
        return conflitantes
        
    def TemConflitoDeIP(self):
        ip_leitores= self.getIPs()
        conflitantes = self._getConflitoEndereco(ip_leitores)
        if conflitantes:
            return conflitantes
        else:
            return False 
    def TemConflitoDeRS485(self):
        RS485_leitores = self.getRS485Adresses() 
        conflitantes = self._getConflitoEndereco(RS485_leitores)
        if conflitantes:
            return conflitantes
        else:
            return False

    def __str__(self):
        return self.__dict__.__str__()
