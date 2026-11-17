
import streamlit as st
from datetime import date

from database.banco import (
    criar_tabela,
    adicionar_alimento,
    listar_alimentos,
    excluir_alimento,
    atualizar_alimento
)

st.set_page_config(
    page_title="Minha Geladeira | AproveitAI",
    page_icon="🥬",
    layout="wide"
)

# Inicializa o banco
criar_tabela()

st.title("🥬 Minha Geladeira")
st.write("Cadastre e acompanhe os alimentos disponíveis em sua casa.")

st.divider()

# Cadastro de alimentos
st.subheader("Adicionar alimento")

with st.form("form_alimento", clear_on_submit=True):

    nome = st.text_input("Nome do alimento")

    col1, col2 = st.columns(2)

    with col1:
        quantidade = st.number_input(
            "Quantidade",
            min_value=0.1,
            value=1.0,
            step=0.5
        )

    with col2:
        unidade = st.selectbox(
            "Unidade",
            ["unidade(s)", "kg", "g", "litro(s)", "ml", "pacote(s)"]
        )

    tem_validade = st.checkbox("Informar data de validade")

    validade = st.date_input(
        "Data de validade",
        value=date.today()
    )

    cadastrar = st.form_submit_button(
        "Adicionar alimento",
        use_container_width=True
    )

    if cadastrar:

        if not nome.strip():
            st.error("Informe o nome do alimento.")

        else:
            data_validade = (
                validade.isoformat() if tem_validade else None
            )

            adicionar_alimento(
                nome.strip(),
                quantidade,
                unidade,
                data_validade
            )

            st.success("Alimento cadastrado com sucesso!")
            st.rerun()


st.divider()

# Listagem de alimentos
st.subheader("Alimentos cadastrados")

alimentos = listar_alimentos()

if not alimentos:

    st.info("Sua geladeira ainda está vazia. Cadastre seu primeiro alimento!")

else:

    for alimento in alimentos:

        with st.container(border=True):

            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.markdown(f"**{alimento['nome']}**")

            with col2:
                st.write(
                    f"{alimento['quantidade']} "
                    f"{alimento['unidade']}"
                )

            with col3:

                if alimento["validade"]:
                    st.write(f"Validade: {alimento['validade']}")

                    data = date.fromisoformat(alimento["validade"])

                    if data < date.today():
                        st.error("Validade vencida")

                    elif (data - date.today()).days <= 3:
                        st.warning("Próximo do vencimento")

                else:
                    st.write("Sem validade informada")

    st.divider()

    # Edição e exclusão
    st.subheader("Gerenciar alimentos")

    opcoes = {
        f"{a['nome']} (ID {a['id']})": a
        for a in alimentos
    }

    selecionado = st.selectbox(
        "Selecione um alimento",
        list(opcoes.keys())
    )

    alimento = opcoes[selecionado]

    with st.form("editar_alimento"):

        novo_nome = st.text_input(
            "Nome",
            value=alimento["nome"]
        )

        nova_quantidade = st.number_input(
            "Quantidade",
            min_value=0.1,
            value=float(alimento["quantidade"])
        )

        unidades = [
            "unidade(s)", "kg", "g",
            "litro(s)", "ml", "pacote(s)"
        ]

        indice = (
            unidades.index(alimento["unidade"])
            if alimento["unidade"] in unidades
            else 0
        )

        nova_unidade = st.selectbox(
            "Unidade",
            unidades,
            index=indice
        )

        possui_validade = st.checkbox(
            "Informar validade",
            value=bool(alimento["validade"])
        )

        nova_validade = st.date_input(
            "Nova validade",
            value=(
                date.fromisoformat(alimento["validade"])
                if alimento["validade"]
                else date.today()
            )
        )

        salvar = st.form_submit_button("Salvar alterações")

        if salvar:

            if not novo_nome.strip():
                st.error("Informe o nome do alimento.")

            else:
                data = (
                    nova_validade.isoformat()
                    if possui_validade else None
                )

                atualizar_alimento(
                    alimento["id"],
                    novo_nome.strip(),
                    nova_quantidade,
                    nova_unidade,
                    data
                )

                st.success("Alimento atualizado!")
                st.rerun()

    if st.button("🗑️ Excluir alimento", type="secondary"):

        excluir_alimento(alimento["id"])

        st.success("Alimento excluído!")
        st.rerun()
