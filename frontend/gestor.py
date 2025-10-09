
import streamlit as st
from auth import get_current_user, make_authenticated_request
import pandas as pd
from datetime import datetime
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import time

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
    
    # Controles de atualização
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        auto_refresh = st.checkbox("🔄 Atualização Automática", value=False, key="auto_refresh")
    
    with col2:
        if auto_refresh:
            refresh_interval = st.selectbox(
                "Intervalo de atualização",
                options=[10, 30, 60, 120],
                format_func=lambda x: f"{x} segundos",
                key="refresh_interval"
            )
    
    with col3:
        if st.button("🔄 Atualizar Agora", use_container_width=True):
            st.rerun()
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()
    
    st.markdown("---")

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
        st.subheader("📈 Visão Geral de Performance")

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
        st.subheader("📊 Análise Inteligente de Performance")

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
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Média Diária", f"{media:.1f} leads/dia")
            with col2:
                st.metric("📏 Valor Central (Mediana)", f"{mediana:.0f} leads")
            with col3:
                st.metric("🎯 Resultado Mais Comum", f"{moda:.0f} leads")
            with col4:
                st.metric("📈 Variação", f"{minimo:.0f} a {maximo:.0f} leads")
            
            # Exibir métricas adicionais - Linha 2
            col1, col2, col3 = st.columns(3)
            with col1:
                variacao_percentual = (desvio_padrao / media * 100) if media > 0 else 0
                st.metric("📊 Estabilidade", f"±{desvio_padrao:.1f} leads", 
                         delta=f"{variacao_percentual:.0f}% de variação")
            with col2:
                if graus_liberdade > 0:
                    st.metric("🎯 Meta Realista (95% confiança)", f"{ic_inferior:.1f} a {ic_superior:.1f}")
                else:
                    st.metric("🎯 Meta Realista (95% confiança)", "N/A")
            with col3:
                # Interpretação da previsibilidade
                if abs(assimetria) < 0.5:
                    previsibilidade = "Alta"
                    emoji = "🟢"
                elif abs(assimetria) < 1:
                    previsibilidade = "Média"
                    emoji = "🟡"
                else:
                    previsibilidade = "Baixa"
                    emoji = "🔴"
                st.metric("🔮 Previsibilidade", f"{emoji} {previsibilidade}")

            # Explicações contextualizadas
            st.markdown("---")
            st.subheader("💡 O que esses números significam para o seu negócio?")
            
            # Card 1 - Performance Atual
            with st.container():
                st.markdown(f"""
                ### 📊 **Cenário Atual da Geração de Leads**
                
                **Sua operação está gerando em média {media:.1f} leads por dia.** Isso significa que, se mantiver o ritmo atual, 
                você pode esperar aproximadamente **{media * 30:.0f} leads por mês** e **{media * 365:.0f} leads por ano**.
                
                - 📌 **Dia típico:** {mediana:.0f} leads (metade dos dias tem mais, metade tem menos)
                - 🎯 **Cenário mais frequente:** {moda:.0f} leads (o número que mais se repete)
                - 📈 **Melhor dia:** {maximo:.0f} leads
                - 📉 **Pior dia:** {minimo:.0f} leads
                """)
            
            # Card 2 - Estabilidade
            with st.container():
                if variacao_percentual < 30:
                    estabilidade_texto = "**EXCELENTE** - Seus resultados são muito consistentes"
                    cor_estabilidade = "🟢"
                    conselho_estabilidade = "Continue com as estratégias atuais, pois estão trazendo resultados previsíveis."
                elif variacao_percentual < 50:
                    estabilidade_texto = "**BOA** - Existe alguma variação, mas é controlável"
                    cor_estabilidade = "🟡"
                    conselho_estabilidade = "Identifique os dias com melhor performance e replique as ações nesses dias."
                else:
                    estabilidade_texto = "**ATENÇÃO** - Resultados muito variáveis"
                    cor_estabilidade = "🔴"
                    conselho_estabilidade = "Foque em criar processos padronizados para estabilizar a geração de leads."
                
                st.markdown(f"""
                ### 📊 **Estabilidade da Operação** {cor_estabilidade}
                
                {estabilidade_texto}. Seus resultados variam em **±{desvio_padrao:.1f} leads** em relação à média, 
                o que representa uma oscilação de **{variacao_percentual:.0f}%**.
                
                **O que isso significa:** Em dias normais, você pode esperar entre **{max(0, media - desvio_padrao):.0f}** 
                e **{media + desvio_padrao:.0f}** leads.
                
                💡 **Ação Recomendada:** {conselho_estabilidade}
                """)
            
            # Card 3 - Metas Realistas
            with st.container():
                st.markdown(f"""
                ### 🎯 **Metas Realistas para Planejamento**
                
                Com **95% de confiança**, sua operação deve gerar entre **{ic_inferior:.1f}** e **{ic_superior:.1f}** leads por dia.
                
                **Como usar essa informação:**
                - 📋 **Para contratar equipe:** Planeje para {ic_inferior:.0f} leads/dia (cenário conservador)
                - 💰 **Para projeção de receita:** Use {media:.1f} leads/dia (cenário realista)
                - 🚀 **Para metas de crescimento:** Almeje {ic_superior:.1f} leads/dia (cenário otimista)
                
                🎯 **Meta mensal realista:** Entre **{ic_inferior * 30:.0f}** e **{ic_superior * 30:.0f}** leads
                """)
            
            # Card 4 - Padrão de Comportamento
            with st.container():
                if assimetria > 0.5:
                    padrao = f"Você tem **muitos dias com poucos leads** ({minimo:.0f}-{mediana:.0f}) e **alguns dias excepcionais** com {maximo:.0f} leads."
                    interpretacao = "Seus picos de performance são raros. Descubra o que aconteceu nos melhores dias e tente replicar."
                    emoji_padrao = "📈"
                elif assimetria < -0.5:
                    padrao = f"Você tem **muitos dias com bons resultados** ({mediana:.0f}-{maximo:.0f}) mas **alguns dias ruins** com apenas {minimo:.0f} leads."
                    interpretacao = "Sua operação é geralmente forte. Identifique os dias ruins para evitar que se repitam."
                    emoji_padrao = "📊"
                else:
                    padrao = f"Seus resultados são **bem distribuídos** entre {minimo:.0f} e {maximo:.0f} leads, com {mediana:.0f} sendo o ponto central."
                    interpretacao = "Operação equilibrada e previsível. Foque em aumentar a média mantendo a consistência."
                    emoji_padrao = "⚖️"
                
                if curtose > 1:
                    concentracao = "Os resultados são muito **concentrados ao redor da média**, com poucos extremos."
                    acao_curtose = "Seu processo é estável, mas pode estar limitado. Teste novas estratégias para buscar crescimento."
                elif curtose < -1:
                    concentracao = "Os resultados são muito **espalhados**, com muitos dias fora do padrão."
                    acao_curtose = "Alta variabilidade indica falta de processo. Padronize as ações para maior previsibilidade."
                else:
                    concentracao = "A distribuição dos resultados é **normal e saudável**."
                    acao_curtose = "Continue monitorando e ajustando conforme necessário."
                
                st.markdown(f"""
                ### {emoji_padrao} **Padrão de Comportamento dos Leads**
                
                **Distribuição:** {padrao}
                
                **Concentração:** {concentracao}
                
                💡 **Interpretação:** {interpretacao}
                
                🎯 **Ação Recomendada:** {acao_curtose}
                """)

            # Gráfico Visual com Interpretação
            st.markdown("---")
            st.subheader("📊 Visualização da Distribuição de Leads")
            
            st.markdown(f"""
            ### 📈 Como interpretar este gráfico:
            
            Este gráfico mostra **quantos dias você teve cada quantidade de leads**.
            
            - **Eixo Horizontal (Quantidade de Leads):** Mostra o número de leads gerados
            - **Eixo Vertical (Número de Dias):** Mostra quantos dias tiveram aquela quantidade
            - **Barras mais altas:** Indicam quantidades de leads que aconteceram em mais dias (mais comuns)
            - **Linha vermelha:** Representa sua média de {media:.1f} leads/dia
            
            💡 **O que procurar:**
            - Se as barras estão concentradas perto da média = **operação estável**
            - Se as barras estão espalhadas = **operação com muita variação**
            - Se tem barras muito à direita = **você teve dias excepcionais**
            """)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Histograma
            n, bins, patches = ax.hist(leads_por_dia_series, bins=min(30, len(leads_por_dia_series)), 
                                       alpha=0.7, color='#1E88E5', edgecolor='black', linewidth=1.2)
            
            # Linha da média
            ax.axvline(media, color='red', linestyle='--', linewidth=2, 
                      label=f'Média: {media:.1f} leads/dia', alpha=0.8)
            
            # Área de confiança
            if graus_liberdade > 0:
                ax.axvspan(ic_inferior, ic_superior, alpha=0.2, color='green', 
                          label=f'Zona de confiança 95%: {ic_inferior:.1f} - {ic_superior:.1f}')
            
            ax.set_title("Distribuição de Leads por Dia - Análise Visual", fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel("Quantidade de Leads por Dia", fontsize=13, fontweight='bold')
            ax.set_ylabel("Quantidade de Dias", fontsize=13, fontweight='bold')
            ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Destacar barra mais alta
            max_height = max(n)
            for i, patch in enumerate(patches):
                if patch.get_height() == max_height:
                    patch.set_facecolor('#FF9800')
                    patch.set_edgecolor('black')
                    patch.set_linewidth(2)
            
            st.pyplot(fig)
            
            # Resumo Executivo Final
            st.markdown("---")
            st.subheader("📋 Resumo Executivo - Ações Prioritárias")
            
            # Explicação do Resumo Executivo
            with st.expander("ℹ️ O que é o Resumo Executivo? Clique para entender", expanded=False):
                st.markdown("""
                ### 📋 O que é o Resumo Executivo?
                
                O **Resumo Executivo** apresenta as **3 ações mais importantes** que você deve tomar com base nos dados analisados. 
                É como um "roteiro de prioridades" gerado automaticamente pelo sistema.
                
                ### 🎯 Como funciona?
                
                O sistema analisa automaticamente três aspectos principais do seu negócio:
                
                #### 1️⃣ **Análise da Taxa de Conversão** (Fechamentos ÷ Total de Leads)
                
                - **Abaixo de 20%:** 🚨 URGENTE - Revise o processo de vendas
                - **Entre 20% e 40%:** ⚠️ IMPORTANTE - Treine a equipe
                - **Acima de 40%:** ✅ PARABÉNS - Foque em aumentar o volume
                
                #### 2️⃣ **Análise da Estabilidade** (Variação nos resultados)
                
                - **Variação > 50%:** 📊 PADRONIZAR - Crie processos fixos
                - **Variação 30-50%:** 🔧 OTIMIZAR - Replique os melhores dias
                - **Variação < 30%:** 🎯 ESCALAR - Hora de crescer
                
                #### 3️⃣ **Análise do Volume** (Média de leads por dia)
                
                - **Menos de 5 leads/dia:** 📈 CRESCER - Invista em marketing
                - **Entre 5 e 20 leads/dia:** 💪 EXPANDIR - Explore novos canais
                - **Mais de 20 leads/dia:** 🚀 MANTER - Foque na qualidade
                
                ### 💡 Por que isso é importante?
                
                Como gestor, você não precisa ser especialista em estatística. O sistema **traduz números complexos em ações práticas** 
                que você pode implementar imediatamente. É como ter um consultor de negócios 24/7 analisando seus dados!
                """)
            
            acoes = []
            
            # Ação 1 - Baseada na taxa de conversão
            if taxa_conversao < 20:
                acoes.append("🚨 **URGENTE:** Taxa de conversão baixa. Revise o processo de vendas e qualificação dos leads.")
            elif taxa_conversao < 40:
                acoes.append("⚠️ **IMPORTANTE:** Taxa de conversão pode melhorar. Treine a equipe e aprimore o follow-up.")
            else:
                acoes.append("✅ **PARABÉNS:** Excelente taxa de conversão! Foque em aumentar o volume de leads.")
            
            # Ação 2 - Baseada na estabilidade
            if variacao_percentual > 50:
                acoes.append("📊 **PADRONIZAR:** Crie processos fixos para reduzir a variação nos resultados.")
            elif variacao_percentual > 30:
                acoes.append("🔧 **OTIMIZAR:** Identifique e replique as ações dos melhores dias.")
            else:
                acoes.append("🎯 **ESCALAR:** Operação estável. Hora de investir em crescimento.")
            
            # Ação 3 - Baseada no volume
            if media < 5:
                acoes.append("📈 **CRESCER:** Volume baixo de leads. Invista em marketing e aquisição.")
            elif media < 20:
                acoes.append("💪 **EXPANDIR:** Volume moderado. Explore novos canais de aquisição.")
            else:
                acoes.append("🚀 **MANTER:** Excelente volume. Foque em manter a qualidade.")
            
            for i, acao in enumerate(acoes, 1):
                st.markdown(f"**{i}.** {acao}")

            # Download dos Dados
            st.markdown("---")
            st.subheader("📥 Exportar Dados")
            csv = df_leads.to_csv(index=False)
            st.download_button(
                label="⬇️ Baixar Relatório Completo (CSV)",
                data=csv,
                file_name=f"relatorio_leads_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        else:
            st.info("📊 Dados insuficientes para calcular estatísticas. Aguarde mais leads serem cadastrados.")

        st.markdown("---")
    else:
        st.error("❌ Erro ao carregar dados do dashboard")
