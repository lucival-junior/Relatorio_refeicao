import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np

image = Image.open('sococo-logo.png')
st.sidebar.image(image,width=250 , caption='Relatório de Refeições', use_column_width=True)

# Add a checkbox to the sidebar:
cafe = st.sidebar.checkbox('Café')
almoco = st.sidebar.checkbox('Almoco')
lanche = st.sidebar.checkbox('Lanche')
ceia = st.sidebar.checkbox('Ceia')

st.sidebar.date_input('Data')

if cafe:
    number = st.number_input('Insert a number')
    st.write('The current number is ', number)


out_file = "modelo1.txt"
out_file2 = "saida.txt"
search_for = "21"
search_for2 = "Estabelecimento:"

uploaded_file2 = st.file_uploader("Choose a CSV file", type="txt", encoding="cp1252")
if uploaded_file2 is not None:
 colunas = [5,11,28,12,7,7]
 data = pd.read_fwf(uploaded_file2, widths=colunas, header=None)
 data.to_csv('novo.txt', index=False)
 st.write(data)

uploaded_file = st.file_uploader("Escolha seu arquivo: ", type="txt", encoding="windows-1252")
if uploaded_file is not None:
    with open(out_file, 'w', encoding="windows-1252") as out_f:
        with open('novo.txt', "r") as in_f:
            for line in in_f:
                if search_for in line:
                    out_f.write(line)

    with open(out_file2, 'w', encoding="windows-1252") as out_f:
        with open('modelo1.txt', "r", encoding="windows-1252") as in_f:
            for line in in_f:
                if search_for2 in line:
                    print('nao tem')
                else:
                  out_f.write(line)

    df = pd.read_csv('saida.txt', sep=',')
    df.columns = ['Empresa', 'Matricula', 'Funcionario', 'Data', 'Hora', 'Refeicao']
    df.to_csv('modelagem.txt', index=False)
    st.write("Shape do Dataset", df)
