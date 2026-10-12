# Simulador de Filtros Digitais

Este projeto é um simulador desenvolvido em Python para demonstrar como filtros digitais podem ser usados para reduzir componentes indesejadas e ruídos em um sinal. A interface foi feita com Tkinter, e os gráficos mostram o sinal no tempo e sua análise de frequências por FFT.

O exemplo utiliza um sinal matemático que representa, de forma didática, um sinal associado ao monitoramento de temperatura. O programa não faz leitura de um sensor físico.

## Funcionalidades

- Geração de um sinal com uma ou duas componentes senoidais.
- Adição de ruído branco gaussiano.
- Aplicação de quatro tipos de filtro Butterworth.
- Comparação do sinal original com o sinal filtrado e com uma referência ideal.
- Visualização de quatro gráficos na interface.
- Análise das frequências antes e depois da filtragem.
- Verificação de valores inválidos e opção para limpar os dados.

A segunda componente do sinal é opcional. Para desativá-la, basta informar 0 Hz no campo Frequência 2.

## Tipos de filtro

| Filtro | O que faz | Parâmetros |
| --- | --- | --- |
| Passa-Baixa | Atenua as frequências acima do corte. | Frequência de corte |
| Passa-Alta | Atenua as frequências abaixo do corte. | Frequência de corte |
| Passa-Faixa | Mantém principalmente as frequências dentro de uma faixa. | Frequência mínima e máxima |
| Rejeita-Faixa | Atenua principalmente as frequências dentro de uma faixa. | Frequência mínima e máxima |

Os filtros não fazem uma separação perfeitamente abrupta nas frequências de corte. Existe uma região de transição, por isso algumas frequências próximas ao corte também podem ser afetadas.

## Parâmetros da interface

| Campo | Descrição | Valor inicial |
| --- | --- | --- |
| Tipo de filtro | Escolhe um dos quatro filtros. | Passa-Baixa |
| Frequência do Sinal (Hz) | Frequência da primeira componente senoidal. | 5,0 |
| Frequência 2 (Hz) | Frequência da segunda componente. Use 0 para desativá-la. | 15,0 |
| Frequência de Corte (Hz) | Usada nos filtros Passa-Baixa e Passa-Alta. | 10,0 |
| Frequência Mínima de Corte (Hz) | Limite inferior dos filtros de faixa. | 4,0 |
| Frequência Máxima de Corte (Hz) | Limite superior dos filtros de faixa. | 10,0 |
| Frequência de Amostragem (Hz) | Quantidade de amostras geradas por segundo. | 100,0 |
| Ordem do Filtro | Define a ordem do filtro. | 2 |
| Nível de Ruído | Define a intensidade do ruído adicionado. | 0,1 |

As amplitudes das duas componentes são definidas no código como 1,0 e 0,5. A duração da simulação também é fixa: 5 segundos. Esses valores não podem ser alterados pela interface.

## Gráficos

A interface apresenta quatro gráficos:

1. Sinal Antes da Filtragem: mostra o sinal original, já com ruído, e a referência do sinal desejado.
2. Sinal Depois da Filtragem: mostra o resultado do filtro e a mesma referência.
3. FFT do Sinal Original: mostra as frequências presentes antes da filtragem.
4. FFT do Sinal Filtrado: mostra as frequências presentes depois da filtragem.

Nos dois primeiros gráficos, a linha laranja representa o sinal desejado, formado pelas componentes que o filtro selecionado deveria preservar. Ela serve como referência para comparação; não é a saída do filtro nem uma medição real de um sensor.

## Como executar

### Requisitos

- Python 3.
- Tkinter, para a interface gráfica.
- NumPy, SciPy e Matplotlib.

Instale as bibliotecas necessárias pelo terminal:

```bash
python -m pip install numpy scipy matplotlib
```

No Windows, o Tkinter normalmente já vem com o Python. Em algumas distribuições Linux, pode ser necessário instalá-lo separadamente.

Salve o código em um arquivo, por exemplo, `simulador.py`. Depois, abra o terminal na pasta do arquivo e execute:

```bash
python simulador.py
```

Se o arquivo tiver outro nome, use esse nome no comando.

### Passo a passo

1. Escolha o tipo de filtro.
2. Informe as frequências do sinal e ajuste os outros parâmetros.
3. Clique em Gerar Sinal.
4. Clique em Aplicar Filtro para processar o sinal e atualizar os gráficos.
5. Compare os sinais no tempo e os gráficos de FFT.
6. Clique em Limpar para apagar os dados e restaurar os valores numéricos iniciais.

O botão Limpar restaura os valores dos campos, mas não altera a seleção do tipo de filtro. Se a frequência de amostragem for modificada depois de gerar o sinal, gere o sinal novamente antes de aplicar o filtro.

## Exemplo de uso

Com os valores iniciais, o sinal contém componentes de 5 Hz e 15 Hz, além do ruído. Ao selecionar o filtro Passa-Baixa com corte em 10 Hz, o simulador tende a preservar a componente de 5 Hz e atenuar a de 15 Hz.

Os gráficos de FFT permitem comparar o conteúdo em frequência antes e depois da filtragem. Como o ruído é gerado aleatoriamente, os resultados podem variar entre execuções.

## Como o simulador funciona

### Geração do sinal

O sinal é formado por uma ou duas ondas senoidais:

s(t) = A1 sen(2π f1 t) + A2 sen(2π f2 t)

Quando f2 é igual a 0, a segunda componente é desativada. Depois, o programa adiciona ruído ao sinal:

x(t) = s(t) + r(t)

### Amostragem

A frequência de amostragem define quantas amostras são geradas por segundo. O programa verifica se as frequências do sinal e as frequências de corte utilizadas estão abaixo da frequência de Nyquist, que corresponde à metade da frequência de amostragem.

Com uma frequência de amostragem de 100 Hz e duração de 5 segundos, são geradas 500 amostras.

### Filtragem e FFT

A função `scipy.signal.butter()` calcula os coeficientes do filtro Butterworth. A função `scipy.signal.filtfilt()` aplica o filtro nos dois sentidos, evitando o deslocamento de fase típico de uma filtragem feita apenas em um sentido.

Para analisar as frequências, o programa utiliza `numpy.fft.rfft()` e `numpy.fft.rfftfreq()`. A amplitude do espectro é calculada a partir do módulo da FFT, com a normalização usada no código.

## Tecnologias utilizadas

- Python: linguagem utilizada no projeto.
- Tkinter e ttk: criação da interface gráfica.
- NumPy: cálculos, geração dos sinais e ruído.
- SciPy: criação e aplicação dos filtros Butterworth.
- Matplotlib: construção dos gráficos.
- FFT do NumPy: análise das frequências do sinal.

## Finalidade do projeto

O simulador foi desenvolvido para fins acadêmicos e permite observar, de forma prática, como o ruído afeta um sinal e como diferentes filtros digitais modificam suas componentes de frequência. O projeto se relaciona ao processamento digital de sinais, à instrumentação e aos Sistemas Ciberfísicos.

Projeto acadêmico: Simulador de Filtros Digitais.

