import pandas as pd
import plotly.graph_objects as go
import requests
import os
from datetime import datetime
import json
import time

TRANSLATIONS = {
    "pt": {
    }
}

# ==============================================================================
# ETAPA 1: EXTRAÇÃO DE DADOS
# ==============================================================================

def extrair_dados_comex(anos, ncm_codes):
    """
    Busca os dados de importação na API do Comex Stat para os anos e NCMs especificados.
    """
    print(f"🔎 Buscando dados para os anos: {anos} e NCMs: {len(ncm_codes)}")
    all_data = []
    base_url = "https://api.comexstat.mdic.gov.br/general"

    for ano in anos:
        for ncm in ncm_codes:
            params = {
                "flow": "2",  # 2 para Importação
                "period": str(ano),
                "partner": "0", # Todos os países
                "product": ncm,
                "type": "raw"
            }
            
            retries = 3
            for attempt in range(retries):
                try:
                    response = requests.get(base_url, params=params, timeout=60)
                    response.raise_for_status()  # Lança um erro para códigos 4xx/5xx
                    
                    data = response.json()
                    if data:
                        print(f"   ✅ Sucesso para Ano: {ano}, NCM: {ncm}. {len(data)} registros encontrados.")
                        all_data.extend(data)
                    else:
                        print(f"   ⚠️ Nenhum dado para Ano: {ano}, NCM: {ncm}.")
                    
                    break # Sai do loop de retentativas se for bem-sucedido

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429: # Erro de "Too Many Requests"
                        wait_time = (attempt + 1) * 5 # Espera 5, 10, 15 segundos
                        print(f"   ⏳ API Rate Limit atingido. Tentando novamente em {wait_time} segundos...")
                        time.sleep(wait_time)
                    else:
                        print(f"   ❌ Erro HTTP para Ano: {ano}, NCM: {ncm}. Status: {e.response.status_code}")
                        break
                except requests.exceptions.RequestException as e:
                    print(f"   ❌ Erro de conexão para Ano: {ano}, NCM: {ncm}. Causa: {e}")
                    break
            else: # Executado se o loop de retentativas falhar todas as vezes
                print(f"   ❌ Falha ao buscar dados para Ano: {ano}, NCM: {ncm} após {retries} tentativas.")

    if not all_data:
        return None

    df = pd.DataFrame(all_data)
    print(f"\nTotal de {len(df)} registros brutos extraídos.")

    # --- ENRIQUECIMENTO DOS DADOS ---
    print("✨ Enriquecendo os dados...")
    
    # Renomear colunas para nomes mais amigáveis
    rename_map = {
        'co_ano': 'Ano', 'co_mes': 'Mês', 'co_pais': 'Cód. País', 'no_pais': 'País de Origem',
        'co_ncm': 'NCM', 'vl_fob': 'Valor US$ FOB', 'vl_cif': 'Valor US$ CIF', 'qt_estat': 'Quantidade Estatística'
    }
    df = df.rename(columns=rename_map)

    # Criar coluna 'HP Bucket'
    def assign_hp_bucket(ncm):
        if str(ncm).startswith('870191'): return '25 - 50HP'
        if str(ncm).startswith('870192'): return '51 - 100HP'
        if str(ncm).startswith('870193'): return '100 - 175HP'
        if str(ncm).startswith('870194'): return '> 176 HP'
        if str(ncm).startswith('870195'): return '> 176 HP'
        return '0 - 24HP' # Categoria padrão

    df['HP Bucket'] = df['NCM'].apply(assign_hp_bucket)
    print("   ✅ Coluna 'HP Bucket' criada.")

    # Selecionar e reordenar colunas finais
    final_cols = [
        'Ano', 'Mês', 'País de Origem', 'NCM', 'HP Bucket', 
        'Valor US$ FOB', 'Valor US$ CIF', 'Quantidade Estatística'
    ]
    df = df[final_cols]
    
    return df


# ==============================================================================
# ETAPA 2: GERAÇÃO DO DASHBOARD
# ==============================================================================

def format_large_number(num):
    return f"{num:,.0f}".replace(",", ".")

def criar_fig_pais(df_agg):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_agg['País de Origem'], y=df_agg['Valor US$ FOB'], name='FOB', text=df_agg['Valor US$ FOB'].apply(format_large_number), textposition='outside'))
    fig.add_trace(go.Bar(x=df_agg['País de Origem'], y=df_agg['Valor US$ CIF'], name='CIF', text=df_agg['Valor US$ CIF'].apply(format_large_number), textposition='outside', visible=False))
    fig.add_trace(go.Bar(x=df_agg['País de Origem'], y=df_agg['Quantidade Estatística'], name='Quantidade', text=df_agg['Quantidade Estatística'].apply(format_large_number), textposition='outside', visible=False))
    fig.update_layout(
        title_text=TRANSLATIONS['pt']['chart1_title'], title_x=0.5,
        updatemenus=[dict(active=0, buttons=list([
        ]), direction="down", x=0.05, xanchor="left", y=1.15, yanchor="top")]
    )
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_yaxes(title_text=TRANSLATIONS['pt']['total_fob_value'])
    fig.update_xaxes(categoryorder='total descending')
    return fig

def gerar_dashboard(df: pd.DataFrame):
    print("🚀 Iniciando a geração do dashboard...")

    # --- LIMPEZA E BLINDAGEM DE DADOS ---
    print("   -> Limpando e preparando os dados...")
    numeric_cols = ['Valor US$ FOB', 'Ano', 'Mês', 'Quantidade Estatística', 'Valor US$ CIF']
    for col in numeric_cols:
        if col in df.columns:

    print(f"\n🎉 SUCESSO! O dashboard foi gerado e salvo em:\n👉 {dashboard_path}")


# ==============================================================================
# ETAPA 3: ORQUESTRADOR PRINCIPAL
# ==============================================================================

def main():
    """
    Orquestra o processo completo: extrai, salva e gera o dashboard.
    """
    # --- PARÂMETROS DE EXTRAÇÃO ---
    # Adicione aqui todos os NCMs de tratores que você deseja monitorar
    codigos_ncm_tratores = [
        "87019100", "87019200", "87019300", "87019410", "87019490", 
        "87019510", "87019590"
    ]
    anos_desejados = [2023, 2024] # Anos para buscar na API

    # 1. Extrair dados frescos da API
    df_fresco = extrair_dados_comex(anos=anos_desejados, ncm_codes=codigos_ncm_tratores)

    if df_fresco is None or df_fresco.empty:
        print("\n❌ NENHUM DADO FOI EXTRAÍDO. Abortando a geração do dashboard.")
        return

    # 2. Salvar os dados frescos em um arquivo Excel
    hoje = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo_excel = f"Imports database_{hoje}.xlsx"
    print(f"\n💾 Salvando dados frescos em: {nome_arquivo_excel}")
    df_fresco.to_excel(nome_arquivo_excel, index=False)

    # 3. Gerar o dashboard usando os dados frescos
    gerar_dashboard(df_fresco)

if __name__ == "__main__":
    main()

