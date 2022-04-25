import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

from urllib.error import URLError

st.set_page_config(
    page_title="Scora Connection", page_icon="📊", initial_sidebar_state="expanded"
)

st.write(
    """
# 📊 Scora Connection
"""
)


@st.cache
def read_file_or_path(url):
    return pd.read_csv(url)


def render_graph(path_url, width=700, height=465, path_file='./html_files'):
    df = pd.read_csv(path_url)
    start_tables = st.multiselect(
        "Escolha as tabelas do início da conexão", list(df.start_table))
    end_tables = st.multiselect(
        "Escolha as tabelas do final da conexão", list(df.end_table))

    graph = Network(width="100%",
                    bgcolor='#222222', font_color='white')

    for start, connection, end in zip(df.start_table.to_list(), df.connection.to_list(), df.end_table.to_list()):
        if len(start_tables) and start not in start_tables:
            continue
        if len(end_tables) and end not in end_tables:
            continue
        graph.add_node(start, title=start, size=10, physics=True)
        graph.add_node(end, title=end, size=10, physics=True)
        graph.add_edge(start, end, label=connection, physics=False)
        graph.inherit_edge_colors(True)

    graph.save_graph(f'{path_file}/pyvis_graph.html')
    HtmlFile = open(f'{path_file}/pyvis_graph.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), width=width, height=height)


try:
    uploaded_file = st.file_uploader("Upload CSV", type=".csv")

    if uploaded_file:
        render_graph(uploaded_file)
except URLError as e:
    st.error(
        """
      **This demo requires internet access.**

      Connection error: %s
  """
        % e.reason
    )
