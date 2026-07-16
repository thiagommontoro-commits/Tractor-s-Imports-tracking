import pandas as pd
import plotly.graph_objects as go
import requests
import os
import glob
from datetime import datetime
import json
import time

TRANSLATIONS = {
    "pt": {
        "dashboard_title": "Dashboard de Importações",
        "dashboard_h1": "Dashboard de Importações de Tratores",
        "dashboard_subtitle": "Análise de dados da API Comex Stat",
        "developed_by": "Desenvolvido por",
        "data_source": "Fonte dos Dados:",
        "last_update": "Última Atualização:",
        "analyzed_period": "Período Analisado:",
        "global_filter_label": "Filtro Global (KPIs, Barras e Tabela):",
        "kpi_total_value": "Valor Total Importado",
        "kpi_total_qty": "Quantidade Total",
        "kpi_origin_countries": "Países de Origem",
        "chart1_title": "Análise de Importação por País de Origem",
        "fob_value": "Valor US$ FOB",
        "cif_value": "Valor US$ CIF",
        "quantity": "Quantidade",
        "total_fob_value": "Valor Total (US$ FOB)",
        "total_cif_value": "Valor Total (US$ CIF)",
        "total_quantity_axis": "Quantidade Total",
        "table_title": "Análise Anual por País",
        "donut_title": "Distribuição por HP Bucket",
        "donut_filter_label": "Cortes Exclusivos da Rosca:",
        "all_years": "Todos os Anos",
        "all_countries": "Todos os Países",
        "annual_cumulative": "Acumulado Anual",
        "cumulative_until_month": "Acumulado até Mês",
        "no_data_period": "Sem dados para o período.",
        "origin_country_header": "País de Origem",
        "hover_qty": "Qtd",
    },
    "en": {
        "dashboard_title": "Imports Dashboard",
        "dashboard_h1": "Tractor Imports Dashboard",
        "dashboard_subtitle": "Comex Stat API Data Analysis",
        "developed_by": "Developed by",
        "data_source": "Data Source:",
        "last_update": "Last Update:",
        "analyzed_period": "Analyzed Period:",
        "global_filter_label": "Global Filter (KPIs, Bars, and Table):",
        "kpi_total_value": "Total Imported Value",
        "kpi_total_qty": "Total Quantity",
        "kpi_origin_countries": "Origin Countries",
        "chart1_title": "Import Analysis by Country of Origin",
        "fob_value": "FOB Value US$",
        "cif_value": "CIF Value US$",
        "quantity": "Quantity",
        "total_fob_value": "Total Value (US$ FOB)",
        "total_cif_value": "Total Value (US$ CIF)",
        "total_quantity_axis": "Total Quantity",
        "table_title": "Annual Analysis by Country",
        "donut_title": "Distribution by HP Bucket",
        "donut_filter_label": "Donut Chart Exclusive Slices:",
        "all_years": "All Years",
        "all_countries": "All Countries",
        "annual_cumulative": "Annual Cumulative",
        "cumulative_until_month": "Cumulative up to Month",
        "no_data_period": "No data for the period.",
        "origin_country_header": "Country of Origin",
        "hover_qty": "Qty",
    }
}

    def assign_hp_bucket(ncm):
        if str(ncm).startswith('870191'): return '25 - 50HP'
        if str(ncm).startswith('870192'): return '51 - 100HP'
        if str(ncm).startswith('870193'): return '100 - 175HP'
        if str(ncm).startswith('870193'): return '101 - 175HP'
        if str(ncm).startswith('870194'): return '> 176 HP'
        if str(ncm).startswith('870195'): return '> 176 HP'
        return '0 - 24HP' # Categoria padrão
    fig.add_trace(go.Bar(x=df_agg['País de Origem'], y=df_agg['Quantidade Estatística'], name='Quantidade', text=df_agg['Quantidade Estatística'].apply(format_large_number), textposition='outside', visible=False))
    fig.update_layout(
        title_text=TRANSLATIONS['pt']['chart1_title'], title_x=0.5,
        updatemenus=[dict(active=0, buttons=list([
            dict(label=TRANSLATIONS['pt']['fob_value'], method="update", args=[{"visible": [True, False, False]}, {"yaxis.title": TRANSLATIONS['pt']['total_fob_value']}]),
            dict(label=TRANSLATIONS['pt']['cif_value'], method="update", args=[{"visible": [False, True, False]}, {"yaxis.title": TRANSLATIONS['pt']['total_cif_value']}]),
            dict(label=TRANSLATIONS['pt']['quantity'], method="update", args=[{"visible": [False, False, True]}, {"yaxis.title": TRANSLATIONS['pt']['total_quantity_axis']}])
        ]), direction="down", x=0.05, xanchor="left", y=1.15, yanchor="top")]
    )
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_yaxes(title_text="Valor Total (US$ FOB)")
    fig.update_yaxes(title_text=TRANSLATIONS['pt']['total_fob_value'])
    fig.update_xaxes(categoryorder='total descending')
    return fig

def gerar_dashboard(df: pd.DataFrame = None):
def gerar_dashboard(df: pd.DataFrame):
    print("🚀 Iniciando a geração do dashboard...")
    project_path = "."

    if df is None:
        search_pattern = os.path.join(project_path, "Imports database_*.xlsx")
        lista_arquivos = glob.glob(search_pattern)
        if not lista_arquivos:
            print(f"❌ ERRO: Nenhum arquivo Excel encontrado.")
            return

        caminho_arquivo = max(lista_arquivos, key=os.path.getctime)
        print(f"📊 Lendo dados do arquivo: {os.path.basename(caminho_arquivo)}")
        try:
            df = pd.read_excel(caminho_arquivo)
        except Exception as e:
            print(f"❌ ERRO: Falha ao ler o arquivo Excel. Causa: {e}")
            return

    # --- LIMPEZA E BLINDAGEM DE DADOS ---
    print("   -> Limpando e preparando os dados...")
    numeric_cols = ['Valor US$ FOB', 'Ano', 'Mês', 'Quantidade Estatística', 'Valor US$ CIF']
    for col in numeric_cols:
        if col in df.columns:

    print(f"\n🎉 SUCESSO! O dashboard foi gerado e salvo em:\n👉 {dashboard_path}")
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(subset=['Valor US$ FOB', 'Ano', 'Mês'], inplace=True)
    df['Mês'] = df['Mês'].astype(int)
    df['Ano'] = df['Ano'].astype(int)

    for col in ['Quantidade Estatística', 'Valor US$ CIF']:
        if col in df.columns: df[col] = df[col].fillna(0)

    ano_min = int(df['Ano'].min())
    ano_max = int(df['Ano'].max())

    metric_options = ['Valor US$ FOB', 'Valor US$ CIF', 'Quantidade Estatística']
    hp_order = ['0 - 24HP', '25 - 50HP', '51 - 100HP', '101 - 175HP', '> 176 HP']
    
    anos_list = sorted(df['Ano'].unique())
    paises_list = sorted(df['País de Origem'].unique())

    # --- GRÁFICOS INICIAIS ---
    print("   -> Gerando Gráfico de Barras Iniciais...")
    initial_country_data = df.groupby('País de Origem')[metric_options].sum().reset_index()
    fig1 = criar_fig_pais(initial_country_data)

    # --- CUBO DE DADOS MASTER ---
    print("   -> Construindo cubo multidimensional de meses, anos e países...")
    master_data = {}
    global_filter_options = [('Total Anual', 'total')] + [(f'Acumulado até Mês {i}', i) for i in range(1, 13)]

    for label, month_key in global_filter_options:
        key = str(month_key)
        
        if month_key == 'total': df_periodo = df
        else: df_periodo = df[df['Mês'] <= month_key]

        kpi_fob = df_periodo['Valor US$ FOB'].sum()
        kpi_qty = df_periodo['Quantidade Estatística'].sum()
        kpi_paises = df_periodo['País de Origem'].nunique()

        country_data = df_periodo.groupby('País de Origem')[metric_options].sum().reset_index()
        if country_data.empty: country_data = pd.DataFrame([{'País de Origem': 'Nenhum dado', 'Valor US$ FOB': 0, 'Valor US$ CIF': 0, 'Quantidade Estatística': 0}])
        fig_pais_periodo = criar_fig_pais(country_data)

        table_data_by_metric = {}
        for metrica in metric_options:
            df_pivot = df_periodo.groupby(['País de Origem', 'Ano'])[metrica].sum().unstack().fillna(0)
            df_pivot = df_pivot.reindex(columns=anos_list, fill_value=0)
            if anos_list: df_pivot = df_pivot.sort_values(by=anos_list[-1], ascending=False)
            
            df_pivot_formatted = df_pivot.map(format_large_number)
            cell_values = [df_pivot_formatted.index.tolist()] + [df_pivot_formatted[ano].tolist() for ano in anos_list]
            table_data_by_metric[metrica] = cell_values

        donut_cube = {}
        opcoes_ano = ['Todos'] + [str(a) for a in anos_list]
        opcoes_pais = ['Todos'] + paises_list

        for y in opcoes_ano:
            donut_cube[y] = {}
            df_y = df_periodo if y == 'Todos' else df_periodo[df_periodo['Ano'] == int(y)]
            
            for p in opcoes_pais:
                df_p = df_y if p == 'Todos' else df_y[df_y['País de Origem'] == p]
                
                if df_p.empty:
                    d_fob = [0]*len(hp_order)
                    d_cif = [0]*len(hp_order)
                    d_qty = [0]*len(hp_order)
                else:
                    hp_agg = df_p.groupby('HP Bucket')[metric_options].sum().reindex(hp_order, fill_value=0).reset_index()
                    d_fob = hp_agg['Valor US$ FOB'].tolist()
                    d_cif = hp_agg['Valor US$ CIF'].tolist()
                    d_qty = hp_agg['Quantidade Estatística'].tolist()

                donut_cube[y][p] = {
                    'labels': hp_order,
                    'fob': d_fob,
                    'cif': d_cif,
                    'qty': d_qty,
                }

        master_data[key] = {
            'kpis': {'fob': f"US$ {format_large_number(kpi_fob)}", 'qty': format_large_number(kpi_qty), 'paises': str(kpi_paises)},
            'chart1': json.loads(fig_pais_periodo.to_json()),
            'chart3_table': table_data_by_metric,
            'donut_cube': donut_cube
        }

    # --- MONTAGEM DO HTML ---
    print("   -> Montando o arquivo HTML final...")
    project_path = "."
    graph1_div = fig1.to_html(full_html=False, include_plotlyjs='cdn', div_id='chart1_div')
    data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")

    meses_options_html = f'<option value="total" data-translate-key="annual_cumulative">{TRANSLATIONS["pt"]["annual_cumulative"]}</option>' + \
                     ''.join([f'<option value="{i}" data-translate-key="cumulative_until_month" data-month-value="{i}">{TRANSLATIONS["pt"]["cumulative_until_month"]} {i}</option>' for i in range(1, 13)])
    anos_options_html = f'<option value="Todos" data-translate-key="all_years">{TRANSLATIONS["pt"]["all_years"]}</option>' + ''.join([f'<option value="{a}">{a}</option>' for a in anos_list])
    paises_options_html = f'<option value="Todos" data-translate-key="all_countries">{TRANSLATIONS["pt"]["all_countries"]}</option>' + ''.join([f'<option value="{p}">{p}</option>' for p in paises_list])

    try:
        with open(os.path.join(project_path, 'dashboard_template.html'), 'r', encoding='utf-8') as f:
            html_template = f.read()
    except FileNotFoundError:
        print("❌ ERRO: Arquivo 'dashboard_template.html' não encontrado. Crie este arquivo com o layout do dashboard.")
        return

    html_string = html_template.format(
        **TRANSLATIONS['pt'],
        graph1_div=graph1_div,
        data_geracao=data_geracao,
        ano_min=ano_min,
        ano_max=ano_max,
        meses_options_html=meses_options_html,
        anos_options_html=anos_options_html,
        paises_options_html=paises_options_html,
        master_data_json=json.dumps(master_data),
        anos_columns_json=json.dumps([str(ano) for ano in anos_list]),
        translations_json=json.dumps(TRANSLATIONS)
    )

    dashboard_path = os.path.join(project_path, "index.html")
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(html_string)

    print(f"\n🎉 SUCESSO! O dashboard foi gerado e salvo em:\n👉 {dashboard_path}")


# ==============================================================================
    gerar_dashboard(df_fresco)

if __name__ == "__main__":
    gerar_dashboard()
    main()
