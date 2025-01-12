from controle_de_acesso import Porta
from controle_de_acesso import Controladora


    
class Andar:
    def __init__(self, nome:str,portas:dict[str,Porta],controladoras:dict[str,Controladora]):
        self._nome = nome,
        self._portas = portas
        self._controladoras = controladoras


    def getNome(self):
        return self._nome
    def setNome(self, nome):
        self._nome = nome

    def criaPorta(self, porta:Porta):
        if isinstance(porta,Porta):
            self._portas[porta.getNome()] = porta
        else:
            raise TypeError("O argumento deve ser do tipo Porta")
        
    def getPortas(self)->dict[str,Porta]:
        return self._portas
    
    def criaControladora(self, controladora:Controladora):
        if isinstance(controladora,Controladora):
            self._controladoras[controladora.getNome()] = controladora
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
    def __init__(self,nome:str,endereco:str,gps:tuple[float,float],andares:dict[str,Andar]):
        self._nome = nome
        self._endereco = endereco
        self._gps = gps
        self._andares = andares
    
    def getNome(self)->str:
        return self._nome
    def setNome(self,nome):
        self._nome = nome
    
    def getEndereco(self)->str:
        return self._endereco
    def setEndereco(self,endereco):
        self._endereco = endereco

    def getGPS(self)->tuple[float,float]:
        return self._gps
    def setGPS(self, gps):
        self._gps = gps

    def getAndares(self)->dict[str,Andar]:
        return self._andares
    
    def criaAndar(self,andar):
        try:
            if isinstance(andar,Andar):
                self._andares[andar.getNome()] = andar
                return True
            else:
                return False
        except:
            return False
    
    def __str__(self):
        return self._nome
        
class Cliente:
    def __init__(self, nome:str, responsavel:str, tel:str, instalacoes:dict[str,Instalacoes]):
        self._nome = nome
        self._responsavel = responsavel
        self._tel = tel
        self._instalacoes = instalacoes

    def getNome(self)->str:
        return self._nome
    def setNome(self,nome):
        self._nome = nome

    def criar_intalacao(self, instalacao:Instalacoes):
        """Método para registrar um instalação dentro de um cliente.
        \n Recebe um objeto do tipo Instalacoes
        \n Retorna false se acontece algum erro registrando a instalação
        \n Retorna true se a instalação foi registrada com sucesso
        \n Levanta um erro se o argumento não for do tipo Instalacoes
        """
        if isinstance(instalacao,Instalacoes):
            try:
                self._instalacoes[instalacao.getNome()] = instalacao
                return True
            except:
                return False
        else:
            raise TypeError("O argumento deve ser do tipo Instalacoes")
    
    def getResponsavel(self)->str:
        return self._responsavel
    def setResponsavel(self,responsavel:str):
        self._responsavel = responsavel
    
    def getTel(self)->str:
        return self._tel
    def setTel(self,tel):
        self._tel = tel

    def getInstalacoes(self)->dict[str,Instalacoes]:
        return self._instalacoes

    def __str__(self):
        return self._nome

