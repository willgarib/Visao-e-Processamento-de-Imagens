from os import walk, startfile
from itertools import compress
from pathlib import Path
from tkinter.filedialog import askopenfilename


class FileScann():
    def __init__(self):
        self.__fill = []

    @property
    def len(self):
        return len(self)
    
    @property
    def fill(self):
        return self.__fill
    
    def __len__(self):
        return len(self.__fill)

    def __repr__(self):
        return f'FileScann()'    

    def __str__(self):
        output = 'FileScann([\n'

        for i in self.__fill:
            output += '           ' + str(i) + ',\n'

        return output[:-2] + '\n])'

    def __getitem__(self, index):
        return self.__fill[index]

    def scann(self, path: str) -> None:
        """ Retorna uma lista com os caminhos de todos os arquivos da pasta 'path'
                e suas sub-pastas """
                        
        tree = list(walk(Path(path)))
        listing = [Path((i[0] + "/" + name).replace('\\', '/')) for i in tree for name in i[2]]
        
        self.__fill = listing

    def search_scann(self, path: str, searchStr: str) -> None:
        """ Retorna uma lista com os caminhos de todos os arquivos da pasta 'path'
                e suas sub-pastas que contenham a sub string 'searchStr' no caminho do arquivo"""

        tree = list(walk(Path(path)))
        listing = [(i[0] + "/" + name).replace('\\', '/') for i in tree for name in i[2]]
        
        # Verificando se tem 'searchStr' no nome e filtrando a lista
        bool_array = map(lambda x: searchStr.upper() in x.upper(), listing)
        listing = compress(listing, bool_array)
        
        # Transformando as strings em Path
        listing = map(Path, listing)
        
        self.__fill = list(listing)

    def save_as_txt(self, fileName: str) -> None:
        """ Salva o conteúdo do scann em um arquivo .txt
                Se o arquivo 'fileName' existir seu conteúdo será perdido"""

        to_str = lambda x: str(x).replace('\\', '/')
        arq = open(fileName, 'w')
        arq.writelines('\n'.join(list(map(to_str, self.fill))))
        arq.close()

        return None

    def load_txt(self, path: str, encoding: str = "utf-8") -> None:
        """ Carrega o conteúdo de um arquivo .txt para o objeto """
        
        with open(Path(path), encoding=encoding) as arq:
            output = arq.read().split('\n')
            
        if output[-1] == '': del output[-1]
        
        self.__fill = list(map(Path, output))
        return None

    def start_file(self, idx: int) -> None:
        startfile(self[idx])

    def s(self, idx):
        self.start_file(idx)  
    
    @staticmethod
    def select_file() -> str:
        return Path(askopenfilename())

if __name__ == '__main__':
    path = "W:\\Pos Vendas\\EMPRESAS"
    
    s = FileScann()
    s.search_scann(path, 'Casam')
   
    input("--- END ---\nPress Enter to Exit...")
