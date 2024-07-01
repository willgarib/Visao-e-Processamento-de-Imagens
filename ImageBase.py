import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from os import stat
from FileScann import FileScann


class ImageBase:
    def __init__(self, path: str):
        self._path = Path(path)
        self._classes = {None}
        
        # Varrendo os arquivos
        scann = FileScann()
        scann.scann(self._path)   
        self._data = pd.DataFrame(scann.fill, columns=['id'])
        
        # Adicionando informações da classes ao DataFrame
        self._data['nome'] = self._data['id'].map(lambda path: getattr(path, 'stem'))
        self._data[['classe', 'extra']] = self._data.nome.str.split('$', n=1, expand=True)
        self._data[['iluminacao', 'fundo']] = self._data.extra.str.split('@', n=1, expand=True)
        self._data.drop(columns=['nome', 'extra'], inplace=True)
        
        self._data['classe'] = self._data.classe.str.extractall(r'([a-zA-z])').unstack(-1, '').sum(1)
        self._data.classe.apply(lambda x: self._classes.update(list(x))); self._classes.remove(None)
        self._data['classe'] = self._data.classe.apply(sorted)
        # _classes já contém todas as classes
        
        # Mapeando cada lista/classe com o aux_map
        aux_map = {}
        for i, classe in enumerate(sorted(self._classes)):
            aux_map[classe] = i
        self._classes = aux_map
        
        # Separando as classes em colunas
        for new_column in self._classes.keys():
            self._data[new_column] = False
            
        # Levando as informações da classes para sua respectiva coluna
        def many_hot(linha): # Notation "One-Hot"
            self._data.loc[linha, self._data.loc[linha].classe] = True
        self._data.index.to_series().apply(many_hot)
        
        # Index
        self._data.index = self._data['id'].map(lambda path: getattr(path, 'name'))
        self._data.rename(columns={'id': 'path'}, inplace=True)
        
        # Adicionando informação sobre o tamanho dos arquivos
        self._data['size'] = self._data.path.apply(
            lambda file: stat(file).st_size/1048576
        )
        
        # Informações sobre Classes
        self._info_classes = {}
        with open('./classes.csv', 'r') as info_classes:
            info_classes.readline()
            for linha in info_classes:
                info = linha.strip().split(',')
                self._info_classes[info[1]] = info[0]
        self._info_classes = pd.DataFrame(
            [self._info_classes, self._classes, self._data.drop(columns=['path', 'classe', 'size', 'fundo', 'iluminacao']).sum()],
            index=['Classe', 'Código', 'Número de Amostras']
            ).T.sort_values('Código')
        
        # Informações sobre Iluminação
        self._info_iluminacao = {}
        with open('./iluminacoes.csv', 'r') as info_iluminacao:
            info_iluminacao.readline()
            for linha in info_iluminacao:
                info = linha.strip().split(',')
                self._info_iluminacao[info[1]] = info[0]
            
        contagem = self._data.iluminacao.value_counts()
        self._info_iluminacao = pd.DataFrame(
            [contagem.index.to_series().map(self._info_iluminacao), contagem],
            index=['Iluminação', 'Número de Amostras']
            ).T
        self._iluminacoes = contagem.index.to_list()
        
        # Informações sobre Fundo
        self._info_fundo = {}
        with open('./fundo.csv', 'r') as info_fundo:
            info_fundo.readline()
            for linha in info_fundo:
                info = linha.strip().split(',')
                self._info_fundo[info[1]] = info[0]
            
        contagem = self._data.fundo.value_counts()
        self._info_fundo = pd.DataFrame(
            [contagem.index.to_series().map(self._info_fundo), contagem],
            index=['Fundo', 'Número de Amostras']
            ).T
        self._fundos = contagem.index.to_list()
        
        # Meta
        self._meta = {
            "Classes": list(self._classes.keys()),
            "Número de Classes": len(self._classes),
            "Fundos": self._info_fundo['Fundo'].to_list(),
            "Iluminações": self._info_iluminacao['Iluminação'].to_list(),
            "Número de Imagens": self._data.shape[0],
            "Tamanho Total (MB)": self._data['size'].sum().round(2),
            }
    
    @staticmethod
    def __getSize(file: str):
        return stat(file).st_size / 1048576
    
    @property
    def path(self) -> str:
        return self._path
    
    @property
    def data(self) -> pd.DataFrame:
        return self._data
    
    @property
    def classes(self) -> dict:
        return self._classes
    
    @property
    def iluminacoes(self) -> list:
        return self._classes
    
    @property
    def fundos(self) -> list:
        return self._classes
    
    @property
    def meta(self):
        return self._meta
    
    @property
    def info_classes(self):
        return self._info_classes
    
    @property
    def info_iluminacoes(self):
        return self._info_iluminacao
    
    @property
    def info_fundos(self):
        return self._info_fundo
    
    def __getitem__(self, idx):
        return self.data.iloc[idx]
    
    def getById(self, id: str):
        return plt.imread(self.data.loc[id].path)

    def getSampleOfClass(self, n: int, label: str = '') -> tuple:
        if label != '': condition = self.data[label]
        else: condition = np.ones(self.data.shape[0], dtype=bool)
        
        title = ['Img ' + str(i) for i in range(1, n+1)]
        return self.data[condition].sample(n), title
    
    def meta_dados():
        pass
