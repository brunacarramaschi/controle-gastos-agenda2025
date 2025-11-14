# Sistema Web Integrado de Controle Financeiro Pessoal e Gerenciamento de Agenda

Projeto Integrador - Laboratório de Programação\
UNISA - Universidade Santo Amaro\
Engenharia de Software - 2025

## 📋 Sobre o Projeto

Este projeto apresenta o desenvolvimento de um sistema web integrado
para controle de gastos pessoais e gerenciamento de agenda de
compromissos utilizando Python e framework Streamlit. A solução aplica
metodologias científicas de educação financeira, incluindo análise
estatística e visualizações interativas.

## 🎯 Objetivo Geral

Desenvolver sistema web integrado de controle de gastos pessoais e
gerenciamento de agenda utilizando Python e Streamlit, incorporando
análise financeira baseada na metodologia 50-30-20 (SEBRAE, 2023),
visualizações interativas com Plotly, cálculos estatísticos e geração
automatizada de relatórios PDF.

## ✨ Funcionalidades Principais

### 💰 Controle Financeiro

-   Cadastro de receitas e despesas com categorização\
-   Cálculo automático de saldo (receitas - despesas)\
-   Análise estatística descritiva (média, mediana, desvio padrão)\
-   Aplicação da metodologia 50-30-20 do SEBRAE\
-   Sistema inteligente de alertas financeiros\
-   Visualizações interativas com gráficos Plotly

### 📅 Gerenciamento de Agenda

-   Cadastro de compromissos (título, data, hora, local, descrição)\
-   Calendário visual mensal integrado\
-   Listagem de próximos compromissos\
-   Alertas de eventos próximos\
-   Exclusão de compromissos

### 📊 Análises e Relatórios

-   Gráfico de evolução temporal (receitas vs despesas)\
-   Gráfico de pizza (distribuição por categoria)\
-   Gráfico comparativo real vs ideal (metodologia 50-30-20)\
-   Geração automática de relatórios em PDF\
-   Exportação de dados em CSV

## 🛠️ Tecnologias Utilizadas

### Linguagem e Framework

-   **Python 3.11+**\
-   **Streamlit**

### Bibliotecas Principais

-   Pandas\
-   NumPy\
-   Plotly\
-   FPDF2\
-   JSON

## 📂 Estrutura de Arquivos

    .
    ├── main.py
    ├── gastos.json
    ├── agenda.json
    ├── README.md
    └── .streamlit/
        └── config.toml

## 🚀 Como Executar

### Requisitos

-   Python 3.11+

### Instalação

    git clone https://github.com/brunacarramaschi/controle-gastos-agenda2025.git
    cd controle-gastos-agenda2025
    pip install streamlit plotly pandas numpy fpdf2 reportlab pillow openpyxl

### Execução

    streamlit run main.py --server.port 5000

Abra no navegador: `http://localhost:5000`

## 📖 Metodologias Aplicadas

### 1. Metodologia 50-30-20 (SEBRAE, 2023)

-   50% Necessidades\
-   30% Desejos\
-   20% Investimentos

Implementação no sistema: função `analisar_metodo_50_30_20()`.

### 2. Análise Estatística Descritiva

-   Média\
-   Mediana\
-   Desvio padrão\
-   Coeficiente de variação

Implementação: função `calcular_estatisticas()`.

### 3. Visualização de Dados com Plotly

-   Gráfico de linhas\
-   Gráfico de pizza\
-   Gráfico de barras

### 4. Sistema Inteligente de Alertas

-   Alerta crítico: saldo negativo\
-   Atenção: saldo muito baixo\
-   Avisos: desvios do 50-30-20\
-   Confirmação: finanças equilibradas

## 📊 Exemplo de Dados

### Transação Financeira (gastos.json)

    {
      "id": 1,
      "tipo": "D",
      "valor": 1200.0,
      "categoria": "Moradia",
      "data": "05/11/2025",
      "descricao": "Aluguel mensal"
    }

### Compromisso (agenda.json)

    {
      "id": 1,
      "titulo": "Reunião de equipe",
      "data": "15/11/2025",
      "hora": "09:00",
      "local": "Escritório - Sala 3",
      "descricao": "Reunião semanal de alinhamento"
    }

## 🎓 Referências Bibliográficas

-   SEBRAE (2023). Metodologia 50-30-20 para orçamento pessoal.
-   SILVA, J. (2022). Educação Financeira e Qualidade de Vida.
-   CERBASI, G. (2020). Como Organizar sua Vida Financeira.
-   KIYOSAKI, R. (2021). Pai Rico, Pai Pobre.
-   COVEY, S. (2021). Os 7 Hábitos das Pessoas Altamente Eficazes.
-   CRESPO, A. (2019). Estatística Aplicada.
-   MCKINNEY, W. (2022). Python for Data Analysis.
-   Python Software Foundation (2023). Python Documentation.
-   Streamlit Documentation (2024).

## 👨‍💻 Autora

**Bruna Carramaschi Santos**\
RA: 4882121\
📧 bbruna2x@estudante.unisa.br\
Orientadora: **Prof. Dr. Maria Oliveira**

## 📝 Licença

Projeto desenvolvido para fins acadêmicos como Projeto Integrador UNISA.

## 🔗 Links Úteis

-   GitHub:
    https://github.com/brunacarramaschi/controle-gastos-agenda2025
-   Execução Online:
    https://replit.com/@brunaunisa/controle-gastos-agenda
-   Documentação Streamlit\
-   Documentação Plotly

## 📅 Histórico de Versões

-   **v1.0 (14/11/2025)**: Versão inicial completa.

------------------------------------------------------------------------

Desenvolvido com 💙 por **Bruna Carramaschi Santos**
