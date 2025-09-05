import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Importa o arquivo de exames medicos 
df = pd.read_csv('medical_examination.csv')

# Faz o calculo do IMC e calculo se a pessoa esta ou não acima do peso 
df['IMC'] = df['weight'] / (df['height'] / 100)**2   #Cria uma nova coluna e realiza o calculo do IMC
df['overweight'] = (df['IMC'] > 25).astype(int)     #define que o IMC acima de 25 é considerado acima do peso

# Normaliza os valores de colesterol e glicose para 0 (Bom) ou 1 (Ruim)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int) 
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4
def draw_cat_plot(df):
    # O .melt() transforma decompõe as colunas em linhas
    df_cat = pd.melt(df, id_vars = ['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Gera uma nova coluna mostrando a quantidade de 0 ou 1 existem para cada variavel
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size()
    df_cat = df_cat.rename(columns={'size': 'total'})

    #cria e armazena o grafico na variavel "fig"                           
    fig = sns.catplot(data=df_cat, x = "variable", y="total", hue="value", col="cardio", kind="bar").fig

    # salva o grafico como "catplot.png"
    fig.savefig('catplot.png')
    return fig

# Função do mapa de calor
def draw_heat_map():
    # Filtra os dados removendo informações incorretas
    df_heat = df_heat[
    (df_heat['ap_lo'] <= df_heat['ap_hi']) &
    (df_heat['height'] >= df_heat['height'].quantile(0.025)) &
    (df_heat['height'] <= df_heat['height'].quantile(0.975)) &
    (df_heat['weight'] >= df_heat['weight'].quantile(0.025)) &
    (df_heat['weight'] <= df_heat['weight'].quantile(0.975))]

    # Calcula a correlation matriz de df_heat
    corr = df_heat.corr()

    # Cria uma mascara para o triangulo superior da matriz
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Define as dimensões do mapa de calor
    fig, ax = plt.subplots(figsize=(12, 10))

    # Paramentros do mapa de calor
    sns.heatmap(corr,   #Correlation matriz
        mask=mask,      #Mascara do triangulo superior 
        annot=True,      #Mostra os valores dentro das celulas do heatmap
        cmap="coolwarm",        #Paleta de cores utilizada
        vmin=-1,        #Define o valor minimo do mapa
        vmax=1,         #Define o valor maximo do mapa
        linewidths=0.5,
        square=True,        #Deixa as celulas quadradas
        cbar_kws={"shrink": 0.5}
    )

    # Salva o heatmap
    fig.savefig('heatmap.png')
    return fig
