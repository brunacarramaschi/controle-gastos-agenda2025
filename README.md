# Sistema Web Integrado de Controle Financeiro Pessoal e Gerenciamento de Agenda

**Projeto Integrador - Laboratório de Programação**  
**UNISA - Universidade Santo Amaro**  
**Engenharia de Software - 2025**

---

## 📋 Sobre o Projeto

Este projeto apresenta o desenvolvimento de um sistema web integrado para controle de gastos pessoais e gerenciamento de agenda de compromissos utilizando Python e framework Streamlit. A solução aplica metodologias científicas de educação financeira, incluindo análise estatística e visualizações interativas.

### 🎯 Objetivo Geral

Desenvolver sistema web integrado de controle de gastos pessoais e gerenciamento de agenda utilizando Python e Streamlit, incorporando análise financeira baseada na **metodologia 50-30-20** (SEBRAE, 2023), visualizações interativas com Plotly, cálculos estatísticos e geração automatizada de relatórios PDF.

---

## ✨ Funcionalidades Principais

### 💰 Controle Financeiro
- ✅ Cadastro de receitas e despesas com categorização
- ✅ Cálculo automático de saldo (receitas - despesas)
- ✅ Análise estatística descritiva (média, mediana, desvio padrão)
- ✅ Aplicação da metodologia 50-30-20 do SEBRAE
- ✅ Sistema inteligente de alertas financeiros
- ✅ Visualizações interativas com gráficos Plotly

### 📅 Gerenciamento de Agenda
- ✅ Cadastro de compromissos (título, data, hora, local, descrição)
- ✅ Calendário visual mensal integrado
- ✅ Listagem de próximos compromissos
- ✅ Alertas de eventos próximos
- ✅ Exclusão de compromissos

### 📊 Análises e Relatórios
- ✅ Gráfico de evolução temporal (receitas vs despesas)
- ✅ Gráfico de pizza (distribuição por categoria)
- ✅ Gráfico comparativo real vs ideal (metodologia 50-30-20)
- ✅ Geração automática de relatórios em PDF
- ✅ Exportação de dados em CSV

---

## 🛠️ Tecnologias Utilizadas

### Linguagem e Framework
- **Python 3.11+**: Linguagem principal
- **Streamlit**: Framework para desenvolvimento web

### Bibliotecas Principais
- **Pandas**: Manipulação e análise de dados tabulares
- **NumPy**: Cálculos estatísticos e numéricos
- **Plotly**: Visualizações interativas de dados
- **FPDF2**: Geração de relatórios PDF
- **JSON**: Persistência de dados

---

## 📂 Estrutura de Arquivos

```
.
├── main.py           # Código principal do sistema
├── gastos.json       # Dados de transações financeiras
├── agenda.json       # Dados de compromissos
├── README.md         # Documentação do projeto
└── .streamlit/
    └── config.toml   # Configurações do Streamlit
```

---

## 🚀 Como Executar

### Requisitos do Sistema
- Python 3.11 ou superior
- Bibliotecas listadas em `pyproject.toml`

### Instalação

1. **Clone o repositório** (se aplicável):
```bash
git clone https://github.com/brunacarramaschi/controle-gastos-agenda2025.git
cd controle-gastos-agenda2025
```

2. **Instale as dependências**:
```bash
pip install streamlit plotly pandas numpy fpdf2 reportlab pillow openpyxl
```

### Execução

Execute o sistema com o seguinte comando:

```bash
streamlit run main.py --server.port 5000
```

O sistema será aberto automaticamente no navegador em `http://localhost:5000`

---

## 📖 Metodologias Aplicadas

### 1. Metodologia 50-30-20 (SEBRAE, 2023)

Técnica de orçamento pessoal que estabelece distribuição percentual das despesas mensais:

- **50% Necessidades**: Despesas essenciais (moradia, alimentação, transporte, saúde, educação)
- **30% Desejos**: Gastos não essenciais (lazer, entretenimento, vestuário)
- **20% Investimentos**: Poupança, aplicações financeiras, reserva de emergência

**Implementação no Sistema**: Função `analisar_metodo_50_30_20()` classifica despesas automaticamente e gera visualização comparativa entre distribuição real e ideal.

### 2. Análise Estatística Descritiva

Aplicação de conceitos fundamentais de estatística:

- **Média Aritmética**: Valor típico das despesas
- **Mediana**: Ponto central (Q2) resistente a outliers
- **Desvio Padrão**: Quantificação da variabilidade dos gastos
- **Coeficiente de Variação**: Dispersão relativa

**Implementação no Sistema**: Função `calcular_estatisticas()` utiliza NumPy para cálculos precisos.

### 3. Visualização de Dados com Plotly

Gráficos interativos para compreensão visual facilitada:

- **Gráfico de Linhas**: Evolução temporal de receitas e despesas
- **Gráfico de Pizza**: Distribuição percentual por categoria
- **Gráfico de Barras**: Comparação real vs ideal (50-30-20)

**Implementação no Sistema**: Funções dedicadas para cada tipo de visualização utilizando biblioteca Plotly.

### 4. Sistema Inteligente de Alertas

Análise automatizada de indicadores de saúde financeira:

- ⚠️ **Alerta Crítico**: Saldo negativo
- ⚡ **Atenção**: Saldo muito baixo (<10% da receita)
- 📊 **Avisos**: Desvios da metodologia 50-30-20
- ✅ **Confirmação**: Finanças equilibradas

**Implementação no Sistema**: Função `gerar_alertas_financeiros()` com recomendações fundamentadas em literatura científica.

---

## 📊 Exemplo de Dados

### Transação Financeira (gastos.json)
```json
{
  "id": 1,
  "tipo": "D",
  "valor": 1200.0,
  "categoria": "Moradia",
  "data": "05/11/2025",
  "descricao": "Aluguel mensal"
}
```

### Compromisso (agenda.json)
```json
{
  "id": 1,
  "titulo": "Reunião de equipe",
  "data": "15/11/2025",
  "hora": "09:00",
  "local": "Escritório - Sala 3",
  "descricao": "Reunião semanal de alinhamento"
}
```

---

## 🎓 Referências Bibliográficas

1. **SEBRAE** (2023). Metodologia 50-30-20 para orçamento pessoal. Serviço Brasileiro de Apoio às Micro e Pequenas Empresas.

2. **SILVA, J.** (2022). Educação Financeira e Qualidade de Vida. Editora Financeira.

3. **CERBASI, G.** (2020). Como Organizar sua Vida Financeira. Editora Sextante.

4. **KIYOSAKI, R.** (2021). Pai Rico, Pai Pobre. Editora Alta Books.

5. **COVEY, S.** (2021). Os 7 Hábitos das Pessoas Altamente Eficazes. Editora Best Seller.

6. **CRESPO, A.** (2019). Estatística Aplicada. Editora Saraiva.

7. **MCKINNEY, W.** (2022). Python for Data Analysis. O'Reilly Media.

8. **Python Software Foundation** (2023). Python Documentation. Disponível em: https://docs.python.org

9. **Streamlit Documentation** (2024). Streamlit Docs. Disponível em: https://docs.streamlit.io

---

## 👨‍💻 Autora

**Bruna Carramaschi Santos**  
Graduanda em Engenharia de Software  
UNISA - Universidade Santo Amaro  
RA: 4882121  
📧 bbruna2x@estudante.unisa.br

**Orientadora**: Prof. Dr. Maria Oliveira

---

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos como Projeto Integrador do curso de Engenharia de Software da UNISA.

---

## 🔗 Links Úteis

- **Aplicação (Deployment)**: https://sistema-de-controle-financeiro-2025-brunacarramasc1.replit.app
- **Repositório GitHub**: https://github.com/brunacarramaschi/controle-gastos-agenda2025
- **Documentação Streamlit**: https://docs.streamlit.io
- **Documentação Plotly**: https://plotly.com/python/

---

## 📅 Histórico de Versões

- **v1.0** (14/11/2025): Versão inicial completa
  - Sistema web com Streamlit
  - Metodologia 50-30-20 implementada
  - Análises estatísticas
  - Visualizações interativas
  - Geração de PDF
  - Calendário visual

---

## 🙏 Agradecimentos

Agradecimentos especiais à Prof. Dr. Maria Oliveira pela orientação e aos colegas do curso de Engenharia de Software da UNISA pelo suporte e colaboração durante o desenvolvimento deste projeto.

---

**Desenvolvido com 💙 por Bruna Carramaschi Santos**  
**UNISA - Engenharia de Software - 2025**
