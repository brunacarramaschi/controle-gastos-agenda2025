import json, os
from datetime import date
from typing import List, Dict

ARQUIVO_GASTOS = 'gastos.json'
ARQUIVO_AGENDA = 'agenda.json'

def carregar_dados(arquivo: str) -> List[Dict]:
    if os.path.exists(arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

def salvar_dados(arquivo: str, dados: List[Dict]):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def cadastrar_transacao(gastos: List[Dict]):
    tipo = input("Tipo (R/D): ").strip().upper()
    if tipo not in ['R', 'D']: print("Inválido!"); return
    try: valor = float(input("Valor: "))
    except: print("Inválido!"); return
    categoria = input("Categoria: ")
    data = input("Data (DD/MM/AAAA): ")
    desc = input("Descrição: ")
    gastos.append({"id": len(gastos)+1, "tipo": tipo, "valor": valor, "categoria": categoria, "data": data, "descricao": desc})
    salvar_dados(ARQUIVO_GASTOS, gastos)
    print("Cadastrado!")

def relatorio_gastos(gastos: List[Dict]):
    r = sum(t["valor"] for t in gastos if t["tipo"] == "R")
    d = sum(t["valor"] for t in gastos if t["tipo"] == "D")
    print(f"RECEITAS: R$ {r:.2f}\nDESPESAS: R$ {d:.2f}\nSALDO: R$ {r-d:.2f}")

def adicionar_compromisso(agenda: List[Dict]):
    titulo = input("Título: ")
    data = input("Data: ")
    hora = input("Hora: ")
    local = input("Local: ")
    desc = input("Descrição: ")
    agenda.append({"id": len(agenda)+1, "titulo": titulo, "data": data, "hora": hora, "local": local, "descricao": desc})
    salvar_dados(ARQUIVO_AGENDA, agenda)
    print("Adicionado!")

def proximos_compromissos(agenda: List[Dict]):
    hoje = date.today().strftime("%d/%m/%Y")
    proximos = sorted([c for c in agenda if c["data"] >= hoje], key=lambda x: x["data"])[:5]
    if not proximos: print("Nenhum futuro."); return
    print("\nPRÓXIMOS:")
    for c in proximos: print(f"{c['data']} {c['hora']} - {c['titulo']} ({c['local']})")

def menu():
    gastos = carregar_dados(ARQUIVO_GASTOS)
    agenda = carregar_dados(ARQUIVO_AGENDA)
    while True:
        print("\n" + "="*45)
        print("  CONTROLE DE GASTOS + AGENDA")
        print("="*45)
        print("1. Transação  2. Relatório  3. Compromisso  4. Próximos  5. Sair")
        op = input("Opção: ")
        if op == '1': cadastrar_transacao(gastos)
        elif op == '2': relatorio_gastos(gastos)
        elif op == '3': adicionar_compromisso(agenda)
        elif op == '4': proximos_compromissos(agenda)
        elif op == '5': salvar_dados(ARQUIVO_GASTOS, gastos); salvar_dados(ARQUIVO_AGENDA, agenda); break
        else: print("Inválido!")

if __name__ == "__main__": menu()
