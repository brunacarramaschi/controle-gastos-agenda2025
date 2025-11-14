import json
import os
from datetime import date

ARQUIVO_GASTOS = 'gastos.json'
ARQUIVO_AGENDA = 'agenda.json'

def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def menu():
    gastos = carregar_dados(ARQUIVO_GASTOS)
    agenda = carregar_dados(ARQUIVO_AGENDA)
    while True:
        print("\n" + "="*50)
        print("  CONTROLE DE GASTOS + AGENDA PESSOAL")
        print("="*50)
        print("1. Cadastrar Transação")
        print("2. Relatório de Gastos")
        print("3. Adicionar Compromisso")
        print("4. Próximos Compromissos")
        print("5. Sair")
        op = input("Opção: ").strip()
        if op == '2':
            r = sum(t["valor"] for t in gastos if t["tipo"] == "R")
            d = sum(t["valor"] for t in gastos if t["tipo"] == "D")
            print(f"\nRECEITAS: R$ {r:.2f}\nDESPESAS: R$ {d:.2f}\nSALDO: R$ {r-d:.2f}")
        elif op == '4':
            hoje = date.today().strftime("%d/%m/%Y")
            proximos = sorted([c for c in agenda if c["data"] >= hoje], key=lambda x: x["data"])[:5]
            print("\nPRÓXIMOS 5 COMPROMISSOS:")
            for c in proximos:
                print(f"{c['data']} {c['hora']} - {c['titulo']} ({c['local']})")
        elif op == '5':
            salvar_dados(ARQUIVO_GASTOS, gastos)
            salvar_dados(ARQUIVO_AGENDA, agenda)
            print("Sistema encerrado.")
            break

if __name__ == "__main__":
    menu()
        else: print("Inválido!")

if __name__ == "__main__": menu()
