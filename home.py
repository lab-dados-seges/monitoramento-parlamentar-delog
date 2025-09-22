import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Monitoramento de PLs", layout="wide")
st.title("Monitoramento de Projetos de Lei - DELOG")

RAW_URL = "https://raw.githubusercontent.com/lab-dados-seges/monitoramento-parlamentar-delog/main/data/df_final.csv"

@st.cache_data(ttl=60*15)  # 15 min
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    # normalização leve
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df_final = load_data(RAW_URL)
except Exception as e:
    st.error(f"Falha ao carregar o CSV: {e}")
    st.stop()

# Busca por número do PL (case-insensitive)
busca = st.text_input("Buscar por número do PL (ex.: 1234/2025)")

df_view = df_final.copy()
if busca:
    b = busca.strip()
    # tente colunas típicas; ajuste conforme seu CSV
    cand_cols = [c for c in df_view.columns if "pl" in c.lower() or "projeto" in c.lower() or "processo" in c.lower()]
    if cand_cols:
        mask = False
        for c in cand_cols:
            mask = mask | df_view[c].astype(str).str.contains(b, case=False, na=False)
        df_view = df_view[mask]

# Links clicáveis (se tiver colunas de URL)
link_cols = [
    "Link Inteiro Teor Parecer",
    "Link Inteiro Teor do PL",
    "Link Ficha de Tramitação",
]
for col in link_cols:
    if col in df_view.columns:
        df_view[col] = df_view[col].apply(
            lambda x: f'<a href="{x}" target="_blank">Clique aqui</a>' if isinstance(x, str) and x.startswith("http") else ""
        )

st.markdown("### Resultado")
st.write(df_view.to_html(escape=False, index=False), unsafe_allow_html=True)