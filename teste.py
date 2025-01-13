import streamlit as st

teste_num = st.number_input("Teste Número:", value=3, min_value=1)
st.write(f"Valor: {teste_num}, Tipo: {type(teste_num)}")