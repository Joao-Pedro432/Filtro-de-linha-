import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
from scipy.signal import butter, filtfilt
from numpy.fft import rfft, rfftfreq

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Variaveis globais

sinal_original = None
sinal_filtrado = None
tempo = None
frequencia = None

# Função para gerar um sinal

def gerar_sinal():
    global sinal_original, tempo

    try:

        # Obtém os valores da interface
        fs = float(????????)
        ruido_nivel = float(??????)

        f1 = float(??????)
        f2 = float(??????)

        amplitude1 = float(?????????)
        amplitude2 = float(?????????)

        duracao = float(?????????)

        # Verificação dos dados

        if fs <= 0:
            raise ValueError("A frequência de amostragem deve ser maior que zero.")

        if duracao <= 0:
            raise ValueError("A duração deve ser maior que zero.")

        if f1 <= 0 or f2 <= 0:
            raise ValueError("As frequências devem ser maiores que zero.")

        # Frequência de Nyquist
        if f1 >= fs / 2 or f2 >= fs / 2:
            raise ValueError(
                "As frequências do sinal devem ser menores que a frequência de Nyquist.")

        # Criação do vetor de tempo

        tempo = np.arange(0, duracao, 1 / fs)

        # Primeira senoide

        sinal1 = amplitude1 * np.sin(2 * np.pi * f1 * tempo)


        # Segunda senoide

        sinal2 = amplitude2 * np.sin(2 * np.pi * f2 * tempo)

        # Geração do ruído branco

        ruido = np.random.normal(0, ruido_nivel, len(tempo))

        # Sinal final recebido pelo sistema

        sinal_original = sinal_sensor + ruido

#Função para filtrar o sinal

def aplicar_filtro():

    global sinal_filtrado, frequencia

    if sinal_original is None:
        messagebox.showwarning(
            "Aviso",
            "Primeiro gere o sinal."
        )
        return

    try:

        fs = float(???????)
        fc = float(???????)
        ordem = int(???????)

        # Verificações

        if fc <= 0:
            raise ValueError(
                "A frequência de corte deve ser maior que zero."
            )

        if fc >= fs / 2:
            raise ValueError(
                "A frequência de corte deve ser menor que a frequência de Nyquist."
            )

        if ordem <= 0:
            raise ValueError(
                "A ordem do filtro deve ser maior que zero."
            )

        # Criação do filtro Passa-baixa

         b, a = butter(
            ordem,
            fc,
            btype="low",
            fs=fs
        )

        # Aplicação do filtro
        sinal_filtrado = filtfilt(
            b,
            a,
            sinal_original
        )

        # Cálculo da FFT

        n = len(sinal_original)

        # FFT do sinal original
        fft_original = np.abs(
            rfft(sinal_original)
        )

        # FFT do sinal filtrado
        fft_filtrado = np.abs(
            rfft(sinal_filtrado)
        )

        # Frequências correspondentes à FFT
        frequencia = rfftfreq(
            n,
            1 / fs
        )