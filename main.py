import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import tkinter as tk
from tkinter import filedialog


# Abrir janela para escolher o arquivo CSV
root = tk.Tk()
root.withdraw()  # Esconde a janela principal do Tkinter
arquivo_csv = filedialog.askopenfilename(
    title="Selecione o arquivo CSV",
    filetypes=[("CSV files", "*.csv"), ("Todos os arquivos", "*.*")]
)

# Ler o arquivo CSV (separado por espaço)
df = pd.read_csv(arquivo_csv, delimiter=' ')

# Carregar o arquivo Excel com a legenda dos alvos
try:
    df_legenda = pd.read_excel('legenda_alvos.xlsx')
    print("✅ Arquivo legenda_alvos.xlsx carregado com sucesso!")
    print("Colunas disponíveis:", df_legenda.columns.tolist())
except Exception as e:
    print(f"❌ Erro ao carregar legenda_alvos.xlsx: {e}")
    df_legenda = None

# Remover coluna 'rank' se existir
if 'rank' in df.columns:
    df.drop(columns=['rank'], inplace=True)

# Criar gráfico interativo
fig = go.Figure()

# Normalizar o eixo X para ir de 0 a 1
x_normalizado = [i / (len(df) - 1) if len(df) > 1 else 0 for i in range(len(df))]

# Adicionar cada série de dados ao gráfico com dica de ferramenta personalizada
for coluna in df.columns:
    nome_completo = coluna
    
    # Buscar o nome completo na legenda se disponível
    if df_legenda is not None and 'Alvos' in df_legenda.columns:
        try:
            # Assumindo que a primeira coluna do Excel contém os números das colunas
            coluna_id = df_legenda.columns[0]
            coluna_int = int(coluna)
            
            # Verificar se o índice existe na legenda
            if coluna_int < len(df_legenda):
                nome_completo = df_legenda['Alvos'][coluna_int]
                print(f'Coluna {coluna} -> Nome completo: {nome_completo}')
        except (ValueError, IndexError):
            # Se não conseguir converter ou não encontrar, mantém o nome original
            pass
    
    # Se o nome for muito longo, truncar para exibição
    if len(nome_completo) > 50:
        nome_exibicao = nome_completo[:50] + "..."
    else:
        nome_exibicao = nome_completo
        
    fig.add_trace(go.Scatter(
        x=x_normalizado,  # Usar eixo X normalizado de 0 a 1
        y=df[coluna], 
        mode='lines', 
        name=nome_exibicao,  # Nome truncado para a legenda
        hovertemplate=f'{nome_completo}<br>Posição: %{{x:.2f}}<br>Valor: %{{y:.2f}}<extra></extra>'  # Nome completo no hover
    ))

# exit()

fig.update_layout(
    title='Gráfico de Curva Interativo',
    xaxis_title='Posição Normalizada',
    yaxis_title='Valor',
    template='plotly_dark',
    xaxis=dict(
        range=[0, 1],  # Define a escala do eixo X de 0 a 1
        tickmode='linear',
        dtick=0.1,  # Intervalo de 0.1 entre as marcações
        tickformat='.2f'  # Formato com 2 casas decimais
    ),
    yaxis=dict(
        range=[0, 1],  # Define a escala do eixo Y de 0 a 1
        tickmode='linear',
        dtick=0.1,  # Intervalo de 0.1 entre as marcações
        tickformat='.2f'  # Formato com 2 casas decimais
    )
)
# Configurar para abrir no navegador
pio.renderers.default = "browser"
fig.show()
# Salvar como HTML interativo
# fig.write_html("grafico.html")
#
# print("✅ Arquivo 'grafico.html' gerado com sucesso!")
