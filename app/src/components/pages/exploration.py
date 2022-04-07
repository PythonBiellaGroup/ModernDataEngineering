import streamlit as st
from app.src.common import connect_db
from app.src.common import load_data
from app.src.common import make_plot


def app():
    
    # Hide Streamlit footer
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # set connection
    cxn = connect_db.establish_db_connection()

    df_ang_ospedali = load_data.load_ospedali(cxn)
    df_ang_clinico = load_data.load_gruppo_clinico(cxn)

    # set variable on sidebar
    anno = st.sidebar.selectbox(
        "Anno", [2012, 2013, 2014, 2015, 2016, 2017], key="exploration_anno_selectbox"
    )
    ospedale = st.sidebar.selectbox(
        "Strutture Ospedaliere",
        df_ang_ospedali["denom_struttura"].to_list(),
        key="exploration_ospedale_selectbox",
    )
    gr_clinico = st.sidebar.selectbox(
        "Gruppo Clinico",
        df_ang_clinico["DESCRIZIONE_ACC_DI_DIAGNOSI"].to_list(),
        key="exploration_gr_clinico_selectbox",
    )

    # get cod from description chosen by the user

    cod_ospedale = load_data.get_cod_ospedale(df_ang_ospedali, ospedale)
    cod_clinico = load_data.get_cod_gruppo_clinico(df_ang_clinico, gr_clinico)

    # load dataframe
    df_performance_ospedali = load_data.load_performance_ospedali(cod_ospedale, cxn)
    df_acc_clinico = load_data.load_clinico(anno, cod_ospedale, cod_clinico, cxn)
    df_reparto_clinico = load_data.load_occupazione_repato_clinico(
        anno, cod_ospedale, cod_clinico, cxn
    )

    # app structure

    st.title("Overview performance ospedaliera e ripartizione per gruppo clinico")

    st.plotly_chart(
        make_plot.plt_performance_ospdeli(df_performance_ospedali),
        use_container_width=True,
    )

    st.plotly_chart(
        make_plot.plt_sankey_acc_clinica(df_acc_clinico), use_container_width=True
    )

    st.plotly_chart(
        make_plot.plt_bar_reparti(df_reparto_clinico), use_container_width=True
    )
