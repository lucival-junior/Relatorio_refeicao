#importe dos pacotes
import streamlit as st
import pandas as pd
from PIL import Image
import  time, datetime
import base64
import plotly.offline as py
import plotly.graph_objs as go
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

#carrega logo do empresa
image = Image.open('logo-grupo-sococo.png')
st.image(image,width=700 , caption='Relatório de Refeições')

#variaveis de arquivo saida
primeira_limpeza = "primeira_limpeza.txt"
segunda_limpeza = "segunda_limpeza.txt"

#busca para limpeza
search_for = '21'
search_for2 = "SOCOCO"

#recebe o arquivo de texto do usuário
uploaded_file = st.file_uploader("Selecione ou arraste seu arquivo gerado pelo TSA: ",
                                 type="txt", encoding="windows-1252")
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
                    pass
                else:
                  out_f.write(line)

#carrega arquivo da segunda limpeza e gera o arquivo final limpo para mostrar na tela
    df = pd.read_csv('segunda_limpeza.txt', sep=',')
    df.columns = ['Empresa', 'Matricula', 'Funcionario', 'Data', 'Hora', 'Refeicao']
    df.to_csv('arquivo_limpo.txt', index=False)

    with st.spinner('Aguarde o carregamento do arquivo...'):
        time.sleep(5)
    #st.success('Concluido!')
    #st.write(df)
    #st.write("Linha / Colunas: ", df.shape)


    if st.checkbox('Desconto por Funcionário'):
        #hora_inicial = st.sidebar.text_input('Hora inicial', '06:00')
        #hora_final = st.sidebar.text_input('Hora final', '08:00')

        #filtro_hora = df.loc[(df['Hora'] >= hora_inicial) & (df['Hora']<= hora_final)]
        #st.write(filtro_hora)
        #st.write("Linha / Colunas: ",filtro_hora.shape)

        #inicio de novo tratamento e criacao de novas colunas

        #trasnformar categoria REFEICAO para fator (ALMOÇO - 0/1	CAFE- 0/1	CEIA- 0/1	JANTAR- 0/1	LANCHE- 0/1)
        filtro_ref = pd.get_dummies(df['Refeicao'])
        #concatena df inicial com novas colunas geradas pelo fator
        novo_df = pd.concat([df, filtro_ref], axis=1, sort=False)

        #remove as colunas (Empresa , Hora , Refeicao) para melhor visualizacao
        novo_df2 = novo_df.drop(columns=['Empresa','Hora','Refeicao'])

        # criar indice para agrupar refeicoes por dia
        # 'estilo' contador para adiconar preco diferente
        mat_dia = novo_df2.groupby(['Matricula','Funcionario','Data']).sum()

        #adiciona novas colunas para visualização
        mat_dia['VALOR_FUN'] = 0
        mat_dia['VALOR_INT'] = 0
        mat_dia['DESCONTAR'] = 0

#----------------------------------------------------------#
        #calculo valor pago pelo almoco
        def almoco(alm):
          if alm['ALMOÇO'] == 1:
            return 1.77
          elif 0 != alm['ALMOÇO'] > 1:
            return (alm['ALMOÇO'] * 8.85) - 7.08
          else:
            return 0

        calculo_almoco = mat_dia.apply(almoco, axis=1)

        #calculo valor pago pelo Café
        def cafe(caf):
          if caf['CAFE'] == 1:
            return 0.68
          elif 0 != caf['CAFE'] > 1:
            return (caf['CAFE'] * 3.41) - 2.73
          else:
            return 0
        calculo_cafe = mat_dia.apply(cafe, axis=1)

        #calculo valor pago pelo Ceia
        def ceia(cei):
          if cei['CEIA'] == 1:
            return 1.77
          elif 0 != cei['CEIA'] > 1:
            return (cei['CEIA'] * 8.85) - 7.08
          else:
            return 0
        calculo_ceia = mat_dia.apply(ceia, axis=1)

        #calculo valor pago pelo Jantar
        def jantar(jan):
          if jan['JANTAR'] == 1:
            return 1.77
          elif 0 != jan['JANTAR'] > 1:
            return (jan['JANTAR'] * 8.85) - 7.08
          else:
            return 0
        calculo_janta = mat_dia.apply(jantar, axis=1)

        #calculo valor pago pelo Lanche
        def lanche(lan):
          if lan['LANCHE'] == 1:
            return 0.68
          elif 0 != lan['LANCHE'] > 1:
            return (lan['LANCHE'] * 3.41) - 2.73
          else:
            return 0
        calculo_lanche = mat_dia.apply(lanche, axis=1)


        mat_dia['DESCONTAR'] = calculo_almoco + calculo_cafe + calculo_ceia + calculo_janta + calculo_lanche
        st.markdown('Refeições por funcionário')
        st.write(mat_dia)
        st.write("Linha / Colunas: ", mat_dia.shape)
        #salva o arquivo em formato de texto com os INDÍCES para download
        mat_dia.to_csv('relatorio_refeicoes.txt')

        #funcao para gerar downlod da data frame tratado
        def download_link(object_to_download, download_filename, download_link_text):

            if isinstance(object_to_download, pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=True)
                b64 = base64.b64encode(object_to_download.encode()).decode()
                return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

        if st.button('Download'):
            tmp_download_link = download_link(mat_dia, 'relatorio_refeicoes.txt', 'Clique para salvar o arquivo')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

#----------------------------------------------------------#
        #Gráfico numero de refeicoes
    if st.checkbox('Quantidade de Refeições'):
        quantidade_cafe = sum((df['Refeicao']=='CAFE') )
        quantidade_almoco = sum((df['Refeicao']=='ALMOÇO') )
        quantidade_lanche = sum((df['Refeicao']=='LANCHE') )
        quantidade_janta = sum((df['Refeicao']=='JANTAR') )
        quantidade_ceia = sum((df['Refeicao']=='CEIA') )

        lista_grafico = [quantidade_cafe, quantidade_almoco,
                        quantidade_lanche, quantidade_janta,
                        quantidade_ceia]

        #verificar para melhorar esse codigo
        total_ref_periodo = (quantidade_cafe + quantidade_almoco +
                            quantidade_lanche + quantidade_janta +
                             quantidade_ceia)

        # configure_plotly_browser_state()
        trace = go.Bar(x=['Café', 'Almoço', 'Lanche', 'Janta','Ceia'],
                       y=lista_grafico)

        legenda = go.Layout(title='Quantidade de refeições por tipo',
                            xaxis={'title': 'Tipo de Refeição'},
                            yaxis={'title': 'Quantidade'}
                            )
        figura = go.Figure(data=trace, layout=legenda)
        st.write(figura)

