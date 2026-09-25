#Simulador
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
from scipy.signal import butter, filtfilt
from numpy.fft import rfft, rfftfreq

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

        f1 = float(entry_freq_min.get()) # Frequência principal
        f2 = float(20.0)

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
        fc = float(entry_freq_min.get())
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
    except ValueError as e:
        messagebox.showerror("Erro", f"Valor inválido: {e}")

def limpar_dados():
    global sinal_original, sinal_filtrado, tempo
    sinal_original = None
    signal_filtrado = None
    tempo = None
    
    # Opcional: limpa ou reseta os campos da tela
    entry_freq_min.delete(0, tk.END)
    entry_freq_min.insert(0, "5.0")
    entry_freq_samp.delete(0, tk.END)
    entry_freq_samp.insert(0, "100.0")
    entry_ordem.delete(0, tk.END)
    entry_ordem.insert(0, "2")
    entry_ruido.delete(0, tk.END)
    entry_ruido.insert(0, "0.1")
    
    messagebox.showinfo("Limpeza", "Dados reiniciados com sucesso!")


#===========================CONFIG. JANELA===========================
root = tk.Tk()
root.title("Simulador filtro passa-baixa")
root.geometry("450x550")
root.resizable(False, False)

# Caixas de texto
frame_controles = ttk.LabelFrame(root, text=" Parâmetros do Filtro ", padding=15)
frame_controles.pack(fill="both", expand=True, padx=15, pady=15)
lbl_tipo = ttk.Label(frame_controles, text="Tipo de Filtro:")
lbl_tipo.grid(row=0, column=0, sticky="w", pady=8)
cb_filtro = ttk.Combobox(
    frame_controles, 
    values=["Passa-Baixa", "Passa-Alta", "Passa-Faixa", "Rejeita-Faixa"], 
    state="readonly"
)
cb_filtro.grid(row=0, column=1, sticky="ew", pady=8)
cb_filtro.current(0)

# Frequência Mínima
lbl_freq_min = ttk.Label(frame_controles, text="Frequência Mínima (Hz)")
lbl_freq_min.grid(row=1, column=0, sticky="w", pady=8)
entry_freq_min = ttk.Entry(frame_controles)
entry_freq_min.grid(row=1, column=1, sticky="ew", pady=8)
entry_freq_min.insert(0, "5.0")

# Freq. Amostragem

lbl_freq_samp = ttk.Label(frame_controles, text="Frequência de Amostragem (Hz):")
lbl_freq_samp.grid(row=2, column=0, sticky="w", pady=8)

entry_freq_samp = ttk.Entry(frame_controles)
entry_freq_samp.grid(row=2, column=1, sticky="ew", pady=8)
entry_freq_samp.insert(0, "100.0")

# Ordem do Filtro

lbl_ordem = ttk.Label(frame_controles, text="Ordem do Filtro:")
lbl_ordem.grid(row=3, column=0, sticky="w", pady=8)

entry_ordem = ttk.Entry(frame_controles)
entry_ordem.grid(row=3, column=1, sticky="ew", pady=8)
entry_ordem.insert(0, "2")

# Nível de Ruído

lbl_ruido = ttk.Label(frame_controles, text="Nível de Ruído:")
lbl_ruido.grid(row=4, column=0, sticky="w", pady=8)

entry_ruido = ttk.Entry(frame_controles)
entry_ruido.grid(row=4, column=1, sticky="ew", pady=8)
entry_ruido.insert(0, "0.1")

# Alinhamento dos Botões

frame_botoes = ttk.Frame(root)
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

root.mainloop()