import os
import sys

class Formatador():

    # base
    base = {
        "inicio": "\033[",
        "fim": "m",
        "texto_normal": "0",
        "separador": ";",
    }

    # comandos prontos
    comando_resetar_texto = base["inicio"] +  base["texto_normal"] +  base["fim"]

    # estilos
    estilos = {
        "estilo_negrito": "1"
    }

    # textos
    textos = {
        "texto_preto": "30",
        "texto_vermelho": "31",
        "texto_verde": "32",
        "texto_amarelo": "33",
        "texto_azul": "34",
        "texto_magenta": "35",
        "texto_ciano": "36",
        "texto_branco": "37",
    }

    # fundos
    fundos = {
        "fundo_preto": "40",
        "fundo_vermelho": "41", 
        "fundo_verde": "42", 
        "fundo_amarelo": "43", 
        "fundo_azul": "44", 
        "fundo_magenta": "45", 
        "fundo_ciano": "46", 
        "fundo_branco": "47" 
    }


    def texto_formatado(self,texto):
        return texto.startswith(self.base["inicio"])
    
    def texto_resetado(self,texto):
        return texto.endswith(self.comando_resetar_texto)
    
    def validar_comando(self, comando):
        try:
            self.base[comando]
        except:
            try:
                self.estilos[comando]
            except:
                try:
                    self.textos[comando]
                except:
                    try:
                        self.fundos[comando]
                    except:
                        raise Exception(f"Comando inválido: {comando}")
        return
    
    def pegar_cod_comando(self, comando):
        cod_comando = ""

        try:
            cod_comando = self.base[comando]
        except:
            try:
                cod_comando = self.estilos[comando]
            except:
                try:
                    cod_comando = self.textos[comando]
                except:
                    try:
                        cod_comando = self.fundos[comando]
                    except:
                        raise Exception(f"Comando inválido: {comando}")

        return cod_comando 
    
    def separar_formatacao(self, i):
        formatacao = i.split(self.base["inicio"])
        formatacao = formatacao[1].split(self.base["fim"])
        formatacao = formatacao[0]
        return formatacao

    def separar_f_inicio_texto_f_fim(self, texto):
        formatacao_incial = ""
        formatacao_final = ""

        if self.texto_formatado(texto):
            formatacao_incial, texto = texto.split(self.base["fim"], 1)
            formatacao_incial += self.base["fim"]

        if self.texto_resetado(texto):
            texto, formatacao_final = texto.split(self.comando_resetar_texto, 1)
            formatacao_final += self.comando_resetar_texto

        return formatacao_incial, texto, formatacao_final
    
    def formatar(self, texto, comando):
        self.validar_comando(comando)
        cod_comando = self.pegar_cod_comando(comando) 

        i, texto, f = self.separar_f_inicio_texto_f_fim(texto)

        if len(i) == 0:
            i = self.base["inicio"]
            i += cod_comando 
            i += self.base["fim"]
        else:
            formatacao = self.separar_formatacao(i)

            lista_formatacao = formatacao.split(self.base["separador"])

            if not cod_comando in lista_formatacao:
                formatacao += self.base["separador"]
                formatacao += cod_comando
            else:
                lista_formatacao.remove(cod_comando)
                if len(lista_formatacao) > 1:
                    formatacao = self.base["separador"].join(lista_formatacao)
                else:
                    if len(lista_formatacao) == 1:
                        formatacao = lista_formatacao[0]
                    else:
                        formatacao = ""

            if len(formatacao) != 0:            
                i = self.base["inicio"] + formatacao + self.base["fim"]
            else:
                i = ""

        if (len(f) == 0):
            f = self.comando_resetar_texto

        return i + texto + f

    def mostrar_exemplo(self):
        texto_normal = self.comando_resetar_texto + "Texto normal"
        print(texto_normal)

        formatos = [self.estilos, self.textos, self.fundos]
        for formato in formatos:
            for chave in formato:
                texto_formatado = self.formatar(chave, chave)
                print(texto_formatado, formato[chave])
                print(self.separar_f_inicio_texto_f_fim(texto_formatado))
                texto_formatado = self.formatar(texto_formatado, chave)

    def limpar(self):
        os.system("cls" if os.name == "nt" else "clear")
        sys.stdout.write("\033[2;1H")  # Move cursor para linha 1, coluna 1
        print("\033[2J")  # Limpa a tela uma única vez