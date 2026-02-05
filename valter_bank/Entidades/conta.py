#!/usr/bin/env python
# coding: utf-8

# In[21]:


# Módulo que define as classes Conta (Abstrata, Corrente e Poupança)

# Importa a classe base abstrata e o decorador para métodos abstratos
from abc import ABC, abstractmethod

# Importa a classe datetime para registrar a data e hora das transações
from datetime import datetime

# Importa exceção persolalizada para saldo insuficiente
from Utilitarios.exceptions import SaldoInsuficienteError

# Define a super classe - base para os outros tipos de conta
class Conta(ABC):

    # Atributo de classe que calcula quantas contas foram criadas (Armazena apenas na memória)
    _total_contas = 0

    # Construtor da classe
    def __init__(self, numero: int, cliente):

        # Número da conta (atributo protegido)
        self._numero = numero

        # Saldo da conta, iniciando em 0.0
        self._saldo = 0.0

        # Referência ao dono da conta
        self._cliente = cliente

        # Lista para armazenar o histórico de transação
        self._historico = []

        # Incrementa o total de contas criadas
        Conta._total_contas += 1

    # Propriedade para acessar o saldo de forma controlada
    @property
    def saldo(self):

        """ Getter para o saldo, permitindo acesso controlado"""
        return self._saldo

    # Método de classe para consultar o número total de contas
    @classmethod
    def get_total_contas(cls):
        """ Método de classe para obter o número total de contas"""

        return cls._total_contas

    # Método para realizar o depósito
    def depositar(self, valor: float):

        # Adiciona um valor na conta
        if valor > 0:

            # Incrementa o valor na conta
            self._saldo += valor

            # Registra a transação no histórico com data e hora
            self._historico.append((datetime.now(), f"Depósito de R${valor:.2f}"))

            print(f"Depósito de R${valor:.2f} realizado com sucesso!")

        else:
            print("O valor de depósito é inválido.")

    # Método abstrato que deve ser implementado pelas subclasses
    @abstractmethod
    def sacar(self, valor: float):

        """ Método abstrato para sacar valor. Deve ser implementado pelas subclasses"""

        pass

    def extrato(self):

        # Exibe o extrato da conta
        print(f"\n--- Extrato da Conta N° {self._numero} ---")
        print(f"Cliente: {self._cliente.nome}")
        print(f"Saldo atual: R${self._saldo:.2f}")
        print("Histórico de transações:")

        # Caso não haja transações registradas
        if not self._historico:
            print("Nenhuma transação registrada.")

        # Percorrer o histórico e exibir cada transação
        for data, transacao in self._historico:
            print(f"- {data.strftime(' %d/%m/%Y  %H:%M:%S')}: {transacao}")
        print("-------------------------------------\n")

class ContaCorrente(Conta):

    """ Demonstra Polimorfismo ao sobescrever o método sacar """

    # Construtor com limite padrão do cheque especial
    def __init__(self, numero: int, cliente, limite: float = 500.0):

        # Chama o construtor da classe base
        super().__init__(numero, cliente)

        # Define o limite de cheque especial
        self.limite = limite

    # Implementação do método sacar com cheque especial
    def sacar(self, valor: float):

        """ Permite saque utilizando o saldo da conta mais o limite(cheque especial)"""

        if valor <= 0:
            print("Valor de saldo inválido!")
            return

        # Calcula o saldo disponível (saldo + limite)
        saldo_disponivel = self._saldo + self.limite

        # Caso o valor do saque ultrapasse o saldo disponível
        if valor > saldo_disponivel:
            raise SaldoInsuficienteError(saldo_disponivel, valor, "Saldo e limite insuficientes.")

        # Deduz o valor do saque do saldo
        self._saldo -= valor

        # Registra a transação no histórico
        self._historico.append((datetime.now(), f"Saque de R${valor:.2f}"))
        print(f"Saque de R${valor:.2f} realizado com sucesso!")

class ContaPoupanca(Conta):

    # Construtor da poupança, herda do construtor base
    def __init__(self, numero : int, cliente):
        super().__init__(numero, cliente)

    # Saque apenas com saldo disponível
    def sacar(self, valor:float):

        if valor <= 0:
            print("Valor de saque inválido!")
            return

        # Verifica se há saldo suficiente
        if valor > self._saldo:
            raise SaldoInsuficienteError(self._saldo, valor)

        # Deduz o valor do saldo
        self._saldo -= valor

        # Registra a transação no histórico
        self._historico.append((datetime.now(), f"Saque de R${valor:.2f}"))
        print(f"Saque de R${valor:.2f} realizado com sucesso!")
    

