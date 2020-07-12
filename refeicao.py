#importe dos pacotes
import streamlit as st
import pandas as pd
from PIL import Image
import  time, datetime
import plotly.offline as py
import plotly.graph_objs as go
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

#carrega logo do empresa
image = Image.open('sococo-logo.png')
st.image(image,width=200 , caption='Relatório de Refeições')

#variaveis de arquivo saida
primeira_limpeza = "primeira_limpeza.txt"
segunda_limpeza = "segunda_limpeza.txt"

#busca para limpeza
search_for = '21'
search_for2 = "SOCOCO"

#recebe o arquivo de texto do usuário
uploaded_file = st.file_uploader("Selecione ou arraste seu arquivo gerado pelo TSA: ", type="txt", encoding="windows-1252")
#formata o arquivo recebido em 06 colunas
colunas = [5,11,28,12,7,7]

if uploaded_file is not None:
# se o arquivo foi carregado, le o arquivo e gera um novo arquivo formatado
    data = pd.read_fwf(uploaded_file, widths=colunas, header=None)
    data.to_csv('arquivo_sem_tratamento.txt', index=False)
    # st.write(data)

# Inicia a primeira limpeza do arquivo gerado acima.
# Gera um novo aquivo com a primeira limpeza concluida.
    with open(primeira_limpeza, 'w', encoding="windows-1252") as out_f:
        with open('arquivo_sem_tratamento.txt', "r") as in_f:
            for line in in_f:
                if search_for in line:
                    out_f.write(line)

# Inicia a segunda limpeza do arquivo gerado acima.
# Gera o arquivo final limpo
    with open(segunda_limpeza, 'w', encoding="windows-1252") as out_f:
        with open('primeira_limpeza.txt', "r", encoding="windows-1252") as in_f:
            for line in in_f:
                if search_for2 in line:
                    print('nao tem')
                else:
                  out_f.write(line)

#carrega arquivo da segunda limpeza e gera o arquivo final limpo para mostrar na tela
    df = pd.read_csv('segunda_limpeza.txt', sep=',')
    df.columns = ['Empresa', 'Matricula', 'Funcionario', 'Data', 'Hora', 'Refeicao']
    df.to_csv('arquivo_limpo.txt', index=False)

    with st.spinner('Aguarde o carregamento do arquivo...'):
        time.sleep(5)
    st.success('Concluido!')
    st.write("Shape do Dataset", df)

    #st.checkbox('Gerar Grafico')#inicio de graficos
    quantidade_cafe = sum((df['Refeicao']=='CAFE') )
    quantidade_almoco = sum((df['Refeicao']=='ALMOÇO') )
    quantidade_lanche = sum((df['Refeicao']=='LANCHE') )
    quantidade_ceia = sum((df['Refeicao']=='CEIA') )
    total = (quantidade_cafe + quantidade_almoco +
             quantidade_lanche + quantidade_ceia)

    if st.checkbox('Gerar Grafico'):
        lista_grafico = [quantidade_cafe,
                        quantidade_almoco,
                        quantidade_lanche,
                        quantidade_ceia,
                        total]



        # configure_plotly_browser_state()
        trace = go.Bar(x=['Café', 'Almoço', 'Lanche', 'Ceia', 'Total'],
                       y=lista_grafico)

        legenda = go.Layout(title='Número de Refeições',
                            xaxis={'title': 'Tipo de Refeição'},
                            yaxis={'title': 'Quantidade'}
                            )
        figura = go.Figure(data=trace, layout=legenda)
        st.write(figura)
    if st.checkbox('Filtro'):
        t = st.time_input('Set an alarm for', datetime.time(0, 0))
        st.write('Alarm is set for', t)
        hora_inicial = st.text_input('Hora inicial', '0:00')
        hora_final = st.text_input('Hora final', '22:00')

        df.loc[(df['Hora'] >= hora_inicial) & (df['Hora']<= hora_final)]



