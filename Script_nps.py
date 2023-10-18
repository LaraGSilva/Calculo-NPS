import pandas as pd

# Lê o arquivo CSV
df = pd.read_csv('base_nps.csv')

# Transforma em objeto
df['data'] = pd.to_datetime(df['data_com_horario']).dt.date
df['hora'] = pd.to_datetime(df['data_com_horario']).dt.time

# Cria uma coluna para o horário
df['horario'] = pd.to_datetime(df['data_com_horario'].dt.strftime('%H:%M'))

# Filtragem por horário
df['hora'] = pd.to_datetime(df['hora'])
df = df[(df['hora'] >= pd.to_datetime('8:55').time()) & (df['hora'] <= pd.to_datetime('18:30').time())]

# Remove valores nulos de agentes, filas e origem
df = df.dropna(subset=["agente", "filas", "origem"])

# Categoriza as notas
def categoriza_nps(nota):
    if nota <= 6:
        return 'detratora'
    elif nota <= 8:
        return 'neutra'
    else:
        return 'promotora'

# Nova coluna que categoriza o NPS
df['categoria_nps'] = df['nota'].apply(categoriza_nps)

# Salva a base tratada
df.to_csv('base_nps_tratada.csv', index=False)

# Carrega a base de dados tratada
df = pd.read_csv('base_nps_tratada.csv')

# Carrega a segunda planilha com informações de filas e superintendências
df_sup_filas = pd.read_csv('sup_filas.csv')

# Realize o cruzamento das informações com base na coluna 'fila'
df = df.merge(df_sup_filas, on='fila', how='left')

# Salva a base cruzada
df.to_csv('base_nps_com_superintendencia.csv', index=False)

# Função para calcular o NPS
def calcula_nps(dataframe):
    valid_responses = dataframe[(dataframe['nota'] >= 0) & (dataframe['nota'] <= 10)]
    detratores = len(valid_responses[valid_responses['nota'] <= 6])
    neutros = len(valid_responses[(valid_responses['nota'] == 7) | (valid_responses['nota'] == 8)])
    promotores = len(valid_responses[valid_responses['nota'] >= 9])
    nps = (promotores - detratores) / len(valid_responses) * 100
    return nps

# Chama a função com o DataFrame tratado
nps_result = calcula_nps(df)

# Imprime o resultado do NPS
print(f"Net Promoter Score (NPS) calculado: {nps_result:.2f}%")








