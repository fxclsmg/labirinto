import construtor
import terminal
import time

# formata parede para diferenciar texto no terminal
lab = construtor.Labirinto()
tf = terminal.Formatador()
direcao=construtor.Direcao()
direcao.direcao = direcao.cima
# tf.mostrar_exemplo()

parede = "1" # representa parede
parede = tf.formatar(parede,"texto_vermelho")
parede = tf.formatar(parede,"estilo_negrito")
lab.parede = parede

lab.fundo = "0"

lab.porta = tf.formatar("2","estilo_negrito")
lab.porta = tf.formatar(lab.porta,"texto_verde")

aberturas = 2

# altura matriz, largura matriz, valor das celulas

lab.gerar_matriz(25, 23)
lab.colocar_parede_borda_matriz() 
lab.set_abertura(aberturas)
lab.inserir_porta_pocicao_aleatoria_borda_matriz() 
lab.inserir_caminho_com_tamanho_curvas(150, 50)

rastro = "3"
rastro = tf.formatar(rastro, "texto_amarelo")
rastro = tf.formatar(rastro, "estilo_negrito")

minotauro_atual = "3"
minotauro_atual = tf.formatar(minotauro_atual, "texto_azul")
minotauro_atual = tf.formatar(minotauro_atual, "estilo_negrito")

lab.minotauro = construtor.Celula(-1, -1, minotauro_atual, rastro)

lab.posicionar_minotauro(lab.minotauro)

fim = True
while fim:

    if lab.minotauro_saiu():
        fim = False

    time.sleep(0.111)

    lab.minotauro, direcao = lab.algoritmo_mao_direira(lab.minotauro, direcao)

    tf.limpar()
    lab.mostrar()

