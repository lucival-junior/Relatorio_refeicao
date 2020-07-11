#importe dos pacotes
import streamlit as st
import pandas as pd
from PIL import Image

#carrega logo do empresa
image = Image.open('sococo-logo.png')
st.sidebar.image(image,width=200 , caption='Relatório de Refeições', use_column_width=True)

# Add a checkbox to the sidebar:
cafe = st.sidebar.checkbox('Café')
almoco = st.sidebar.checkbox('Almoco')
lanche = st.sidebar.checkbox('Lanche')
ceia = st.sidebar.checkbox('Ceia')

#variaveis de arquivo saida
out_file = "primeira_limpeza.txt"
out_file2 = "segunda_limpeza.txt"

#busca para limpeza
search_for = "21"
search_for2 = "Estabelecimento:"

#recebe o arquivo de texto e formata em 06 colunas
uploaded_file = st.file_uploader("Escolha seu arquivo: ", type="txt", encoding="windows-1252")
colunas = [5,11,28,12,7,7]

if uploaded_file is not None:
# se o arquivo foi carregado, le o arquivo e gera um novo arquivo formatado
    data = pd.read_fwf(uploaded_file, widths=colunas, header=None)
    data.to_csv('arquivo_sem_tratamento.txt', index=False)
    # st.write(data)

# Inicia a primeira limpeza do arquivo gerado acima.
# Gera um novo aquivo com a primeira limpeza concluida.
    with open(out_file, 'w', encoding="windows-1252") as out_f:
        with open('arquivo_sem_tratamento.txt', "r") as in_f:
            for line in in_f:
                if search_for in line:
                    out_f.write(line)

# Inicia a segunda limpeza do arquivo gerado acima.
# Gera o arquivo final limpo
    with open(out_file2, 'w', encoding="windows-1252") as out_f:
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
    st.write("Shape do Dataset", df)
