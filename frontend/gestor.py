import streamlit as st
from auth import get_current_user, make_authenticated_request
import pandas as pd
from datetime import datetime
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
def show_gestor_interface():
    menu = st.sidebar.selectbox("Menu Gestor", ["Dashboard", "Leads", "Usuários"])
    
    if menu == "Dashboard":
        show_gestor_dashboard()
    elif menu == "Leads":
        show_gestor_leads()
    elif menu == "Usuários":
        show_gestor_usuarios()

def show_gestor_dashboard():
    st.header("📊 Dashboard Executivo")

    response = make_authenticated_request("/leads/")
    if response and response.status_code == 200:
        leads = response.json()

        if not leads:
            st.info("📭 Nenhum lead cadastrado ainda.")
            return

        # Converter datas
        for lead in leads:
            lead['created_date'] = datetime.strptime(lead['created_at'][:10], '%Y-%m-%d')

        # ===== MÉTRICAS PRINCIPAIS =====
        st.subheader("📈 Visão Geral")

        total_leads = len(leads)
        fechados = len([l for l in leads if l['status'] == 'fechado'])
        perdidos = len([l for l in leads if l['status'] == 'perdido'])
        em_andamento = total_leads - fechados - perdidos
        taxa_conversao = (fechados / total_leads * 100) if total_leads > 0 else 0

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("📋 Total de Leads", total_leads)
        col2.metric("✅ Fechados", fechados, delta=f"{taxa_conversao:.1f}%")
        col3.metric("❌ Perdidos", perdidos)
        col4.metric("🔄 Em Andamento", em_andamento)
        col5.metric("🎯 Taxa de Conversão", f"{taxa_conversao:.1f}%")

        st.markdown("---")

        # ===== ESTATÍSTICAS DESCRITIVAS =====
        st.subheader("📐 Estatísticas Descritivas dos Leads")

        df_leads = pd.DataFrame(leads)
        df_leads['data'] = pd.to_datetime(df_leads['created_at'], format='ISO8601').dt.date
        leads_por_dia_series = df_leads.groupby('data').size()

        if len(leads_por_dia_series) > 0:
            # Calcular estatísticas
            media = leads_por_dia_series.mean()
            mediana = leads_por_dia_series.median()
            desvio_padrao = leads_por_dia_series.std()
            modo_valores = leads_por_dia_series.mode()
            moda = modo_valores.iloc[0] if len(modo_valores) > 0 else 0
            minimo = leads_por_dia_series.min()
            maximo = leads_por_dia_series.max()
            
            # Assimetria (Skewness)
            assimetria = leads_por_dia_series.skew()
            
            # Curtose (Kurtosis)
            curtose = leads_por_dia_series.kurtosis()

            # Intervalo de confiança (95%)
            confianca = 0.95
            graus_liberdade = len(leads_por_dia_series) - 1
            ic_inferior = 0
            ic_superior = 0
            if graus_liberdade > 0:
                t_critico = stats.t.ppf((1 + confianca) / 2, graus_liberdade)
                erro_padrao = desvio_padrao / np.sqrt(len(leads_por_dia_series))
                margem_erro = t_critico * erro_padrao
                ic_inferior = media - margem_erro
                ic_superior = media + margem_erro

            # Exibir métricas em cards - Linha 1
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("📊 Média de Leads/Dia", f"{media:.2f}")
            with col2:
                st.metric("📏 Mediana", f"{mediana:.1f}")
            with col3:
                st.metric("🎯 Moda", f"{moda:.0f}")
            with col4:
                st.metric("📈 Amplitude", f"{minimo:.0f} - {maximo:.0f}")
            with col5:
                st.metric("📊 Desvio Padrão", f"{desvio_padrao:.2f}")
            
            # Exibir métricas adicionais - Linha 2
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🔄 Assimetria", f"{assimetria:.2f}")
            with col2:
                st.metric("📐 Curtose", f"{curtose:.2f}")
            with col3:
                if graus_liberdade > 0:
                    st.metric("📊 Intervalo de Confiança 95%", f"[{ic_inferior:.2f}, {ic_superior:.2f}]")
                else:
                    st.metric("📊 Intervalo de Confiança 95%", "N/A")

            # Incluir explicações didáticas
            st.markdown(f"""
            ### 📊 Explicação das Estatísticas
            
            **Medidas de Tendência Central:**
            - **Média ({media:.2f})**: O número médio de leads gerados por dia. Representa o "centro" dos dados.
            - **Mediana ({mediana:.1f})**: O valor central quando ordenamos os dias. Metade dos dias tem menos leads, metade tem mais.
            - **Moda ({moda:.0f})**: O número de leads que aparece com mais frequência. É o cenário mais comum.
            
            **Medidas de Dispersão:**
            - **Amplitude ({minimo:.0f} - {maximo:.0f})**: A diferença entre o menor e maior número de leads. Mostra a variação total.
            - **Desvio Padrão ({desvio_padrao:.2f})**: Mede o quanto os dados se afastam da média. Valores altos indicam grande variação nos resultados diários.
            - **Intervalo de Confiança 95% ([{ic_inferior:.2f}, {ic_superior:.2f}])**: Com 95% de confiança, a verdadeira média de leads por dia está neste intervalo. É uma margem de segurança para nossas estimativas.
            
            **Forma da Distribuição:**
            - **Assimetria ({assimetria:.2f})**: Indica se a distribuição é simétrica ou não. 
              - Valor = 0: distribuição perfeitamente simétrica
              - Valor > 0: mais dias com poucos leads (cauda à direita)
              - Valor < 0: mais dias com muitos leads (cauda à esquerda)
            
            - **Curtose ({curtose:.2f})**: Mede o "achatamento" da distribuição.
              - Valor = 0: distribuição normal (referência)
              - Valor > 0: mais concentrada (picos acentuados)
              - Valor < 0: mais espalhada (achatada)
            
            💡 **Dica**: Estas estatísticas ajudam a entender padrões e tomar decisões estratégicas baseadas em dados reais.
            """)

            # Gerar o histograma
            st.subheader("📊 Distribuição de Leads")
            
            st.markdown("""
            **O que é este gráfico?**
            
            Este histograma mostra visualmente como os leads se distribuem ao longo dos dias. Cada barra representa quantos dias 
            tiveram um determinado número de leads.
            
            **Como interpretar:**
            - **Eixo X (Quantidade de Leads)**: Mostra o número de leads gerados
            - **Eixo Y (Frequência)**: Mostra quantos dias tiveram aquela quantidade de leads
            - **Altura das barras**: Barras mais altas indicam que aquele número de leads é mais comum
            - **Formato geral**: Se o gráfico é simétrico, assimétrico, concentrado ou espalhado
            
            💡 Use este gráfico para identificar padrões: dias típicos têm quantos leads? Existem dias excepcionais?
            """)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            leads_por_dia_series.plot(kind='hist', bins=30, ax=ax, alpha=0.7, color='#1E88E5')
            ax.set_title("Distribuição dos Leads por Dia", fontsize=14, fontweight='bold')
            ax.set_xlabel("Quantidade de Leads", fontsize=12)
            ax.set_ylabel("Frequência (Número de Dias)", fontsize=12)
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)

            # Fornecer tabela para download
            st.subheader("📥 Download dos Dados de Leads")
            csv = df_leads.to_csv(index=False)
            st.download_button("Baixar Dados como CSV", csv, "leads.csv", "text/csv")

        else:
            st.info("📊 Dados insuficientes para calcular estatísticas descritivas. Aguarde mais leads serem cadastrados.")

        st.markdown("---")
    else:
        st.error("❌ Erro ao carregar dados do dashboard")