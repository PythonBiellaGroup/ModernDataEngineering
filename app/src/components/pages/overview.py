import streamlit as st
from streamlit_folium import folium_static
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

    # load dataframe
    df_popolazione = load_data.load_demo_data(cxn)
    df_tipo_livello_emergenza = load_data.load_livello_emergenza(cxn)
    df_tipo_strutture = load_data.load_tipo_strutture(cxn)
    df_mortalita = load_data.load_mortalita(cxn)
    df_local_strutture = load_data.load_strutture_geo(cxn)
    df_province = load_data.load_provincie(cxn)

    # set variable on sidebar
    anno = st.sidebar.selectbox("Anno", [2012, 2013, 2014, 2015, 2016, 2017])
    provincia = st.sidebar.selectbox("Provincia", df_province["PROVINCIA"].to_list())

    # app structure

    st.title("Overview generale ospedali regione Lombardia")

    with st.container():
        st.plotly_chart(
            make_plot.plt_bar_tipo_strutture(df_tipo_strutture),
            use_container_width=True,
        )
        st.plotly_chart(
            make_plot.plt_pie_livello_emerg(df_tipo_livello_emergenza),
            use_container_width=True,
        )
    with st.container():
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(
                make_plot.plt_bar_demo(df_popolazione, anno, provincia),
                use_container_width=True,
            )
        with col4:
            st.plotly_chart(
                make_plot.plt_num_mortalita(df_mortalita, anno, provincia),
                use_container_width=True,
            )
        with st.container():
            folium_static(make_plot.plt_map_hospital(df_local_strutture))
