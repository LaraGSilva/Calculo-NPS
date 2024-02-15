import pandas as pd

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return None

def preprocess_data(df):
    df['data'] = pd.to_datetime(df['data_com_horario']).dt.date
    df['hora'] = pd.to_datetime(df['data_com_horario']).dt.time
    df['horario'] = pd.to_datetime(df['data_com_horario'].dt.strftime('%H:%M'))
    df['hora'] = pd.to_datetime(df['hora'])
    df = df[(df['hora'] >= pd.to_datetime('8:55').time()) & (df['hora'] <= pd.to_datetime('18:30').time())]
    df = df.dropna(subset=["agente", "filas", "origem"])
    df['categoria_nps'] = df['nota'].apply(categorize_nps)
    return df

def categorize_nps(nota):
    if nota <= 6:
        return 'detratora'
    elif nota <= 8:
        return 'neutra'
    else:
        return 'promotora'

def merge_data(df_main, df_sup_filas):
    df_main = df_main.merge(df_sup_filas, on='fila', how='left')
    return df_main

def calculate_nps(dataframe):
    valid_responses = dataframe[(dataframe['nota'] >= 0) & (dataframe['nota'] <= 10)]
    detractors = len(valid_responses[valid_responses['nota'] <= 6])
    neutrals = len(valid_responses[(valid_responses['nota'] == 7) | (valid_responses['nota'] == 8)])
    promoters = len(valid_responses[valid_responses['nota'] >= 9])
    nps = (promoters - detractors) / len(valid_responses) * 100
    return nps

def main():
    # Carregar dados
    df = load_data('base_nps.csv')
    df_sup_filas = load_data('sup_filas.csv')

    if df is not None and df_sup_filas is not None:
        # Pré-processamento de dados
        df = preprocess_data(df)

        # Mesclar dados
        df = merge_data(df, df_sup_filas)

        # Calcular NPS
        nps_result = calculate_nps(df)

        # Imprimir resultado do NPS
        print(f"Net Promoter Score (NPS) calculado: {nps_result:.2f}%")









