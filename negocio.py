from controle_de_acesso import Porta
from controle_de_acesso import Controladora

class Cliente:
    def __init__(self, nome, responsavel, tel, instalacoes):
        self._nome = nome
        self._responsavel = responsavel
        self._tel = tel
        self._instalacoes = instalacoes

    def getNome(self):
        return self._nome
    def setNome(self,nome):
        self._nome = nome

    def criar_intalacao(self, instalacao):
        self._instalacoes.append(instalacao)
    
    def getResponsavel(self):
        return self._responsavel
    def setResponsavel(self,responsavel):
        self._responsavel = responsavel
    
    def getTel(self):
        return self._tel
    def setTel(self,tel):
        self._tel = tel

    def getInstalacoes(self)->list:
        return self._instalacoes

    def __str__(self):
        return self._nome
    
class Andar:
    def __init__(self, nome:str,portas:list[Porta],controladoras:list[Controladora]):
        self._nome = nome,
        self._portas = portas
        self._controladoras = controladoras


    def getNome(self):
        return self._nome
    def setNome(self, nome):
        self._nome = nome

    def criaPorta(self, porta:Porta):
        if isinstance(porta,Porta):
            self._portas.append(porta)
        else:
            raise TypeError("O argumento deve ser do tipo Porta")
    def listaPortas(self)->list[Porta]:
        nome_portas = []
        for porta in self._portas:
            nome_portas.append(porta.getNome())
        return nome_portas
    
    def criaControladora(self, controladora:Controladora):
        if isinstance(controladora,Controladora):
            self._controladoras.append(controladora)
        else:
            raise TypeError("O argumento deve ser do tipo Controladora")
        
    def listaControladoras(self):
        controladoras = []
        for controladora in self._controladoras:
            controladoras.append(controladora.getLocal())
        return controladoras

    def __str__(self):
        return self._nome

class Instalacoes:
    def __init__(self,nome:str,endereco:str,gps:tuple[float,float],andares:list[Andar]):
        self._nome = nome
        self._endereco = endereco
        self._gps = gps
        self._andares = andares
    
    def getNome(self):
        return self._nome
    def setNome(self,nome):
        self._nome = nome
    
    def getEndereco(self):
        return self._endereco
    def setEndereco(self,endereco):
        self._endereco = endereco

    def getGPS(self):
        return self._gps
    def setGPS(self, gps):
        self._gps = gps

    def getAndares(self):
        return self._andares
    
    def criaAndar(self,andar):
        self._andares.append(andar)

    def __str__(self):
        return self._nome
        