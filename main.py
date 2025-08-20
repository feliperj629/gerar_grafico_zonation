import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime


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
    
    # Verificar se existe coluna de grupos
    tem_grupos = 'Grupo' in df_legenda.columns
    if tem_grupos:
        grupos_disponiveis = df_legenda['Grupo'].unique()
        print(f"Grupos disponíveis: {list(grupos_disponiveis)}")
        
        # Interface para seleção de grupo
        print("\n=== SELEÇÃO DE GRUPO ===")
        print("0. Todos os grupos")
        for i, grupo in enumerate(grupos_disponiveis, 1):
            print(f"{i}. {grupo}")
        
        try:
            escolha = input(f"\nEscolha um grupo (0-{len(grupos_disponiveis)}) ou pressione Enter para todos: ").strip()
            if escolha and escolha.isdigit():
                idx = int(escolha)
                if idx == 0:
                    grupo_selecionado = None
                    print("✅ Gerando gráfico com todos os grupos")
                elif 1 <= idx <= len(grupos_disponiveis):
                    grupo_selecionado = grupos_disponiveis[idx - 1]
                    print(f"✅ Grupo selecionado: {grupo_selecionado}")
                else:
                    grupo_selecionado = None
                    print("❌ Opção inválida. Gerando com todos os grupos.")
            else:
                grupo_selecionado = None
                print("✅ Gerando gráfico com todos os grupos")
        except:
            grupo_selecionado = None
            print("✅ Gerando gráfico com todos os grupos")
    else:
        grupo_selecionado = None
        print("ℹ️ Nenhuma coluna 'Grupo' encontrada. Gerando com todos os dados.")
        
except Exception as e:
    print(f"❌ Erro ao carregar legenda_alvos.xlsx: {e}")
    df_legenda = None
    grupo_selecionado = None

# Remover coluna 'rank' se existir
if 'rank' in df.columns:
    df.drop(columns=['rank'], inplace=True)

# Criar gráfico interativo
fig = go.Figure()

# Normalizar o eixo X para ir de 0 a 1
x_normalizado = [i / (len(df) - 1) if len(df) > 1 else 0 for i in range(len(df))]

# Adicionar cada série de dados ao gráfico com dica de ferramenta personalizada
colunas_processadas = 0
for coluna in df.columns:
    nome_completo = coluna
    grupo_coluna = None
    
    # Buscar o nome completo e grupo na legenda se disponível
    if df_legenda is not None and 'Alvos' in df_legenda.columns:
        try:
            # Assumindo que a primeira coluna do Excel contém os números das colunas
            coluna_id = df_legenda.columns[0]
            coluna_int = int(coluna)
            
            # Verificar se o índice existe na legenda
            if coluna_int < len(df_legenda):
                nome_completo = df_legenda['Alvos'][coluna_int]
                # Verificar se tem coluna de grupo
                if 'Grupo' in df_legenda.columns:
                    grupo_coluna = df_legenda['Grupo'][coluna_int]
                
                print(f'Coluna {coluna} -> Nome completo: {nome_completo} | Grupo: {grupo_coluna}')
        except (ValueError, IndexError):
            # Se não conseguir converter ou não encontrar, mantém o nome original
            pass
    
    # Filtrar por grupo se um grupo específico foi selecionado
    if grupo_selecionado is not None:
        if grupo_coluna != grupo_selecionado:
            continue  # Pular colunas que não pertencem ao grupo selecionado
    
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
    colunas_processadas += 1

print(f"\n📊 Total de colunas processadas: {colunas_processadas}")
if grupo_selecionado:
    print(f"🎯 Filtrado apenas para o grupo: {grupo_selecionado}")
else:
    print("🌍 Incluindo todos os grupos disponíveis")

# exit()

fig.update_layout(
    title='Gráfico de Curva Interativo',
    xaxis_title='Valor X',
    yaxis_title='Valor Y',
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

# Criar pasta outputs se não existir
pasta_outputs = "outputs"
if not os.path.exists(pasta_outputs):
    os.makedirs(pasta_outputs)
    print(f"✅ Pasta '{pasta_outputs}' criada com sucesso!")

# Gerar nome do arquivo com data e hora
data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")

# Obter o nome base do arquivo CSV (sem extensão)
nome_base_csv = os.path.splitext(os.path.basename(arquivo_csv))[0]

if grupo_selecionado:
    # Incluir nome do grupo no nome do arquivo
    nome_grupo_limpo = grupo_selecionado.replace(" ", "_").replace("/", "_").replace("\\", "_")
    nome_arquivo = f"{nome_grupo_limpo}_{nome_base_csv}_{data_hora}.html"
else:
    nome_arquivo = f"{nome_base_csv}_{data_hora}.html"

caminho_completo = os.path.join(pasta_outputs, nome_arquivo)

# Salvar como HTML interativo
fig.write_html(caminho_completo)
print(f"✅ Arquivo '{nome_arquivo}' salvo em '{pasta_outputs}/' com sucesso!")
print(f"📁 Caminho completo: {caminho_completo}")
