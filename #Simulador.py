#Simulador
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
from scipy.signal import butter, filtfilt
from numpy.fft import rfft, rfftfreq

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variáveis
sinal_original = None
sinal_filtrado = None
tempo = None

#===========================PROCESSAMENTO E VALORES===========================
def gerar_sinal():
    global sinal_original, tempo

    try:

        # Obtém os valores da interface
        fs = float(entry_freq_samp.get())
        ruido_nivel = float(entry_ruido.get())

        f1 = float(entry_freq_sinal.get()) # Frequência principal
        f2 = float(entry_freq2.get())

        amplitude1 = float(1.0)
        amplitude2 = float(0.5)

        duracao = float(5.0) # Duração em segundos

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

        sinal_sensor = sinal1 + sinal2
        sinal_original = sinal_sensor + ruido

        messagebox.showinfo("Sucesso", "Sinal gerado com sucesso!")

    except ValueError as e:
        messagebox.showerror("Erro", f"Valor inválido: {e}")

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

        fs = float(entry_freq_samp.get())
        fc = float(entry_freq_corte.get())
        ordem = int(entry_ordem.get())

        tipo_filtro = cb_filtro.get()

        # Frequências usadas pelo Passa-Faixa e Rejeita-Faixa
        fc1 = fc / 2
        fc2 = fc * 1.5

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

        # Escolha do tipo de filtro

        if tipo_filtro == "Passa-Baixa":

            b, a = butter(
                ordem,
                fc,
                btype="low",
                fs=fs
            )

        elif tipo_filtro == "Passa-Alta":

            b, a = butter(
                ordem,
                fc,
                btype="high",
                fs=fs
            )

        elif tipo_filtro == "Passa-Faixa":

            b, a = butter(
                ordem,
                [fc1, fc2],
                btype="bandpass",
                fs=fs
            )

        elif tipo_filtro == "Rejeita-Faixa":

            b, a = butter(
                ordem,
                [fc1, fc2],
                btype="bandstop",
                fs=fs
            )

        else:

            raise ValueError(
                "Este tipo de filtro ainda não está disponível."
            )

        # Aplicação do filtro

        sinal_filtrado = filtfilt(
            b,
            a,
            sinal_original
        )

        # Cálculo da FFT

        n = len(sinal_original)

        fft_original = np.abs(
            rfft(sinal_original)
        )

        fft_filtrado = np.abs(
            rfft(sinal_filtrado)
        )

        # Frequências da FFT

        frequencia = rfftfreq(
            n,
            1 / fs
        )

        # Atualiza os gráficos

        atualizar_graficos(
            fft_original,
            fft_filtrado
        )

    except ValueError as e:

        messagebox.showerror(
            "Erro",
            f"Valor inválido: {e}"
        )


def limpar_dados():
    global sinal_original, sinal_filtrado, tempo
    sinal_original = None
    sinal_filtrado = None
    tempo = None
    
    # Opcional: limpa ou reseta os campos da tela
    entry_freq_sinal.delete(0, tk.END)
    entry_freq_sinal.insert(0, "5.0")
    entry_freq_samp.delete(0, tk.END)
    entry_freq_samp.insert(0, "100.0")
    entry_freq_corte.delete(0, tk.END)
    entry_freq_corte.insert(0, "10.0")
    entry_ordem.delete(0, tk.END)
    entry_ordem.insert(0, "2")
    entry_ruido.delete(0, tk.END)
    entry_ruido.insert(0, "0.1")
    entry_freq2.delete(0, tk.END)
    entry_freq2.insert(0, "15.0")

    if eixos is not None:
        limpar_graficos()
    
    messagebox.showinfo("Limpeza", "Dados reiniciados com sucesso!")

def atualizar_campos_interface(event=None):
    tipo_filtro = cb_filtro.get()

    if tipo_filtro in ["Passa-Faixa", "Rejeita-Faixa"]:
        label_freq2.grid(row=2, column=0, sticky="w", pady=8)
        entry_freq2.grid(row=2, column=1, sticky="ew", pady=8)
    else:
        label_freq2.grid_remove()
        entry_freq2.grid_remove()

#=======================CRIAÇÃO DOS GRÁFICOS============================

# Função para atualizar os gráficos

def atualizar_graficos(
    fft_original,
    fft_filtrado
):

    global figura, eixos, canvas
    
    for eixo in eixos:
        eixo.clear()

    # GRÁFICO 1 - SINAL ORIGINAL

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

    # GRÁFICO 2 - SINAL FILTRADO

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

    # GRÁFICO 3 - FFT DO SINAL ORIGINAL

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

    # GRÁFICO 4 - FFT DO SINAL FILTRADO

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


# FUNÇÃO PARA LIMPAR

def limpar_graficos():

    for eixo in eixos:
        eixo.clear()

        eixo.set_xlabel("")
        eixo.set_ylabel("")
        eixo.set_title("")

    figura.tight_layout()

    canvas.draw()


#===========================CONFIG. JANELA===========================
root = tk.Tk()
root.title("Simulador filtro passa-baixa")
root.geometry("1100x650")
root.resizable(False, False)

# Divisão dos controles dos gráficos
main_pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#--- Coluna dos controles ---
frame_esq = ttk.Frame(main_pane)
main_pane.add(frame_esq, weight=1)

# --- Controles ---
# Caixas de texto
frame_controles = ttk.LabelFrame(frame_esq, text=" Parâmetros do Filtro ", padding=15)
frame_controles.pack(fill="both", expand=True, padx=15, pady=15)
frame_controles.columnconfigure(1, weight=1)
lbl_tipo = ttk.Label(frame_controles, text="Tipo de Filtro:")
lbl_tipo.grid(row=0, column=0, sticky="w", pady=8)
cb_filtro = ttk.Combobox(
    frame_controles, 
    values=["Passa-Baixa", "Passa-Alta", "Passa-Faixa", "Rejeita-Faixa"], 
    state="readonly"
)
cb_filtro.grid(row=0, column=1, sticky="ew", pady=8)
cb_filtro.current(0)
cb_filtro.bind("<<ComboboxSelected>>", atualizar_campos_interface)

# Frequência do Sinal
lbl_freq_sinal = ttk.Label(
    frame_controles,
    text="Frequência do Sinal (Hz):"
)
lbl_freq_sinal.grid(row=1, column=0, sticky="w", pady=8)

entry_freq_sinal = ttk.Entry(frame_controles)
entry_freq_sinal.grid(row=1, column=1, sticky="ew", pady=8)
entry_freq_sinal.insert(0, "5.0")

# Frequência 2
label_freq2 = ttk.Label(frame_controles, text="Frequência 2 (Hz):")
label_freq2.grid(row=2, column=0, sticky="w", pady=8)

entry_freq2 = ttk.Entry(frame_controles)
entry_freq2.grid(row=2, column=1, sticky="ew", pady=8)
entry_freq2.insert(0, "15.0")


# Frequência de Corte
lbl_freq_corte = ttk.Label(
    frame_controles,
    text="Frequência de Corte (Hz):"
)
lbl_freq_corte.grid(row=3, column=0, sticky="w", pady=8)

entry_freq_corte = ttk.Entry(frame_controles)
entry_freq_corte.grid(row=3, column=1, sticky="ew", pady=8)
entry_freq_corte.insert(0, "10.0")

# Freq. Amostragem

lbl_freq_samp = ttk.Label(frame_controles, text="Frequência de Amostragem (Hz):")
lbl_freq_samp.grid(row=4, column=0, sticky="w", pady=8)

entry_freq_samp = ttk.Entry(frame_controles)
entry_freq_samp.grid(row=4, column=1, sticky="ew", pady=8)
entry_freq_samp.insert(0, "100.0")

# Ordem do Filtro

lbl_ordem = ttk.Label(frame_controles, text="Ordem do Filtro:")
lbl_ordem.grid(row=5, column=0, sticky="w", pady=8)

entry_ordem = ttk.Entry(frame_controles)
entry_ordem.grid(row=5, column=1, sticky="ew", pady=8)
entry_ordem.insert(0, "2")

# Nível de Ruído

lbl_ruido = ttk.Label(frame_controles, text="Nível de Ruído:")
lbl_ruido.grid(row=6, column=0, sticky="w", pady=8)

entry_ruido = ttk.Entry(frame_controles)
entry_ruido.grid(row=6, column=1, sticky="ew", pady=8)
entry_ruido.insert(0, "0.1")

# Alinhamento dos Botões

frame_botoes = ttk.Frame(frame_esq)
frame_botoes.pack(fill="x", padx=15, pady=10)

# Botão Gerar Sinal

btn_gerar = ttk.Button(frame_botoes, text="Gerar Sinal", command= gerar_sinal)
btn_gerar.pack(side="left", expand=True, padx=2)

# Botão Aplicar Filtro

btn_aplicar = ttk.Button(frame_botoes, text="Aplicar Filtro", command= aplicar_filtro)
btn_aplicar.pack(side="left", expand=True, padx=2)

# Botão Limpar

btn_limpar = ttk.Button(frame_botoes, text="Limpar", command= limpar_dados)
btn_limpar.pack(side="left", expand=True, padx=2)

#--- Seção de Gráficos ---
# Grade 2x2 dos gráficos
frame_dir = ttk.LabelFrame(main_pane, text="Visualização Gráfica", padding=10)
main_pane.add(frame_dir, weight=3)

# Figura dos 4 gráficos
figura, eixos = plt.subplots(2, 2, figsize=(8.5, 5.5))
eixos = eixos.flatten()

# Conversão
canvas = FigureCanvasTkAgg(figura, master=frame_dir)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Ajuste do layout inicial
figura.tight_layout(pad=2.0)
canvas.draw()

atualizar_campos_interface()
root.mainloop()