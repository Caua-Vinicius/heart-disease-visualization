import streamlit as st
import pandas as pd
import plotly.express as px

file_path = "heart.csv"
df = pd.read_csv(file_path)

st.set_page_config(page_title="Análise Dinâmica de Doenças Cardíacas", layout="wide")
st.title("📊 Análise Dinâmica de Fatores Relacionados a Doenças Cardíacas")

st.sidebar.header("Filtros Interativos")
idade_min, idade_max = st.sidebar.slider("Faixa Etária", int(df.age.min()), int(df.age.max()), (40, 60))
sexo = st.sidebar.radio("Sexo", options=["Todos", "Masculino", "Feminino"])
tipo_dor = st.sidebar.multiselect("Tipo de Dor no Peito", options=df.cp.unique(), default=df.cp.unique())

df_filtered = df[(df["age"].between(idade_min, idade_max)) & (df["cp"].isin(tipo_dor))]
if sexo == "Masculino":
    df_filtered = df_filtered[df_filtered["sex"] == 1]
elif sexo == "Feminino":
    df_filtered = df_filtered[df_filtered["sex"] == 0]

st.markdown("### 🔍 Resumo dos Dados Filtrados")
st.write(f"📌 {df_filtered.shape[0]} registros selecionados em tempo real")

col1, col2 = st.columns(2)

if len(df_filtered["sex"].unique()) > 1:
    df_fbs = df_filtered.groupby(["sex", "fbs", "target"]).size().reset_index(name="count")
    anim_frame_fbs = "sex"
else:
    df_fbs = df_filtered.groupby(["fbs", "target"]).size().reset_index(name="count")
    anim_frame_fbs = None

with col1:
    st.markdown("## 🍬 Açúcar no Sangue em Jejum vs. Doença Cardíaca")
    fig_fbs = px.bar(
        df_fbs,
        x="fbs",
        y="count",
        color="target",
        barmode="group",
        labels={
            "fbs": "Fasting Blood Sugar (>120 mg/dl)",
            "target": "Heart Disease (0=No, 1=Yes)",
            "count": "Contagem"
        },
        title="Relação Dinâmica entre Açúcar no Sangue e Doença Cardíaca",
        animation_frame=anim_frame_fbs,
        height=400
    )
    fig_fbs.update_xaxes(tickvals=[0, 1], ticktext=["Não (>120 mg/dl)", "Sim (≤120 mg/dl)"])
    fig_fbs.update_layout(hovermode="x unified")
    st.plotly_chart(fig_fbs, use_container_width=True)
    st.info("""
    🧐 *Interpretação*:  
    - Gráfico de barras dinâmico mostrando a contagem de pacientes por nível de açúcar no sangue.  
    - Passe o mouse sobre as barras para ver detalhes; clique e arraste para zoom.  
    - Se houver animação por sexo, observe como o padrão muda entre masculino e feminino.  
    - Insight: Proporções altas de 'Sim' com doença (1) sugerem risco associado a açúcar elevado.  
    """)

if len(df_filtered["sex"].unique()) > 1:
    df_restecg = df_filtered.groupby(["sex", "restecg", "target"]).size().reset_index(name="count")
    anim_frame_restecg = "sex"
else:
    df_restecg = df_filtered.groupby(["restecg", "target"]).size().reset_index(name="count")
    anim_frame_restecg = None

with col2:
    st.markdown("## 📈 Resultados de ECG em Repouso vs. Doença Cardíaca")
    fig_restecg = px.bar(
        df_restecg,
        x="restecg",
        y="count",
        color="target",
        barmode="group",
        labels={
            "restecg": "Resting ECG Results",
            "target": "Heart Disease (0=No, 1=Yes)",
            "count": "Contagem"
        },
        title="Relação Dinâmica entre ECG em Repouso e Doença Cardíaca",
        animation_frame=anim_frame_restecg,
        height=400
    )
    fig_restecg.update_xaxes(tickvals=[0, 1, 2], ticktext=["Normal", "Anormalidade ST-T", "Hipertrofia"])
    fig_restecg.update_layout(hovermode="x unified")
    st.plotly_chart(fig_restecg, use_container_width=True)
    st.info("""
    🧐 *Interpretação*:  
    - Barras dinâmicas para resultados de ECG em repouso (0 = normal, 1 = ST-T, 2 = hipertrofia).  
    - Passe o mouse para detalhes; use os botões para explorar (zoom, pan, etc.).  
    - Animação por sexo (se disponível) mostra diferenças entre gêneros.  
    - Insight: Mais casos de doença em 'Anormalidade ST-T' ou 'Hipertrofia' indicam risco.  
    """)

col3, col4 = st.columns(2)

with col3:
    st.markdown("## 💓 Distribuição Dinâmica de Oldpeak")
    fig_oldpeak = px.box(
        df_filtered,
        x="target",
        y="oldpeak",
        color="target",
        labels={
            "target": "Heart Disease (0=No, 1=Yes)",
            "oldpeak": "ST Depression Induced by Exercise"
        },
        title="Distribuição Dinâmica de Oldpeak por Status de Doença",
        animation_frame="sex" if len(df_filtered["sex"].unique()) > 1 else None,
        height=400
    )
    fig_oldpeak.update_xaxes(tickvals=[0, 1], ticktext=["Sem Doença", "Com Doença"])
    fig_oldpeak.update_layout(hovermode="closest")
    st.plotly_chart(fig_oldpeak, use_container_width=True)
    st.info("""
    🧐 *Interpretação*:  
    - Box plot dinâmico comparando depressão ST entre pacientes com e sem doença.  
    - Passe o mouse sobre os pontos para ver valores individuais; use zoom para detalhes.  
    - Animação por sexo (se disponível) destaca diferenças de gênero.  
    - Insight: Mediana ou outliers mais altos em 'Com Doença' indicam impacto do exercício.  
    """)

if len(df_filtered["sex"].unique()) > 1:
    df_ca = df_filtered.groupby(["sex", "ca", "target"]).size().reset_index(name="count")
    anim_frame_ca = "sex"
else:
    df_ca = df_filtered.groupby(["ca", "target"]).size().reset_index(name="count")
    anim_frame_ca = None

with col4:
    st.markdown("## 🩺 Número de Vasos Principais vs. Doença Cardíaca")
    fig_ca = px.bar(
        df_ca,
        x="ca",
        y="count",
        color="target",
        barmode="group",
        labels={
            "ca": "Number of Major Vessels",
            "target": "Heart Disease (0=No, 1=Yes)",
            "count": "Contagem"
        },
        title="Relação Dinâmica entre Vasos Principais e Doença Cardíaca",
        animation_frame=anim_frame_ca,
        height=400
    )
    fig_ca.update_xaxes(tickvals=[0, 1, 2, 3], ticktext=["0", "1", "2", "3"])
    fig_ca.update_layout(hovermode="x unified")
    st.plotly_chart(fig_ca, use_container_width=True)
    st.info("""
    🧐 *Interpretação*:  
    - Barras dinâmicas para o número de vasos principais (0 a 3).  
    - Interaja com o gráfico usando zoom, pan ou hover para detalhes.  
    - Animação por sexo (se disponível) mostra variações entre gêneros.  
    - Insight: Mais vasos afetados (2 ou 3) com doença sugerem maior gravidade.  
    """)

st.markdown("## 📊 Conclusões e Insights Dinâmicos")
st.success("""
✅ *Resumo*:  
- Açúcar elevado no sangue pode ser um fator de risco (explore com hover e filtros).  
- ECG anormal (ST-T ou hipertrofia) está ligado a maior prevalência de doença.  
- Oldpeak mais alto em pacientes com doença reflete impacto do exercício (veja outliers).  
- Mais vasos afetados indicam gravidade (use animação por sexo para padrões).  
- *Dica*: Experimente os filtros e interaja com os gráficos para análises personalizadas!  
""")
