import numpy as np

from scipy.signal import butter, filtfilt

from numpy.fft import rfft, rfftfreq


# ====================================================
# VARIÁVEIS
# ====================================================

sinal_original = None
sinal_filtrado = None
tempo = None
frequencia = None


# ====================================================
# FUNÇÃO PARA GERAR O SINAL
# ====================================================

def gerar_sinal(fs, ruido_nivel, f1, f2, amplitude1, amplitude2, duracao):

    global sinal_original, tempo

    # Verificação dos dados

    if fs <= 0:
        raise ValueError(
            "A frequência de amostragem deve ser maior que zero."
        )

    if duracao <= 0:
        raise ValueError(
            "A duração deve ser maior que zero."
        )

    if f1 <= 0 or f2 <= 0:
        raise ValueError(
            "As frequências devem ser maiores que zero."
        )

    if amplitude1 < 0 or amplitude2 < 0:
        raise ValueError(
            "As amplitudes não podem ser negativas."
        )


    # ====================================================
    # FREQUÊNCIA DE NYQUIST
    # ====================================================

    if f1 >= fs / 2 or f2 >= fs / 2:
        raise ValueError(
            "As frequências do sinal devem ser menores que a frequência de Nyquist."
        )


    # ====================================================
    # VETOR DE TEMPO
    # ====================================================

    tempo = np.arange(
        0,
        duracao,
        1 / fs
    )


    # ====================================================
    # PRIMEIRA SENOIDE
    # ====================================================

    sinal1 = amplitude1 * np.sin(
        2 * np.pi * f1 * tempo
    )


    # ====================================================
    # SEGUNDA SENOIDE
    # ====================================================

    sinal2 = amplitude2 * np.sin(
        2 * np.pi * f2 * tempo
    )


    # ====================================================
    # SINAL DO SENSOR SEM RUÍDO
    # ====================================================

    sinal_sensor = 25 + sinal1 + sinal2


    # ====================================================
    # RUÍDO BRANCO
    # ====================================================

    ruido = np.random.normal(
        0,
        ruido_nivel,
        len(tempo)
    )


    # ====================================================
    # SINAL FINAL RECEBIDO PELO SISTEMA
    # ====================================================

    sinal_original = sinal_sensor + ruido


    return tempo, sinal_original


# ====================================================
# FUNÇÃO PARA APLICAR O FILTRO E CALCULAR A FFT
# ====================================================

def aplicar_filtro(sinal_original, fs, fc, ordem):

    global sinal_filtrado, frequencia


    # ====================================================
    # VERIFICAÇÕES
    # ====================================================

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


    # ====================================================
    # FILTRO BUTTERWORTH PASSA-BAIXA
    # ====================================================

    b, a = butter(
        ordem,
        fc,
        btype="low",
        fs=fs
    )


    # ====================================================
    # APLICAÇÃO DO FILTRO
    # ====================================================

    sinal_filtrado = filtfilt(
        b,
        a,
        sinal_original
    )


    # ====================================================
    # FFT
    # ====================================================

    n = len(sinal_original)


    # FFT DO SINAL ORIGINAL

    fft_original = np.abs(
        rfft(sinal_original)
    )


    # FFT DO SINAL FILTRADO

    fft_filtrado = np.abs(
        rfft(sinal_filtrado)
    )


    # ====================================================
    # FREQUÊNCIAS DA FFT
    # ====================================================

    frequencia = rfftfreq(
        n,
        1 / fs
    )


    return sinal_filtrado, fft_original, fft_filtrado, frequencia


# ====================================================
# TESTE
# ====================================================

# Valores utilizados no teste

fs = 100

ruido_nivel = 0.5

f1 = 0.5

f2 = 10

amplitude1 = 5

amplitude2 = 1.5

duracao = 10


# ====================================================
# GERAR O SINAL
# ====================================================

tempo, sinal_original = gerar_sinal(
    fs,
    ruido_nivel,
    f1,
    f2,
    amplitude1,
    amplitude2,
    duracao
)


# ====================================================
# APLICAR O FILTRO
# ====================================================

fc = 2

ordem = 4


sinal_filtrado, fft_original, fft_filtrado, frequencia = aplicar_filtro(
    sinal_original,
    fs,
    fc,
    ordem
)


# ====================================================
# RESULTADOS
# ====================================================

print("======================================")
print("TESTE REALIZADO COM SUCESSO")
print("======================================")

print("Frequência de amostragem:", fs, "Hz")

print("Frequência 1:", f1, "Hz")

print("Frequência 2:", f2, "Hz")

print("Amplitude 1:", amplitude1)

print("Amplitude 2:", amplitude2)

print("Nível de ruído:", ruido_nivel)

print("Frequência de corte:", fc, "Hz")

print("Ordem do filtro:", ordem)

print("Duração:", duracao, "segundos")

print("Quantidade de amostras:", len(tempo))

print("--------------------------------------")

print("Primeiros valores do sinal original:")

print(sinal_original[:10])

print("--------------------------------------")

print("Primeiros valores do sinal filtrado:")

print(sinal_filtrado[:10])

print("--------------------------------------")

print("Quantidade de pontos da FFT:")

print(len(fft_original))

print("--------------------------------------")

print("Teste finalizado.")