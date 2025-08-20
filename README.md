# Gerador de Gráfico de Zonation

## 📊 Descrição

Este script Python gera gráficos interativos de curvas a partir de arquivos CSV, com suporte a legendas personalizadas carregadas de arquivos Excel. O projeto é especialmente útil para visualizar dados de zonation com escalas normalizadas e nomes descritivos dos alvos.

## 🚀 Funcionalidades

- **Gráficos interativos**: Criação de gráficos de linha usando Plotly
- **Carregamento de dados**: Suporte a arquivos CSV separados por espaço
- **Legendas personalizadas**: Carregamento de nomes descritivos de arquivo Excel
- **Escalas normalizadas**: Eixos X e Y configurados de 0.00 a 1.00
- **Interface gráfica**: Seleção de arquivos via janela de diálogo
- **Hover informativo**: Tooltips com nomes completos e valores
- **Tema escuro**: Interface visual moderna com template dark

## 📋 Requisitos

### Dependências Python
```bash
pip install pandas plotly openpyxl tkinter
```

### Arquivos necessários
- `main.py` - Script principal
- `legenda_alvos.xlsx` - Arquivo Excel com legendas (opcional)

## 📁 Estrutura do Projeto

```
gerar_grafico_zonation/
├── main.py              # Script principal
├── legenda_alvos.xlsx   # Arquivo de legendas (opcional)
├── grafico.html         # Gráfico gerado (opcional)
└── README.md            # Este arquivo
```

## 🔧 Como Funciona

### 1. Carregamento de Dados
- Abre uma janela de diálogo para selecionar o arquivo CSV
- Lê o arquivo CSV usando delimitador de espaço
- Carrega automaticamente o arquivo `legenda_alvos.xlsx` se disponível

### 2. Processamento de Legendas
- Busca nomes descritivos na coluna 'Alvos' do Excel
- Mapeia colunas numéricas para nomes completos
- Mantém nomes originais se não encontrar correspondência

### 3. Normalização de Escalas
- **Eixo X**: Normaliza posições de 0.00 a 1.00 (independente do número de linhas)
- **Eixo Y**: Mantém valores originais na escala de 0.00 a 1.00

### 4. Geração do Gráfico
- Cria gráfico interativo com Plotly
- Adiciona cada coluna como uma linha separada
- Configura tooltips informativos
- Aplica tema escuro e formatação profissional

## 📊 Formato dos Arquivos

### Arquivo CSV de Dados
```
0.1 0.2 0.3 0.4
0.2 0.3 0.4 0.5
0.3 0.4 0.5 0.6
...
```
- **Delimitador**: Espaço
- **Colunas**: Valores numéricos (0.00 a 1.00)
- **Linhas**: Pontos de dados

### Arquivo Excel de Legendas
| Coluna1 | Alvos |
|---------|-------|
| 0       | Nome do Alvo 1 |
| 1       | Nome do Alvo 2 |
| 2       | Nome do Alvo 3 |

- **Primeira coluna**: Números das colunas (0, 1, 2, ...)
- **Coluna 'Alvos'**: Nomes descritivos correspondentes

## 🎯 Como Usar

### Execução Básica
```bash
python main.py
```

### Passos de Uso
1. **Execute o script**: `python main.py`
2. **Selecione o CSV**: Escolha o arquivo de dados na janela de diálogo
3. **Aguarde o processamento**: O script carregará dados e legendas
4. **Visualize o gráfico**: O gráfico abrirá automaticamente no navegador

### Personalização
- **Legendas**: Coloque `legenda_alvos.xlsx` na mesma pasta
- **Escalas**: Modifique os ranges nos parâmetros `xaxis` e `yaxis`
- **Tema**: Altere `template='plotly_dark'` para outros temas

## 📈 Características do Gráfico

- **Eixo X**: Posição normalizada (0.00 a 1.00)
- **Eixo Y**: Valores dos dados (0.00 a 1.00)
- **Marcações**: Intervalos de 0.1 com 2 casas decimais
- **Interatividade**: Zoom, pan, hover e legendas clicáveis
- **Responsividade**: Adapta-se a diferentes tamanhos de tela

## 🛠️ Personalização Avançada

### Modificar Escalas
```python
xaxis=dict(
    range=[0, 1],        # Escala do eixo X
    dtick=0.1,           # Intervalo das marcações
    tickformat='.2f'     # Formato decimal
)
```

### Alterar Tema
```python
template='plotly_white'  # Tema claro
template='plotly'        # Tema padrão
template='ggplot2'       # Tema estilo R
```

### Salvar como HTML
```python
fig.write_html("meu_grafico.html")
```

## 🔍 Solução de Problemas

### Erro ao carregar Excel
- Verifique se o arquivo `legenda_alvos.xlsx` existe
- Confirme se tem a coluna 'Alvos'
- Verifique se não está corrompido

### Gráfico não abre
- Confirme se o Plotly está instalado: `pip install plotly`
- Verifique se o navegador padrão está configurado
- Tente salvar como HTML: `fig.write_html("grafico.html")`

### Dados não aparecem
- Verifique o formato do CSV (delimitador de espaço)
- Confirme se os valores estão entre 0 e 1
- Verifique se não há colunas vazias

## 📝 Exemplo de Saída

O script gera um gráfico interativo com:
- Múltiplas linhas coloridas (uma por coluna)
- Eixos normalizados de 0.00 a 1.00
- Tooltips informativos ao passar o mouse
- Legenda clicável para mostrar/ocultar linhas
- Interface responsiva e profissional

## 🤝 Contribuições

Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Adicionar novas funcionalidades
- Melhorar a documentação

## 📄 Licença

Este projeto é de uso livre para fins educacionais e profissionais.

---

**Desenvolvido para visualização de dados de zonation com escalas normalizadas e legendas personalizadas.**
