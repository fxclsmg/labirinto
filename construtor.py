import random

class Direcao:
    nenhum = -1
    cima = 0
    direita = 1
    baixo = 2
    esquerda = 3
    direcao = nenhum

    def __init__(self):
        self.direcao = random.randint(0,3) 

class Celula:
    x, y = (-1, -1)
    valor = ""
    valor2 = ""
    
    def __init__(self, x=-1, y=-1, valor="", valor2=""):
        self.x = x
        self.y = y
        self.valor = valor
        self.valor2 = valor2

class Labirinto:
    saidas = []
    borda = []
    labirinto = []
    caminho = []
    aberturas = 0
    parede = ""
    fundo = ""
    porta = ""
    minotauro = Celula()
    Teseu = Celula()

    def gerar_matriz(self, altura, largura):
        self.labirinto = []

        # valor minimo de 3 para garantir espaço central mínimo = 1
        valor_minimo = 3
        if altura < valor_minimo:
            raise Exception(f"Altura inválida: {altura}. Altura mínima permitida: {valor_minimo}")
        if largura < valor_minimo:
            raise Exception(f"Largura inválida: {largura}. Largura mínima permitida: {valor_minimo}")

        x = 0
        y = 0

        while y < altura:
            self.labirinto.append([])
            while x < largura:
                self.labirinto[y].append(Celula(x, y, self.fundo))
                x += 1
            x = 0
            y += 1

        return self.labirinto

    def mostrar(self):
        for linha in self.labirinto:
            for celula  in linha:
                print(celula.valor, " ", end="")
            print()
    



    def colocar_parede_borda_matriz(self):
        if len(self.labirinto) == 0:
            raise Exception("Labirinto vazio")

        linha_0 = self.labirinto[0]
        i = 0
        while i < len(linha_0):
            c = Celula(i,0,self.parede)
            linha_0[i] = c
            self.borda.append((i,0))
            i += 1
            
        linha_i = self.labirinto[len(self.labirinto)-1]
        i = 0
        while i < len(linha_i):
            c = Celula(i,len(self.labirinto)-1,self.parede)
            linha_i[i] = c
            self.borda.append((i,len(self.labirinto)-1))
            i += 1

        i = 0
        coluna_0 = len(self.labirinto)
        while i < coluna_0:
            c = Celula(0,i,self.parede)
            self.labirinto[i][0] = c
            self.borda.append((0,i))
            i += 1

        i = 0
        coluna_0 = len(self.labirinto)
        while i < coluna_0:
            c = Celula(len(self.labirinto[0])-1,i,self.parede)
            self.labirinto[i][len(self.labirinto[0])-1] = c
            self.borda.append((len(self.labirinto[0])-1, i))
            i += 1
        
        # remove os cantos
        j = 0
        while j < 2:
            self.borda.remove((0,0))
            self.borda.remove((0, len(self.labirinto)-1))
            self.borda.remove((len(self.labirinto[0])-1, 0))
            self.borda.remove((len(self.labirinto[0])-1, len(self.labirinto)-1))
            j += 1

        return self.labirinto
    
    def set_abertura(self, quantidade):
        total_borda = len(self.borda)
        
        if (quantidade > total_borda):
            raise Exception(f"Quantidade inválida: {quantidade}. Valor deve ser menor igual a {total_borda}")
        
        self.aberturas = quantidade

    def inserir_porta_pocicao_aleatoria_borda_matriz(self):
        total_borda = len(self.borda)
        
        if (self.aberturas > total_borda):
            raise Exception(f"Quantidade inválida: {self.aberturas }. Valor deve ser menor igual a {total_borda}")

        i = 0
        while i < self.aberturas:
            pos = random.randint(0,len(self.borda)-1)
            x, y = self.borda[pos]

            if self.labirinto[y][x].valor != self.porta:
                self.labirinto[y][x].valor = self.porta
                self.saidas.append(self.labirinto[y][x])                
                i += 1
            else:
                self.borda.remove(self.borda[pos])

        return self.labirinto
    
    def caminho_livre(self, celula, direcao):
        celula_destino = Celula(celula.x, celula.y, celula.valor)   
        d = Direcao()
        x = celula.x
        y = celula.y 

        topo = y == 0
        fim = x == len(self.labirinto[0])-1  
        fundo = y == len(self.labirinto)-1
        inicio = x == 0

        if direcao.direcao == d.cima:
            if topo: 
                return False
            
        if direcao.direcao == d.direita:
            if fim:
                return False
                
        if direcao.direcao == d.baixo:
            if fundo:
                return False
            
        if direcao.direcao == d.esquerda:
            if inicio:
                return False
            
        if direcao.direcao == d.cima:
            celula_destino.y = celula.y-1          
            
        if direcao.direcao == d.direita:
            celula_destino.x = celula.x+1
                
        if direcao.direcao == d.baixo:
            celula_destino.y = celula.y+1
            
        if direcao.direcao == d.esquerda:
            celula_destino.x = celula.x-1

        celula_destino = self.labirinto[celula_destino.y][celula_destino.x]

        if celula_destino.valor == self.parede:
            return False
        
        if celula_destino.valor == self.porta:
            return False

        return True


    def caminhar(self, celula, direcao, valor):
        celula_destino = Celula(celula.x, celula.y, celula.valor)
        d = Direcao()

        if direcao.direcao == d.cima:
            celula_destino.y = celula.y-1          
            
        if direcao.direcao == d.direita:
            celula_destino.x = celula.x+1
                
        if direcao.direcao == d.baixo:
            celula_destino.y = celula.y+1
            
        if direcao.direcao == d.esquerda:
            celula_destino.x = celula.x-1

        celula_destino = self.labirinto[celula_destino.y][celula_destino.x]
        self.labirinto[celula_destino.y][celula_destino.x].valor = valor
        celula_destino.valor = valor


        return celula_destino

    def inserir_caminho_com_tamanho_curvas(self, tamanho, curvas):
        if len(self.saidas) <= 0:
            raise Exception("Labirinto sem saída")
        
        if tamanho < curvas-1:
            raise Exception(f"Tamanho {tamanho} deve ser maior que curvas {curvas}")
        
        if curvas < 0:
            raise Exception(f"Não é possível fazer {curvas} curvas")
        
        if tamanho > (len(self.labirinto[0]) * len(self.labirinto)):
            raise Exception(f"Não é possível caminho com tamanho {tamanho}")
        
        for saida in self.saidas:
            max_tentativas = len(self.labirinto[0]) * len(self.labirinto)
            tam = tamanho            
            celula_atual = saida
            self.caminho.append(saida)
            curva = 0
            while curva < curvas:
                reta = tamanho // curvas
                direcao = Direcao()
                while reta > 0:
                    if self.caminho_livre(celula_atual, direcao):
                        celula_atual = self.caminhar(celula_atual, direcao, self.porta)
                        self.caminho.append(celula_atual)
                        reta -= 1
                        tam -= 1
                    else:
                        direcao = Direcao()
                    if tam < 0:
                        break
                    max_tentativas -= 1
                    if max_tentativas <= 0:
                        break
                curva += 1

    def posicionar_minotauro(self, minotauro):
        pos = random.randint(0,len(self.caminho)-1)
        self.minotauro.x = self.caminho[pos].x
        self.minotauro.y = self.caminho[pos].y
        self.labirinto[minotauro.y][minotauro.x] = minotauro

    def algoritmo_mao_direira(self, celula, direcao):
        d = Direcao()
        linha_0 = celula.x == 0
        coluna_0 = celula.y == 0
        linha_i = celula.x == len(self.labirinto[0])-1
        coluna_i = celula.y == len(self.labirinto)-1

        celula_destino = Celula(celula.x, celula.y, celula.valor, celula.valor2)  

        if linha_0 or coluna_0 or linha_i or coluna_i:
            return celula_destino, direcao

        cima = Celula(celula_destino.x, celula_destino.y-1)
        direita = Celula(celula_destino.x+1, celula_destino.y) 
        baixo = Celula(celula_destino.x, celula_destino.y+1)
        esquerda = Celula(celula_destino.x-1, celula_destino.y)

        if direcao.direcao == d.cima:
            try:
                celula_destino = self.labirinto[cima.y][cima.x]
            except:
                pass

        if direcao.direcao == d.direita:
            try:
                celula_destino = self.labirinto[direita.y][direita.x]
            except:
                pass

        if direcao.direcao == d.baixo:
            try:
                celula_destino = self.labirinto[baixo.y][baixo.x]
            except:
                pass

        if direcao.direcao == d.esquerda:
            try:
                celula_destino = self.labirinto[esquerda.y][esquerda.x]
            except:
                pass

        bateu_parede = celula_destino.valor == self.parede
        vazio = celula_destino.valor == self.fundo
        ja_passou = celula_destino.valor == self.minotauro.valor2

        if bateu_parede or vazio:
            if direcao.direcao == d.cima:
                direcao.direcao = d.direita
            elif direcao.direcao == d.direita:
                direcao.direcao = d.baixo
            elif direcao.direcao == d.baixo:
                direcao.direcao = d.esquerda
            elif direcao.direcao == d.esquerda:
                direcao.direcao = d.cima   
            return celula, direcao 
         
        elif ja_passou: 

            try:
                celula_cima = self.labirinto[cima.y][cima.x]
            except:
                celula_cima = Celula()

            try:
                celula_direita = self.labirinto[direita.y][direita.x]
            except:
                celula_direita = Celula()

            try:
                celula_baixo = self.labirinto[baixo.y][baixo.x]
            except:
                celula_baixo = Celula()
            
            try:
                celula_esquerda = self.labirinto[esquerda.y][esquerda.x]
            except:
                celula_esquerda = Celula()

            passou_cima = celula_cima.valor == self.minotauro.valor2
            passou_direita = celula_direita.valor == self.minotauro.valor2
            passou_baixo = celula_baixo.valor == self.minotauro.valor2
            passou_esquerda = celula_esquerda.valor == self.minotauro.valor2

            travas = [self.fundo, self.parede, self.minotauro.valor2]

            travou_cima = celula_cima.valor in travas
            travou_direita = celula_direita.valor in travas
            travou_baixo = celula_baixo.valor in travas
            travou_esquerda = celula_esquerda.valor in travas
            
            if travou_cima and travou_direita and travou_baixo and travou_esquerda:
                
                if passou_cima or passou_direita or passou_baixo or passou_esquerda:
                    celulas_livres = []
                
                    if passou_cima:
                        celulas_livres.append(celula_cima)
                    if passou_direita:
                        celulas_livres.append(celula_direita)
                    if passou_baixo:
                        celulas_livres.append(celula_baixo)
                    if passou_esquerda:
                        celulas_livres.append(celula_esquerda)

                    pos = random.randint(0,len(celulas_livres)-1)
                    celula_destino = celulas_livres[pos]
                    celula_destino.valor = self.minotauro.valor
                    celula_destino.valor2 = self.minotauro.valor2

                    if celula.valor == self.minotauro.valor:
                        self.labirinto[celula.y][celula.x].valor = self.minotauro.valor2

                    direcao = Direcao()
                    return celula_destino, direcao
            
            direcao = Direcao()
            return celula, direcao

        self.labirinto[celula_destino.y][celula_destino.x].valor = self.minotauro.valor
        celula_destino.valor = self.minotauro.valor
        celula_destino.valor2 = self.minotauro.valor2

        if celula.valor == self.minotauro.valor:
           self.labirinto[celula.y][celula.x].valor = self.minotauro.valor2
        
        return celula_destino, direcao

    def minotauro_saiu(self):
        linha_0 = self.minotauro.x == 0
        coluna_0 = self.minotauro.y == 0
        linha_i = self.minotauro.x == len(self.labirinto[0])-1
        coluna_i = self.minotauro.y == len(self.labirinto)-1

        return linha_0 or coluna_0 or linha_i or coluna_i
    
        
