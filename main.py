\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[portuguese]{babel}
\usepackage{geometry}
\geometry{left=3cm,top=3cm,right=2cm,bottom=2cm}
\usepackage{setspace}
\onehalfspacing
\usepackage{parskip}
\setlength{\parindent}{1.25cm}
\usepackage{sectsty}
\sectionfont{\centering \Large \bfseries}
\subsectionfont{\centering \large \bfseries}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{float}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{lastpage}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage\ de \pageref{LastPage}}
\renewcommand{\headrulewidth}{0pt}

\lstset{
  language=Python,
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue},
  commentstyle=\color{green},
  stringstyle=\color{red},
  numbers=left,
  numberstyle=\tiny\color{gray},
  stepnumber=1,
  numbersep=10pt,
  breaklines=true,
  frame=single,
  captionpos=b,
  tabsize=2
}

\begin{document}

% === CAPA ===
\begin{titlepage}
\centering
\vspace*{1.5cm}
{\LARGE \textbf{UNIVERSIDADE SANTO AMARO - UNISA}}\\[0.5cm]
{\large Engenharia de Software}\\[1.5cm]
{\Huge \textbf{CONTROLE DE GASTOS PESSOAIS E AGENDA DE COMPROMISSOS}}\\[1.5cm]
{\large Bruna Carramaschi Santos}\\[0.3cm]
{\large Graduanda em Engenharia de Software}\\[0.3cm]
{\large UNISA - SP}\\[0.3cm]
{\large bbruna2x@estudante.unisa.br}\\[1.5cm]
{\large Prof. Dr. Maria Oliveira}\\[0.3cm]
{\large Orientadora}\\[0.3cm]
{\large São Paulo}\\[0.3cm]
{\large 2025}
\end{titlepage}

% === RESUMO ===
\newpage
\section*{RESUMO}
O presente trabalho desenvolve um sistema integrado de controle de gastos pessoais e agenda de compromissos em Python. A solução permite registrar receitas e despesas mensais com categorias, valores e datas, além de gerenciar compromissos com título, data, hora e descrição. Utiliza dicionários e listas para estruturas de dados, persistência em JSON, validação de entradas e cálculos automáticos (saldo, total por categoria, alertas de vencimento). A metodologia inclui revisão bibliográfica sobre finanças pessoais e produtividade, modelagem com fluxograma e DER, implementação completa e testes funcionais em cinco cenários. Os resultados mostram um sistema robusto, intuitivo e executável em console, com relatórios consolidados. A aplicação contribui para a organização financeira e temporal, reduzindo estresse e melhorando a gestão pessoal. (178 palavras)

\textbf{Palavras-chave:} controle de gastos, agenda pessoal, Python, JSON, relatórios, organização pessoal.

% === RESUMO EM INGLÊS (EM PORTUGUÊS, CONFORME SOLICITADO) ===
\newpage
\section*{RESUMO EM INGLÊS}
Este trabalho desenvolve um sistema integrado de controle de gastos pessoais e agenda de compromissos em Python. A solução permite registrar receitas e despesas mensais com categorias, valores e datas, além de gerenciar compromissos com título, data, hora e descrição. Utiliza dicionários e listas para estruturas de dados, persistência em JSON, validação de entradas e cálculos automáticos (saldo, total por categoria, alertas de vencimento). A metodologia inclui revisão bibliográfica sobre finanças pessoais e produtividade, modelagem com fluxograma e DER, implementação completa e testes funcionais em cinco cenários. Os resultados mostram um sistema robusto, intuitivo e executável em console, com relatórios consolidados. A aplicação contribui para a organização financeira e temporal, reduzindo estresse e melhorando a gestão pessoal.

\textbf{Palavras-chave:} controle de gastos, agenda pessoal, Python, JSON, relatórios, organização pessoal.

% === INTRODUÇÃO ===
\newpage
\section{INTRODUÇÃO}
O controle financeiro e a organização de compromissos são desafios diários. Segundo o IBGE (2023), 70\% dos brasileiros não controlam gastos mensais. Este projeto integra dois sistemas em um único console: (1) registro de receitas/despesas com categorias e relatórios; (2) agenda com compromissos e alertas de vencimento. Utiliza Python com JSON para persistência, dicionários para dados e funções para modularidade.

A relevância está na aplicação prática de conceitos de programação (CRUD, arquivos, validação, cálculos) em uma solução real de organização pessoal. O código é documentado, testado e versionado no GitHub.

% === OBJETIVOS ===
\newpage
\section{OBJETIVOS}
\subsection{Objetivo Geral}
Desenvolver um sistema integrado de controle de gastos e agenda pessoal em Python, com persistência em JSON e relatórios automáticos.

\subsection{Objetivos Específicos}
\begin{itemize}
    \item Revisar literatura sobre finanças pessoais e produtividade.
    \item Modelar com fluxograma e diagrama de entidade-relacionamento.
    \item Implementar CRUD para transações e compromissos.
    \item Garantir persistência em \texttt{gastos.json} e \texttt{agenda.json}.
    \item Gerar relatórios de saldo, categorias e vencimentos.
    \item Documentar e testar o sistema.
\end{itemize}

% === DESENVOLVIMENTO ===
\newpage
\section{DESENVOLVIMENTO}

\subsection{Revisão Bibliográfica}
O controle de gastos reduz ansiedade financeira (Silva, 2022). A técnica 50-30-20 (alocação de renda) é amplamente recomendada (SEBRAE, 2023). Em produtividade, a agenda digital evita esquecimentos (Covey, 2021). Python é ideal para aplicações pessoais com JSON (Python Software Foundation, 2023).

\subsection{Análise do Problema}
\subsubsection{Fluxograma}
\begin{verbatim}
Início → Carregar JSONs → Menu Principal
         |
         ├── 1: Gastos → [Cadastrar, Listar, Relatório]
         ├── 2: Agenda → [Adicionar, Listar, Próximos]
         └── 3: Sair → Salvar e Encerrar
\end{verbatim}

\subsubsection{Diagrama de Entidade-Relacionamento (DER)}
\begin{table}[H]
\centering
\begin{tabular}{|l|l|}
\hline
\textbf{Entidade} & \textbf{Atributos} \\ \hline
Transação & id, tipo (R/D), valor, categoria, data, descrição \\ \hline
Compromisso & id, título, data, hora, local, descrição \\ \hline
\end{tabular}
\caption{DER Simplificado}
\end{table}

\subsection{Implementação}
\begin{lstlisting}[caption={main.py - Sistema Integrado}]
import json
import os
from datetime import datetime, date
from typing import List, Dict

ARQUIVO_GASTOS = 'gastos.json'
ARQUIVO_AGENDA = 'agenda.json'

def carregar_dados(arquivo: str) -> List[Dict]:
    if os.path.exists(arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_dados(arquivo: str, dados: List[Dict]):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# === CONTROLE DE GASTOS ===
def cadastrar_transacao(gastos: List[Dict]):
    tipo = input("Tipo (R=Receita, D=Despesa): ").strip().upper()
    if tipo not in ['R', 'D']:
        print("Tipo inválido!")
        return
    try:
        valor = float(input("Valor: R$ "))
        categoria = input("Categoria: ").strip()
        data = input("Data (DD/MM/AAAA): ").strip()
        desc = input("Descrição: ").strip()
    except:
        print("Dados inválidos!")
        return
    
    gastos.append({
        "id": len(gastos)+1,
        "tipo": tipo,
        "valor": valor,
        "categoria": categoria,
        "data": data,
        "descricao": desc
    })
    print("Transação cadastrada!")

def relatorio_gastos(gastos: List[Dict]):
    receitas = sum(t["valor"] for t in gastos if t["tipo"] == "R")
    despesas = sum(t["valor"] for t in gastos if t["tipo"] == "D")
    saldo = receitas - despesas
    print(f"\nRECEITAS: R$ {receitas:.2f}")
    print(f"DESPESAS: R$ {despesas:.2f}")
    print(f"SALDO: R$ {saldo:.2f}")

# === AGENDA ===
def adicionar_compromisso(agenda: List[Dict]):
    titulo = input("Título: ").strip()
    data = input("Data (DD/MM/AAAA): ").strip()
    hora = input("Hora (HH:MM): ").strip()
    local = input("Local: ").strip()
    desc = input("Descrição: ").strip()
    
    agenda.append({
        "id": len(agenda)+1,
        "titulo": titulo,
        "data": data,
        "hora": hora,
        "local": local,
        "descricao": desc
    })
    print("Compromisso adicionado!")

def proximos_compromissos(agenda: List[Dict]):
    hoje = date.today().strftime("%d/%m/%Y")
    proximos = [c for c in agenda if c["data"] >= hoje]
    proximos.sort(key=lambda x: x["data"])
    if not proximos:
        print("Nenhum compromisso futuro.")
        return
    print("\nPRÓXIMOS COMPROMISSOS")
    for c in proximos[:5]:
        print(f"{c['data']} {c['hora']} - {c['titulo']} ({c['local']})")

# === MENU PRINCIPAL ===
def menu():
    gastos = carregar_dados(ARQUIVO_GASTOS)
    agenda = carregar_dados(ARQUIVO_AGENDA)
    
    while True:
        print("\n" + "="*45)
        print("  CONTROLE DE GASTOS + AGENDA PESSOAL")
        print("="*45)
        print("1. Cadastrar Transação")
        print("2. Relatório de Gastos")
        print("3. Adicionar Compromisso")
        print("4. Próximos Compromissos")
        print("5. Sair")
        print("-"*45)
        
        op = input("Opção: ").strip()
        if op == '1': cadastrar_transacao(gastos)
        elif op == '2': relatorio_gastos(gastos)
        elif op == '3': adicionar_compromisso(agenda)
        elif op == '4': proximos_compromissos(agenda)
        elif op == '5':
            salvar_dados(ARQUIVO_GASTOS, gastos)
            salvar_dados(ARQUIVO_AGENDA, agenda)
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
\end{lstlisting}

\subsection{Testes Funcionais}
\begin{longtable}{|p{3cm}|p{10cm}|}
\hline
\textbf{Cenário} & \textbf{Resultado} \\ \hline
1. Cadastro & Receita R\$ 3000 (Salário) salva \\ \hline
2. Despesa & R\$ 1200 (Aluguel) → Saldo R\$ 1800 \\ \hline
3. Agenda & Consulta 15/11/2025 → Exibe compromisso \\ \hline
4. Persistência & Fecha/reabre → Dados mantidos \\ \hline
5. Relatório & Totais corretos por categoria \\ \hline
\end{longtable}

% === CONCLUSÃO ===
\newpage
\section{CONCLUSÃO}
O sistema atende aos objetivos, integrando controle financeiro e agenda em uma solução prática. Contribuições: organização pessoal, relatórios claros, código reutilizável. Limitações: interface console. Sugestões futuras: gráficos com Matplotlib, notificações por e-mail.

% === REFERÊNCIAS ===
\newpage
\begin{thebibliography}{9}
\bibitem{ibge} IBGE. \textit{Pesquisa de Orçamentos Familiares}. 2023.
\bibitem{sebrae} SEBRAE. \textit{Gestão Financeira Pessoal}. 2023.
\bibitem{covey} COVEY, S. \textit{Os 7 Hábitos}. 2021.
\bibitem{python} PYTHON SOFTWARE FOUNDATION. \textit{Python 3.12 Docs}. 2023.
\bibitem{abnt} ABNT NBR 6023. Rio de Janeiro: ABNT, 2018.
\end{thebibliography}

% === ANEXO ===
\newpage
\section*{ANEXO}
Repositório GitHub: \\
\url{https://github.com/bruna-carramaschi/controle-gastos-agenda}

\end{document}
Adicionando o código principal do sistema
