import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
from scipy.signal import butter, filtfilt
from numpy.fft import rfft, rfftfreq

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================

sinal_original = None
sinal_filtrado = None
tempo = None
frequencia = None


# ============================================================
# FUNÇÃO PARA GERAR O SINAL
# ============================================================

def gerar_sinal():

    global sinal_original, tempo

    try:
        # Obtém os valores da interface
        fs = float(entry_amostragem.get())
        ruido_nivel = float(entry_ruido.get())

        f1 = float(entry_freq1.get())
        f2 = float(entry_freq2.get())

        duracao = float(entry_duracao.get())

        # Verificação
        if fs <= 0:
            raise ValueError("A frequência de amostragem deve ser maior que zero.")

        if duracao <= 0:
            raise ValueError("A duração deve ser maior que zero.")

        if f1 <= 0 or f2 <= 0:
            raise ValueError("As frequências devem ser maiores que zero.")

        # Frequência de Nyquist
        if f1 >= fs / 2 or f2 >= fs / 2:
            raise ValueError(
                "As frequências do sinal devem ser menores que a frequência de Nyquist."
            )

        # Criação do vetor de tempo
        tempo = np.arange(0, duracao, 1 / fs)

        # ====================================================
        # SINAL DO SENSOR
        # ====================================================

        # Componente lenta:
        # representa a variação principal da temperatura
        amplitude1 = 5

        # Componente de maior frequência:
        # representa uma interferência/componente indesejada
        amplitude2 = 1.5

        sinal_sensor = (
            25
            + amplitude1 * np.sin(2 * np.pi * f1 * tempo)
            + amplitude2 * np.sin(2 * np.pi * f2 * tempo)
        )

        # ====================================================
        # RUÍDO BRANCO
        # ====================================================

        ruido = np.random.normal(
            0,
            ruido_nivel,
            len(tempo)
        )

        # Sinal final recebido pelo sistema
        sinal_original = sinal_sensor + ruido

        # Limpa o gráfico anterior
        limpar_graficos()

        messagebox.showinfo(
            "Sinal gerado",
            "O sinal do sensor foi gerado com sucesso."
        )

    except ValueError as erro:
        messagebox.showerror(
            "Erro",
            str(erro)
        )


# ============================================================
# FUNÇÃO PARA APLICAR O FILTRO
# ============================================================

def aplicar_filtro():

    global sinal_filtrado, frequencia

    if sinal_original is None:
        messagebox.showwarning(
            "Aviso",
            "Primeiro gere o sinal."
        )
        return

    try:

        fs = float(entry_amostragem.get())
        fc = float(entry_freq_corte.get())
        ordem = int(entry_ordem.get())

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

        # ====================================================
        # FILTRO BUTTERWORTH PASSA-BAIXA
        # ====================================================

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

        # ====================================================
        # FFT
        # ====================================================

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

        # ====================================================
        # ATUALIZA OS GRÁFICOS
        # ====================================================

        atualizar_graficos(
            fft_original,
            fft_filtrado
        )

    except ValueError as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )


# ============================================================
# FUNÇÃO PARA ATUALIZAR OS GRÁFICOS
# ============================================================

def atualizar_graficos(
    fft_original,
    fft_filtrado
):

    # Limpa todos os eixos
    for eixo in eixos:
        eixo.clear()

    # ========================================================
    # GRÁFICO 1 - SINAL ORIGINAL
    # ========================================================

    eixos[0].plot(
        tempo,
        sinal_original,
        label="Sinal original"
    )

    eixos[0].set_title(
        "Sinal Original - Domínio do Tempo"
    )

    eixos[0].set_xlabel(
        "Tempo (s)"
    )

    eixos[0].set_ylabel(
        "Amplitude"
    )

    eixos[0].legend()
    eixos[0].grid(True)

    # ========================================================
    # GRÁFICO 2 - SINAL FILTRADO
    # ========================================================

    eixos[1].plot(
        tempo,
        sinal_filtrado,
        label="Sinal filtrado"
    )

    eixos[1].set_title(
        "Sinal Filtrado - Domínio do Tempo"
    )

    eixos[1].set_xlabel(
        "Tempo (s)"
    )

    eixos[1].set_ylabel(
        "Amplitude"
    )

    eixos[1].legend()
    eixos[1].grid(True)

    # ========================================================
    # GRÁFICO 3 - FFT DO SINAL ORIGINAL
    # ========================================================

    eixos[2].plot(
        frequencia,
        fft_original,
        label="FFT original"
    )

    eixos[2].set_title(
        "FFT do Sinal Original"
    )

    eixos[2].set_xlabel(
        "Frequência (Hz)"
    )

    eixos[2].set_ylabel(
        "Amplitude"
    )

    eixos[2].set_xlim(
        0,
        min(50, max(frequencia))
    )

    eixos[2].legend()
    eixos[2].grid(True)

    # ========================================================
    # GRÁFICO 4 - FFT DO SINAL FILTRADO
    # ========================================================

    eixos[3].plot(
        frequencia,
        fft_filtrado,
        label="FFT filtrada"
    )

    eixos[3].set_title(
        "FFT do Sinal Filtrado"
    )

    eixos[3].set_xlabel(
        "Frequência (Hz)"
    )

    eixos[3].set_ylabel(
        "Amplitude"
    )

    eixos[3].set_xlim(
        0,
        min(50, max(frequencia))
    )

    eixos[3].legend()
    eixos[3].grid(True)

    # Ajusta os gráficos
    figura.tight_layout()

    # Atualiza a interface
    canvas.draw()


# ============================================================
# FUNÇÃO PARA LIMPAR
# ============================================================

def limpar_graficos():

    for eixo in eixos:
        eixo.clear()

        eixo.set_xlabel("")
        eixo.set_ylabel("")
        eixo.set_title("")

    figura.tight_layout()

    canvas.draw()


# ============================================================
# JANELA PRINCIPAL
# ============================================================

janela = tk.Tk()

janela.title(
    "Simulador de Filtro Passa-Baixa - Sensor de Temperatura"
)

janela.geometry(
    "1400x900"
)


# ============================================================
# FRAME DE CONTROLES
# ============================================================

frame_controles = ttk.LabelFrame(
    janela,
    text="Parâmetros do Sistema"
)

frame_controles.pack(
    side=tk.TOP,
    fill=tk.X,
    padx=10,
    pady=10
)


# ============================================================
# TIPO DE FILTRO
# ============================================================

ttk.Label(
    frame_controles,
    text="Tipo de filtro:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

combo_filtro = ttk.Combobox(
    frame_controles,
    values=[
        "Passa-Baixa"
    ],
    state="readonly",
    width=15
)

combo_filtro.current(0)

combo_filtro.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# ============================================================
# FREQUÊNCIA 1
# ============================================================

ttk.Label(
    frame_controles,
    text="Frequência 1 (Hz):"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)

entry_freq1 = ttk.Entry(
    frame_controles,
    width=10
)

entry_freq1.insert(
    0,
    "0.2"
)

entry_freq1.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


# ============================================================
# FREQUÊNCIA 2
# ============================================================

ttk.Label(
    frame_controles,
    text="Frequência 2 (Hz):"
).grid(
    row=0,
    column=4,
    padx=5,
    pady=5
)

entry_freq2 = ttk.Entry(
    frame_controles,
    width=10
)

entry_freq2.insert(
    0,
    "10"
)

entry_freq2.grid(
    row=0,
    column=5,
    padx=5,
    pady=5
)


# ============================================================
# FREQUÊNCIA DE CORTE
# ============================================================

ttk.Label(
    frame_controles,
    text="Frequência de corte (Hz):"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

entry_freq_corte = ttk.Entry(
    frame_controles,
    width=10
)

entry_freq_corte.insert(
    0,
    "2"
)

entry_freq_corte.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# ============================================================
# FREQUÊNCIA DE AMOSTRAGEM
# ============================================================

ttk.Label(
    frame_controles,
    text="Frequência de amostragem (Hz):"
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5
)

entry_amostragem = ttk.Entry(
    frame_controles,
    width=10
)

entry_amostragem.insert(
    0,
    "100"
)

entry_amostragem.grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)


# ============================================================
# ORDEM DO FILTRO
# ============================================================

ttk.Label(
    frame_controles,
    text="Ordem do filtro:"
).grid(
    row=1,
    column=4,
    padx=5,
    pady=5
)

entry_ordem = ttk.Entry(
    frame_controles,
    width=10
)

entry_ordem.insert(
    0,
    "4"
)

entry_ordem.grid(
    row=1,
    column=5,
    padx=5,
    pady=5
)


# ============================================================
# NÍVEL DE RUÍDO
# ============================================================

ttk.Label(
    frame_controles,
    text="Nível de ruído:"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

entry_ruido = ttk.Entry(
    frame_controles,
    width=10
)

entry_ruido.insert(
    0,
    "0.5"
)

entry_ruido.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)


# ============================================================
# DURAÇÃO DO SINAL
# ============================================================

ttk.Label(
    frame_controles,
    text="Duração (s):"
).grid(
    row=2,
    column=2,
    padx=5,
    pady=5
)

entry_duracao = ttk.Entry(
    frame_controles,
    width=10
)

entry_duracao.insert(
    0,
    "10"
)

entry_duracao.grid(
    row=2,
    column=3,
    padx=5,
    pady=5
)


# ============================================================
# BOTÃO GERAR SINAL
# ============================================================

botao_gerar = ttk.Button(
    frame_controles,
    text="Gerar Sinal",
    command=gerar_sinal
)

botao_gerar.grid(
    row=3,
    column=0,
    padx=10,
    pady=10
)


# ============================================================
# BOTÃO APLICAR FILTRO
# ============================================================

botao_filtrar = ttk.Button(
    frame_controles,
    text="Aplicar Filtro",
    command=aplicar_filtro
)

botao_filtrar.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)


# ============================================================
# BOTÃO LIMPAR
# ============================================================

botao_limpar = ttk.Button(
    frame_controles,
    text="Limpar Resultados",
    command=limpar_graficos
)

botao_limpar.grid(
    row=3,
    column=2,
    padx=10,
    pady=10
)


# ============================================================
# ÁREA DOS GRÁFICOS
# ============================================================

figura = Figure(
    figsize=(12, 8),
    dpi=100
)

eixos = [
    figura.add_subplot(2, 2, 1),
    figura.add_subplot(2, 2, 2),
    figura.add_subplot(2, 2, 3),
    figura.add_subplot(2, 2, 4)
]


# ============================================================
# CANVAS
# ============================================================

canvas = FigureCanvasTkAgg(
    figura,
    master=janela
)

canvas.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)


# ============================================================
# EXECUÇÃO DA INTERFACE
# ============================================================

janela.mainloop()