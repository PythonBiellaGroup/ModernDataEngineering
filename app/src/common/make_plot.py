import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium


def plt_bar_demo(df, anno, provincia):
    fig = px.bar(
        df[(df.ANNO == anno) & (df.PROVINCIA == provincia)],
        x="FASCIA_ETA",
        y="POPOLAZIONE",
        color="GENERE",
        title="Distribuzione popolazione per fasce d'età",
    )
    return fig


def plt_pie_livello_emerg(df):
    fig = px.pie(
        df,
        values="CONTEGGIO",
        names="LIVELLO_EMERGENZA",
        title="Tipologia livello di emergenza gestito dalle strutture",
    )
    return fig


def plt_bar_tipo_strutture(df):
    fig = px.bar(
        df,
        x="CONTEGGIO",
        y="TIPO_STRUTTURA",
        title="Tipologia di strutture ospedaliere presenti in Lombardia",
    )
    return fig


def plt_num_mortalita(df, anno, provincia):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=df[(df.ANNO == anno) & (df.PROVINCIA == provincia)].iloc[0][
                "SPERANZA_VITA_NASCITA"
            ],
            title="Speranza di vita alla nascita",
            domain={"row": 0, "column": 0},
            gauge={"axis": {"visible": True}},
        )
    )
    fig.add_trace(
        go.Indicator(
            value=df[(df.ANNO == anno) & (df.PROVINCIA == provincia)].iloc[0][
                "TASSO_MORTALITA"
            ],
            title="Tasso di mortalità",
            domain={"row": 1, "column": 0},
            gauge={"axis": {"visible": True}},
        )
    )
    fig.update_layout(grid={"rows": 2, "columns": 1, "pattern": "independent"})
    return fig


def plt_map_hospital(df):

    mappa = folium.Map(
        location=[45.464664, 9.188540],
        zoom_start=7.5,
        position="central",
        tiles="CartoDB positron",
    )

    # insert marker for all hospital in Lombardy

    for row in df.index:
        folium.Marker(
            location=[df["COORDINATA_X"][row], df["COORDINATA_Y"][row]],
            tooltip=[df["DENOM_STRUTTURA"][row], df["DENOM_ENTE"][row]],
            icon=folium.Icon(color="red", icon="plus"),
        ).add_to(mappa)
    # draw boundaries
    json_boundaries = r"./app/static/province_lombardia.geojson"
    folium.GeoJson(json_boundaries, overlay=True).add_to(mappa)
    return mappa


def plt_bar_reparti(df):
    fig = px.bar(
        df,
        x="descrizione_disciplina",
        y="totale_ricoveri",
        color="descrizione_disciplina",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Ripartizione per reparto",
    )
    return fig


def plt_performance_ospdeli(df):
    perf_plot = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Trasferimenti tra strutture",
            "Tasso dimissioni volontarie",
            "Tasso ritorni in sala operatoria",
            "Tasso ricoveri ripetuti",
        ),
    )

    perf_plot.add_trace(
        go.Scatter(
            x=df["ANNO"],
            y=df["NUM_TRASFERIMENTI_FRA_STRUTTURE"],
            hoverinfo="none",
            mode="lines+markers",
            line_color="#f0f921",
            name="Tasso trasferimenti tra strutture",
        ),
        row=1,
        col=1,
    )

    perf_plot.add_trace(
        go.Scatter(
            x=df["ANNO"],
            y=df["MEDIA_TRASFERIMENTI_FRA_STRUTTURE"],
            mode="lines+markers",
            line_color="firebrick",
            name="Media trasferimenti tra strutture",
        ),
        row=1,
        col=1,
    )

    perf_plot.add_trace(
        go.Scatter(
            x=df["ANNO"],
            y=df["TASSO_DIMISSIONI_VOLONTARIE"],
            mode="lines+markers",
            line_color="#ed7953",
            name="Tasso dimissioni volontarie",
        ),
        row=1,
        col=2,
    )

    perf_plot.add_trace(
        go.Scatter(
            x=df["ANNO"],
            y=df["MEDIA_DIMISSIONI_VOLONTARIE"],
            mode="lines+markers",
            line_color="firebrick",
            name="Media dimissioni volontarie",
        ),
        row=1,
        col=2,
    )

    perf_plot.add_trace(
        go.Scatter(
            x=df["ANNO"],
            y=df["TASSO_RITORNI_IN_SALA_OPERATORIA"],
            mode="lines+markers",
            line_color="#7201a8",
            name="Tasso ritorni in sala operatoria",
        ),
        row=2,
        col=1,
    )

    perf_plot.add_trace(
        go.Scatter(
            x=df["ANNO"],
            y=df["MEDIA_RITORNI_SALA_OPERATORIA"],
            mode="lines+markers",
            line_color="firebrick",
            name="Media ritorni in sala operatoria",
        ),
        row=2,
        col=1,
    )

    perf_plot.add_trace(
        go.Scatter(
            x=df["ANNO"],
            y=df["TASSO_INEFFICACIA_CURE"],
            mode="lines+markers",
            line_color="#0d0887",
            name="Tasso ricoveri ripetuti",
        ),
        row=2,
        col=2,
    )

    perf_plot.add_trace(
        go.Scatter(
            x=df["ANNO"],
            y=df["MEDIA_INEFFICACIA_CURE"],
            mode="lines+markers",
            line_color="firebrick",
            name="Media ricoveri ripetuti",
        ),
        row=2,
        col=2,
    )
    return perf_plot


def plt_sankey_acc_clinica(df):
    source = []
    target = []
    label = (
        df["descrizione_acc_di_diagnosi"].unique().tolist()
        + df.descrizione_drg.tolist()
    )
    for x in range(0, df.shape[0]):
        source.append(0)
    value = df.totale_ricoveri.tolist()
    label = (
        df["descrizione_acc_di_diagnosi"].unique().tolist()
        + df.descrizione_drg.tolist()
    )
    target.extend(range(1, df.shape[0] + 1))

    # data to dict, dict to sankey
    link = dict(source=source, target=target, value=value)
    node = dict(label=label, pad=50, thickness=5)
    data = go.Sankey(link=link, node=node)

    # plot
    fig = go.Figure(data)
    fig.update_layout(
        hovermode="x", title="Ripartizione delle diagnosi per categoria clinica"
    )
    return fig
