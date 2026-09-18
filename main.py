"""
Sistemas Operacionais - IFRS Campus Restinga - ADS 3N - 2026/2
Trabalho de Desenvolvimento: simulador de algoritmos de escalonamento de processos.

Codigo-base em Python. Equivalente ao base.java, com a mesma estrutura de dados
(listas paralelas), o mesmo menu e a mesma saida.

O FCFS ja vem implementado como exemplo de referencia.
Cabe a voce implementar: SJF (preemptivo e nao preemptivo), Prioridade
(preemptivo e nao preemptivo) e Round Robin.
"""

import random

MAXIMO_TEMPO_EXECUCAO = 65535

n_processos = 4


def main():
    tempo_execucao = [0] * n_processos
    tempo_chegada = [0] * n_processos
    prioridade = [0] * n_processos
    tempo_espera = [0] * n_processos
    tempo_restante = [0] * n_processos

    popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    # Escolher algoritmo
    while True:
        alg = input(
            "Escolha o algoritmo?: [1=FCFS 2=SJF Preemptivo 3=SJF Nao Preemptivo  "
            "4=Prioridade Preemptivo 5=Prioridade Nao Preemptivo 6=Round_Robin  "
            "7=Imprime lista de processos 8=Popular processos novamente 9=Sair]: "
        )

        # Se apertar Enter sem digitar nada, mostra o menu novamente
        if alg == "":
            continue

        alg = int(alg)

        if alg == 1:
            FCFS(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 2:
            SJF(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 3:
            SJF(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 4:
            PRIORIDADE(True, tempo_execucao, tempo_espera,
                       tempo_restante, tempo_chegada, prioridade)

        elif alg == 5:
            PRIORIDADE(False, tempo_execucao, tempo_espera,
                       tempo_restante, tempo_chegada, prioridade)

        elif alg == 6:
            Round_Robin(tempo_execucao, tempo_espera, tempo_restante)

        elif alg == 7:
            imprime_processos(tempo_execucao, tempo_espera,
                              tempo_restante, tempo_chegada, prioridade)

        elif alg == 8:
            popular_processos(tempo_execucao, tempo_espera,
                              tempo_restante, tempo_chegada, prioridade)
            imprime_processos(tempo_execucao, tempo_espera,
                              tempo_restante, tempo_chegada, prioridade)

        elif alg == 9:
            break


def popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    aleatorio = int(input("Sera aleatorio?:  "))

    for i in range(n_processos):
        # Popular Processos Aleatorio
        if aleatorio == 1:
            tempo_execucao[i] = random.randint(1, 10)
            tempo_chegada[i] = random.randint(1, 10)
            prioridade[i] = random.randint(1, 15)
        # Popular Processos Manual
        else:
            tempo_execucao[i] = int(input("Digite o tempo de execucao do processo[" + str(i) + "]:  "))
            tempo_chegada[i] = int(input("Digite o tempo de chegada do processo[" + str(i) + "]:  "))
            prioridade[i] = int(input("Digite a prioridade do processo[" + str(i) + "]:  "))

        tempo_restante[i] = tempo_execucao[i]
        tempo_espera[i] = 0


def imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    # Imprime lista de processos
    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_execucao=" + str(tempo_execucao[i]) +
              " tempo_restante=" + str(tempo_restante[i]) +
              " tempo_chegada=" + str(tempo_chegada[i]) +
              " prioridade =" + str(prioridade[i]))


def imprime_stats(espera):
    tempo_espera = list(espera)
    # Implementar o calculo e impressao de estatisticas

    tempo_espera_total = 0.0

    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_espera=" + str(tempo_espera[i]))
        tempo_espera_total = tempo_espera_total + tempo_espera[i]

    print("Tempo medio de espera: " + str(tempo_espera_total / n_processos))


def FCFS(execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    # tempo_chegada = list(chegada)

    processo_em_execucao = 0  # processo inicial no FIFO e o zero

    # implementar codigo do FCFS
    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        if tempo_execucao[processo_em_execucao] == tempo_restante[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = i - 1

        if tempo_restante[processo_em_execucao] == 1:
            if processo_em_execucao == (n_processos - 1):
                break
            else:
                processo_em_execucao = processo_em_execucao + 1
        else:
            tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1
    #

    imprime_stats(tempo_espera)


def SJF(preemptivo, execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)

    tempo = 0
    processos_finalizados = 0
    processo_em_execucao = -1

    while processos_finalizados < n_processos:

        # Procura os processos que já chegaram e ainda não terminaram
        candidatos = []

        for i in range(n_processos):
            if tempo_chegada[i] <= tempo and tempo_restante[i] > 0:
                candidatos.append(i)

        # Se nenhum processo chegou, avanca o tempo
        if len(candidatos) == 0:
            tempo += 1
            continue

        if preemptivo:
            # SJF PREEMPTIVO
            # Escolhe o processo com menor tempo restante
            processo_em_execucao = min(
                candidatos,
                key=lambda i: (tempo_restante[i], tempo_chegada[i], i)
            )

        else:
            # SJF NAO PREEMPTIVO
            # So escolhe um novo processo quando a CPU esta livre
            if processo_em_execucao == -1:
                processo_em_execucao = min(
                    candidatos,
                    key=lambda i: (tempo_execucao[i], tempo_chegada[i], i)
                )

        print("tempo[" + str(tempo) + "]: processo[" +
              str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        # Executa o processo durante 1 unidade de tempo
        tempo_restante[processo_em_execucao] -= 1
        tempo += 1

        # Verifica se o processo terminou
        if tempo_restante[processo_em_execucao] == 0:

            # Tempo de espera =
            # tempo de termino - chegada - tempo de execucao
            tempo_espera[processo_em_execucao] = (
                tempo
                - tempo_chegada[processo_em_execucao]
                - tempo_execucao[processo_em_execucao]
            )

            processos_finalizados += 1

            # CPU fica livre para escolher outro processo
            processo_em_execucao = -1

    imprime_stats(tempo_espera)


def PRIORIDADE(preemptivo, execucao, espera, restante, chegada, prioridade):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    prioridade_temp = list(prioridade)

    # implementar codigo do Prioridade preemptivo e nao preemptivo
    # ...
    #

    imprime_stats(tempo_espera)


def Round_Robin(execucao, espera, restante):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)

    # implementar codigo do Round-Robin
    # ...
    #

    imprime_stats(tempo_espera)


main()
