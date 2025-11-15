import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import calendar as cal
from fpdf import FPDF
import os
from streamlit.web.server import Server
from streamlit.runtime.scriptrunner import get_script_run_ctx

from database import init_db
from db_operations import (
    get_transactions_for_user, add_transaction, delete_transaction,
    get_appointments_for_user, add_appointment, delete_appointment,
    get_goals_for_user, add_goal, update_goal_progress, delete_goal
)

st.set_page_config(
    page_title="Sistema de Controle Financeiro e Agenda",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# Sem autenticação para versão JSON
current_user = None

def calcular_estatisticas(gastos):
    if not gastos:
        return {
            'total_receitas': 0,
            'total_despesas': 0,
            'saldo': 0,
            'media_despesas': 0,
            'mediana_despesas': 0,
            'desvio_padrao': 0,
            'max_despesa': 0,
            'min_despesa': 0
        }
    
    receitas = [g['valor'] for g in gastos if g['tipo'] == 'R']
    despesas = [g['valor'] for g in gastos if g['tipo'] == 'D']
    
    total_receitas = sum(receitas) if receitas else 0
    total_despesas = sum(despesas) if despesas else 0
    
    if despesas:
        media = np.mean(despesas)
        mediana = np.median(despesas)
        desvio = np.std(despesas)
        max_desp = max(despesas)
        min_desp = min(despesas)
    else:
        media = mediana = desvio = max_desp = min_desp = 0
    
    return {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': total_receitas - total_despesas,
        'media_despesas': media,
        'mediana_despesas': mediana,
        'desvio_padrao': desvio,
        'max_despesa': max_desp,
        'min_despesa': min_desp
    }

def analisar_metodo_50_30_20(gastos):
    despesas = [g for g in gastos if g['tipo'] == 'D']
    
    if not despesas:
        return {
            'necessidades': 0,
            'desejos': 0,
            'investimentos': 0,
            'total': 0,
            'perc_necessidades': 0,
            'perc_desejos': 0,
            'perc_investimentos': 0
        }
    
    categorias_necessidades = ['Moradia', 'Alimentação', 'Transporte', 'Saúde', 'Educação']
    categorias_desejos = ['Lazer', 'Vestuário', 'Entretenimento', 'Restaurantes']
    categorias_investimentos = ['Investimentos', 'Poupança', 'Previdência']
    
    necessidades = sum([d['valor'] for d in despesas if d['categoria'] in categorias_necessidades])
    desejos = sum([d['valor'] for d in despesas if d['categoria'] in categorias_desejos])
    investimentos = sum([d['valor'] for d in despesas if d['categoria'] in categorias_investimentos])
    outros = sum([d['valor'] for d in despesas if d['categoria'] not in categorias_necessidades + categorias_desejos + categorias_investimentos])
    
    total = necessidades + desejos + investimentos + outros
    
    if total > 0:
        perc_nec = (necessidades / total) * 100
        perc_des = (desejos / total) * 100
        perc_inv = (investimentos / total) * 100
    else:
        perc_nec = perc_des = perc_inv = 0
    
    return {
        'necessidades': necessidades,
        'desejos': desejos,
        'investimentos': investimentos,
        'total': total,
        'perc_necessidades': perc_nec,
        'perc_desejos': perc_des,
        'perc_investimentos': perc_inv
    }

def gerar_alertas_financeiros(stats, analise):
    alertas = []
    
    if stats['saldo'] < 0:
        alertas.append({
            'tipo': 'danger',
            'mensagem': '⚠️ ALERTA CRÍTICO: Saldo negativo! Suas despesas estão superando suas receitas.',
            'recomendacao': 'Revise urgentemente seus gastos e identifique onde pode economizar (Silva, 2022).'
        })
    elif stats['saldo'] < stats['total_receitas'] * 0.1:
        alertas.append({
            'tipo': 'warning',
            'mensagem': '⚡ ATENÇÃO: Saldo muito baixo! Menos de 10% da receita está sendo poupado.',
            'recomendacao': 'Tente aumentar suas reservas seguindo a metodologia 50-30-20 (SEBRAE, 2023).'
        })
    
    if analise['perc_necessidades'] > 60:
        alertas.append({
            'tipo': 'warning',
            'mensagem': f"📊 Necessidades representam {analise['perc_necessidades']:.1f}% dos gastos (ideal: 50%).",
            'recomendacao': 'Busque alternativas mais econômicas para despesas essenciais.'
        })
    
    if analise['perc_desejos'] > 40:
        alertas.append({
            'tipo': 'warning',
            'mensagem': f"🛍️ Desejos representam {analise['perc_desejos']:.1f}% dos gastos (ideal: 30%).",
            'recomendacao': 'Reduza gastos supérfluos para melhorar equilíbrio financeiro (Cerbasi, 2020).'
        })
    
    if analise['perc_investimentos'] < 15:
        alertas.append({
            'tipo': 'info',
            'mensagem': f"💡 Investimentos representam apenas {analise['perc_investimentos']:.1f}% (ideal: 20%).",
            'recomendacao': 'Aumente gradualmente o percentual destinado a investimentos e poupança.'
        })
    
    if stats['desvio_padrao'] > stats['media_despesas'] * 0.5:
        alertas.append({
            'tipo': 'info',
            'mensagem': '📈 Alta variabilidade nos gastos detectada.',
            'recomendacao': 'Busque maior consistência nas despesas mensais para melhor planejamento.'
        })
    
    if not alertas:
        alertas.append({
            'tipo': 'success',
            'mensagem': '✅ Excelente! Suas finanças estão equilibradas!',
            'recomendacao': 'Continue mantendo o controle e aplicando boas práticas de educação financeira.'
        })
    
    return alertas

def criar_grafico_evolucao(gastos):
    if not gastos:
        return None
    
    df = pd.DataFrame(gastos)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df = df.sort_values('data')
    
    receitas_acum = []
    despesas_acum = []
    saldo_acum = []
    datas = []
    
    rec_total = 0
    desp_total = 0
    
    for _, row in df.iterrows():
        if row['tipo'] == 'R':
            rec_total += row['valor']
        else:
            desp_total += row['valor']
        
        receitas_acum.append(rec_total)
        despesas_acum.append(desp_total)
        saldo_acum.append(rec_total - desp_total)
        datas.append(row['data'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=datas, y=receitas_acum,
        mode='lines+markers',
        name='Receitas Acumuladas',
        line=dict(color='green', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=datas, y=despesas_acum,
        mode='lines+markers',
        name='Despesas Acumuladas',
        line=dict(color='red', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=datas, y=saldo_acum,
        mode='lines+markers',
        name='Saldo',
        line=dict(color='blue', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Evolução Financeira ao Longo do Tempo',
        xaxis_title='Data',
        yaxis_title='Valor (R$)',
        hovermode='x unified',
        height=400
    )
    
    return fig

def criar_grafico_pizza_categorias(gastos):
    despesas = [g for g in gastos if g['tipo'] == 'D']
    
    if not despesas:
        return None
    
    df = pd.DataFrame(despesas)
    por_categoria = df.groupby('categoria')['valor'].sum().reset_index()
    
    fig = px.pie(
        por_categoria,
        values='valor',
        names='categoria',
        title='Distribuição de Despesas por Categoria',
        hole=0.3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig

def criar_grafico_comparativo_50_30_20(analise):
    if analise['total'] == 0:
        return None
    
    categorias = ['Necessidades', 'Desejos', 'Investimentos']
    real = [analise['perc_necessidades'], analise['perc_desejos'], analise['perc_investimentos']]
    ideal = [50, 30, 20]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Real',
        x=categorias,
        y=real,
        marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']
    ))
    
    fig.add_trace(go.Bar(
        name='Ideal (50-30-20)',
        x=categorias,
        y=ideal,
        marker_color=['#95E1D3', '#95E1D3', '#95E1D3']
    ))
    
    fig.update_layout(
        title='Metodologia 50-30-20: Real vs Ideal',
        yaxis_title='Percentual (%)',
        barmode='group',
        height=400
    )
    
    return fig

def criar_calendario_visual(agenda):
    hoje = datetime.now()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    cal_mes = cal.monthcalendar(ano_atual, mes_atual)
    
    compromissos_dict = {}
    for comp in agenda:
        try:
            data_comp = datetime.strptime(comp['data'], '%d/%m/%Y')
            dia = data_comp.day
            if data_comp.month == mes_atual and data_comp.year == ano_atual:
                if dia not in compromissos_dict:
                    compromissos_dict[dia] = []
                compromissos_dict[dia].append(comp['titulo'])
        except:
            continue
    
    st.write(f"### 📅 Calendário - {cal.month_name[mes_atual]} {ano_atual}")
    
    cols = st.columns(7)
    dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    
    for i, dia in enumerate(dias_semana):
        cols[i].markdown(f"**{dia}**")
    
    for semana in cal_mes:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].write("")
            else:
                if dia in compromissos_dict:
                    num_comp = len(compromissos_dict[dia])
                    cols[i].markdown(f"**{dia}** 🔴 ({num_comp})")
                elif dia == hoje.day:
                    cols[i].markdown(f"**{dia}** 📍")
                else:
                    cols[i].write(str(dia))

def gerar_pdf_relatorio(gastos, agenda, stats, analise):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    pdf.cell(0, 10, 'RELATÓRIO FINANCEIRO E AGENDA', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'RESUMO FINANCEIRO', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    pdf.cell(0, 8, f'Total de Receitas: R$ {stats["total_receitas"]:.2f}', 0, 1)
    pdf.cell(0, 8, f'Total de Despesas: R$ {stats["total_despesas"]:.2f}', 0, 1)
    pdf.cell(0, 8, f'Saldo: R$ {stats["saldo"]:.2f}', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'ANÁLISE ESTATÍSTICA', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    pdf.cell(0, 8, f'Media de Despesas: R$ {stats["media_despesas"]:.2f}', 0, 1)
    pdf.cell(0, 8, f'Mediana de Despesas: R$ {stats["mediana_despesas"]:.2f}', 0, 1)
    pdf.cell(0, 8, f'Desvio Padrao: R$ {stats["desvio_padrao"]:.2f}', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'METODOLOGIA 50-30-20', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    pdf.cell(0, 8, f'Necessidades: {analise["perc_necessidades"]:.1f}% (Ideal: 50%)', 0, 1)
    pdf.cell(0, 8, f'Desejos: {analise["perc_desejos"]:.1f}% (Ideal: 30%)', 0, 1)
    pdf.cell(0, 8, f'Investimentos: {analise["perc_investimentos"]:.1f}% (Ideal: 20%)', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'PROXIMOS COMPROMISSOS', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    agenda_futura = sorted(agenda, key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))[:5]
    for comp in agenda_futura:
        pdf.cell(0, 7, f"{comp['data']} {comp['hora']} - {comp['titulo']}", 0, 1)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 9)
    pdf.cell(0, 5, 'Referencias:', 0, 1)
    pdf.cell(0, 5, 'SEBRAE (2023). Metodologia 50-30-20 para orcamento pessoal.', 0, 1)
    pdf.cell(0, 5, 'Silva, J. (2022). Educacao Financeira e Qualidade de Vida.', 0, 1)
    pdf.cell(0, 5, 'Cerbasi, G. (2020). Como Organizar sua Vida Financeira.', 0, 1)
    
    arquivo_pdf = 'relatorio_financeiro.pdf'
    pdf.output(arquivo_pdf)
    
    return arquivo_pdf

def dashboard_principal():
    st.title("💰 Dashboard Principal")
    
    gastos = get_transactions_for_user()
    agenda = get_appointments_for_user()
    
    stats = calcular_estatisticas(gastos)
    analise = analisar_metodo_50_30_20(gastos)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💵 Receitas Totais", f"R$ {stats['total_receitas']:.2f}")
    with col2:
        st.metric("💸 Despesas Totais", f"R$ {stats['total_despesas']:.2f}")
    with col3:
        delta_color = "normal" if stats['saldo'] >= 0 else "inverse"
        st.metric("💰 Saldo", f"R$ {stats['saldo']:.2f}", 
                 delta=f"{stats['saldo']:.2f}")
    
    st.divider()
    
    st.subheader("🚨 Alertas Financeiros")
    alertas = gerar_alertas_financeiros(stats, analise)
    
    for alerta in alertas:
        if alerta['tipo'] == 'danger':
            st.error(f"{alerta['mensagem']}\n\n**Recomendação:** {alerta['recomendacao']}")
        elif alerta['tipo'] == 'warning':
            st.warning(f"{alerta['mensagem']}\n\n**Recomendação:** {alerta['recomendacao']}")
        elif alerta['tipo'] == 'success':
            st.success(f"{alerta['mensagem']}\n\n**Recomendação:** {alerta['recomendacao']}")
        else:
            st.info(f"{alerta['mensagem']}\n\n**Recomendação:** {alerta['recomendacao']}")
    
    st.divider()
    
    st.subheader("📅 Próximos Compromissos")
    
    hoje = datetime.now()
    proximos = []
    
    for comp in agenda:
        try:
            data_comp = datetime.strptime(comp['data'], '%d/%m/%Y')
            if data_comp >= hoje:
                proximos.append((data_comp, comp))
        except:
            continue
    
    proximos.sort(key=lambda x: x[0])
    
    if proximos:
        for data, comp in proximos[:5]:
            dias_falta = (data - hoje).days
            if dias_falta == 0:
                badge = "🔴 HOJE"
            elif dias_falta == 1:
                badge = "🟡 AMANHÃ"
            elif dias_falta <= 7:
                badge = f"🟢 Em {dias_falta} dias"
            else:
                badge = f"📅 {comp['data']}"
            
            st.info(f"**{badge}** - {comp['titulo']} às {comp['hora']}\n\n📍 {comp['local']}")
    else:
        st.info("Nenhum compromisso agendado.")

def cadastrar_transacao():
    st.title("➕ Cadastrar Nova Transação")
    
    with st.form("form_transacao"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01)
            data = st.date_input("Data")
        
        with col2:
            if tipo == "Despesa":
                categorias = ['Moradia', 'Alimentação', 'Transporte', 'Saúde', 
                            'Educação', 'Lazer', 'Vestuário', 'Investimentos', 
                            'Poupança', 'Outros']
            else:
                categorias = ['Salário', 'Freelance', 'Investimentos', 
                            'Presente', 'Outros']
            
            categoria = st.selectbox("Categoria", categorias)
        
        descricao = st.text_area("Descrição")
        
        submitted = st.form_submit_button("💾 Salvar Transação")
        
        if submitted:
            tipo_codigo = 'R' if tipo == "Receita" else 'D'
            
            if add_transaction(None, tipo_codigo, categoria, float(valor), 
                             data.strftime('%d/%m/%Y'), descricao):
                st.success("✅ Transação cadastrada com sucesso!")
                st.balloons()
            else:
                st.error("❌ Erro ao salvar transação.")
    
    st.divider()
    st.subheader("📋 Transações Recentes")
    
    gastos = get_transactions_for_user()
    if gastos:
        df = pd.DataFrame(gastos)
        df['tipo_nome'] = df['tipo'].apply(lambda x: '💵 Receita' if x == 'R' else '💸 Despesa')
        df = df.sort_values('id', ascending=False)
        
        st.dataframe(
            df[['id', 'tipo_nome', 'categoria', 'valor', 'data', 'descricao']].head(10),
            use_container_width=True
        )

def analise_financeira():
    st.title("📊 Análise Financeira Detalhada")
    
    gastos = get_transactions_for_user()
    
    if not gastos:
        st.warning("Nenhuma transação cadastrada. Adicione transações primeiro.")
        return
    
    stats = calcular_estatisticas(gastos)
    analise = analisar_metodo_50_30_20(gastos)
    
    tab1, tab2, tab3 = st.tabs(["📈 Estatísticas", "🎯 Metodologia 50-30-20", "📉 Gráficos"])
    
    with tab1:
        st.subheader("Análise Estatística Descritiva")
        st.write("""
        *Aplicando conceitos de estatística descritiva (Crespo, 2019) para identificar 
        padrões de comportamento financeiro.*
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Média de Despesas", f"R$ {stats['media_despesas']:.2f}")
            st.caption("Valor típico das suas despesas")
            
            st.metric("Mediana de Despesas", f"R$ {stats['mediana_despesas']:.2f}")
            st.caption("Valor central (50% acima, 50% abaixo)")
            
            st.metric("Desvio Padrão", f"R$ {stats['desvio_padrao']:.2f}")
            st.caption("Variabilidade dos gastos")
        
        with col2:
            st.metric("Maior Despesa", f"R$ {stats['max_despesa']:.2f}")
            st.metric("Menor Despesa", f"R$ {stats['min_despesa']:.2f}")
            
            if stats['media_despesas'] > 0:
                cv = (stats['desvio_padrao'] / stats['media_despesas']) * 100
                st.metric("Coeficiente de Variação", f"{cv:.1f}%")
                st.caption("Dispersão relativa dos gastos")
    
    with tab2:
        st.subheader("Metodologia 50-30-20 (SEBRAE, 2023)")
        
        st.write("""
        **Distribuição Ideal:**
        - 💵 **50% Necessidades**: Moradia, alimentação, transporte, saúde, educação
        - 🎯 **30% Desejos**: Lazer, entretenimento, vestuário
        - 💰 **20% Investimentos**: Poupança, aplicações financeiras
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Necessidades", f"{analise['perc_necessidades']:.1f}%", 
                     delta=f"{analise['perc_necessidades'] - 50:.1f}% do ideal")
            st.metric("Desejos", f"{analise['perc_desejos']:.1f}%",
                     delta=f"{analise['perc_desejos'] - 30:.1f}% do ideal")
            st.metric("Investimentos", f"{analise['perc_investimentos']:.1f}%",
                     delta=f"{analise['perc_investimentos'] - 20:.1f}% do ideal")
        
        with col2:
            fig = criar_grafico_comparativo_50_30_20(analise)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Visualizações Interativas com Plotly")
        
        fig_evolucao = criar_grafico_evolucao(gastos)
        if fig_evolucao:
            st.plotly_chart(fig_evolucao, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pizza = criar_grafico_pizza_categorias(gastos)
            if fig_pizza:
                st.plotly_chart(fig_pizza, use_container_width=True)
        
        with col2:
            despesas_por_cat = {}
            for g in gastos:
                if g['tipo'] == 'D':
                    cat = g['categoria']
                    despesas_por_cat[cat] = despesas_por_cat.get(cat, 0) + g['valor']
            
            if despesas_por_cat:
                fig_barras = go.Figure([go.Bar(
                    x=list(despesas_por_cat.keys()),
                    y=list(despesas_por_cat.values()),
                    marker_color='indianred'
                )])
                fig_barras.update_layout(
                    title='Despesas por Categoria',
                    xaxis_title='Categoria',
                    yaxis_title='Valor (R$)',
                    height=400
                )
                st.plotly_chart(fig_barras, use_container_width=True)

def gerenciar_agenda():
    st.title("📅 Gerenciamento de Agenda")
    
    tab1, tab2, tab3 = st.tabs(["➕ Adicionar", "📋 Listar", "📅 Calendário"])
    
    with tab1:
        st.subheader("Novo Compromisso")
        
        with st.form("form_compromisso"):
            titulo = st.text_input("Título do Compromisso")
            
            col1, col2 = st.columns(2)
            with col1:
                data = st.date_input("Data")
                hora = st.time_input("Hora")
            with col2:
                local = st.text_input("Local")
            
            descricao = st.text_area("Descrição / Observações")
            
            submitted = st.form_submit_button("💾 Salvar Compromisso")
            
            if submitted and titulo:
                if add_appointment(None, titulo, data.strftime('%d/%m/%Y'),
                                 hora.strftime('%H:%M'), local, descricao):
                    st.success("✅ Compromisso agendado com sucesso!")
                    st.balloons()
                else:
                    st.error("❌ Erro ao salvar compromisso.")
    
    with tab2:
        st.subheader("Todos os Compromissos")
        
        agenda = get_appointments_for_user()
        if agenda:
            agenda_ordenada = sorted(agenda, 
                                    key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))
            
            for comp in agenda_ordenada:
                with st.expander(f"📌 {comp['data']} {comp['hora']} - {comp['titulo']}"):
                    st.write(f"**Local:** {comp['local']}")
                    st.write(f"**Descrição:** {comp['descricao']}")
                    
                    if st.button(f"🗑️ Excluir", key=f"del_{comp['id']}"):
                        if delete_appointment(comp['id']):
                            st.success("✅ Compromisso excluído!")
                            st.rerun()
        else:
            st.info("Nenhum compromisso cadastrado.")
    
    with tab3:
        agenda = get_appointments_for_user()
        criar_calendario_visual(agenda)

def relatorios_graficos():
    st.title("📄 Relatórios e Exportação")
    
    gastos = get_transactions_for_user()
    agenda = get_appointments_for_user()
    
    if not gastos:
        st.warning("Nenhuma transação cadastrada.")
        return
    
    stats = calcular_estatisticas(gastos)
    analise = analisar_metodo_50_30_20(gastos)
    
    st.subheader("📊 Relatório Consolidado")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Receitas", f"R$ {stats['total_receitas']:.2f}")
    with col2:
        st.metric("Despesas", f"R$ {stats['total_despesas']:.2f}")
    with col3:
        st.metric("Saldo", f"R$ {stats['saldo']:.2f}")
    
    st.divider()
    
    if st.button("📥 Gerar Relatório PDF", type="primary"):
        with st.spinner("Gerando relatório..."):
            arquivo_pdf = gerar_pdf_relatorio(gastos, agenda, stats, analise)
            
            with open(arquivo_pdf, 'rb') as f:
                st.download_button(
                    label="📄 Download do Relatório PDF",
                    data=f,
                    file_name=f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            
            st.success("✅ Relatório gerado com sucesso!")
    
    st.divider()
    
    st.subheader("📋 Tabela Detalhada de Transações")
    
    if gastos:
        df = pd.DataFrame(gastos)
        df['tipo_nome'] = df['tipo'].apply(lambda x: 'Receita' if x == 'R' else 'Despesa')
        
        st.dataframe(
            df[['id', 'tipo_nome', 'categoria', 'valor', 'data', 'descricao']],
            use_container_width=True
        )
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📊 Exportar para CSV",
            csv,
            f"transacoes_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )

def main():
    st.sidebar.title("💰 Sistema de Controle Financeiro")
    st.sidebar.markdown("---")
    st.sidebar.write("**UNISA - Engenharia de Software**")
    st.sidebar.write("Projeto Integrador 2025")
    st.sidebar.write("*Bruna Carramaschi Santos*")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Menu Principal",
        ["🏠 Dashboard", "➕ Cadastrar Transação", "📊 Análise Financeira", 
         "📅 Gerenciar Agenda", "📄 Relatórios e PDF"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Metodologias Aplicadas:**
    - 📚 Metodologia 50-30-20 (SEBRAE, 2023)
    - 📈 Análise Estatística Descritiva
    - 📊 Visualização de Dados (Plotly)
    - 📅 Gestão de Produtividade (GTD)
    """)
    
    if menu == "🏠 Dashboard":
        dashboard_principal()
    elif menu == "➕ Cadastrar Transação":
        cadastrar_transacao()
    elif menu == "📊 Análise Financeira":
        analise_financeira()
    elif menu == "📅 Gerenciar Agenda":
        gerenciar_agenda()
    elif menu == "📄 Relatórios e PDF":
        relatorios_graficos()

# Configurar endpoint webhook para Streamlit
def setup_webhook():
    """Configura endpoint webhook para receber dados POST"""
    try:
        # Verifica se há dados de webhook no query params
        query_params = st.query_params
        if 'webhook_data' in query_params:
            webhook_data = json.loads(query_params['webhook_data'])
            st.session_state['last_webhook_data'] = webhook_data
            st.success(f"✅ Webhook recebido: {webhook_data}")
    except Exception as e:
        pass

if __name__ == "__main__":
    setup_webhook()
    main()
