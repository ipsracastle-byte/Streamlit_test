"""
Aplicación Streamlit: Simulador de Lanzamiento de Moneda

Descripción:
    Aplicación interactiva que simula el lanzamiento de una moneda
    y muestra estadísticas sobre los resultados.

Autor: Israel Castillo
Fecha: 2026-02-22
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Tuple

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE LA PÁGINA
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Simulador de Moneda",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# FUNCIONES
# ═══════════════════════════════════════════════════════════════════════════

def flip_coin(n_flips: int = 1, probability: float = 0.5) -> List[str]:
    """
    Simula el lanzamiento de una moneda n veces.
    
    Args:
        n_flips (int): Número de lanzamientos
        probability (float): Probabilidad de obtener cara (0.5 = moneda justa)
    
    Returns:
        list: Lista con resultados ('Cara' o 'Cruz')
    """
    results = np.random.choice(
        ['Cara', 'Cruz'], 
        size=n_flips, 
        p=[probability, 1 - probability]
    )
    return results.tolist()


def calculate_statistics(results: List[str]) -> dict:
    """
    Calcula estadísticas de los lanzamientos.
    
    Args:
        results (list): Lista de resultados
    
    Returns:
        dict: Diccionario con estadísticas
    """
    total = len(results)
    caras = results.count('Cara')
    cruces = results.count('Cruz')
    
    return {
        'total': total,
        'caras': caras,
        'cruces': cruces,
        'porcentaje_caras': (caras / total * 100) if total > 0 else 0,
        'porcentaje_cruces': (cruces / total * 100) if total > 0 else 0
    }


def create_pie_chart(stats: dict) -> go.Figure:
    """
    Crea gráfico de pastel con los resultados.
    
    Args:
        stats (dict): Estadísticas de lanzamientos
    
    Returns:
        go.Figure: Gráfico de Plotly
    """
    fig = go.Figure(data=[go.Pie(
        labels=['Cara', 'Cruz'],
        values=[stats['caras'], stats['cruces']],
        hole=0.3,
        marker_colors=['#FFD700', '#C0C0C0']
    )])
    
    fig.update_layout(
        title_text="Distribución de Resultados",
        showlegend=True,
        height=400
    )
    
    return fig


def create_bar_chart(stats: dict) -> go.Figure:
    """
    Crea gráfico de barras con los resultados.
    
    Args:
        stats (dict): Estadísticas de lanzamientos
    
    Returns:
        go.Figure: Gráfico de Plotly
    """
    fig = go.Figure(data=[
        go.Bar(
            x=['Cara', 'Cruz'],
            y=[stats['caras'], stats['cruces']],
            marker_color=['#FFD700', '#C0C0C0'],
            text=[stats['caras'], stats['cruces']],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title_text="Frecuencia de Resultados",
        xaxis_title="Resultado",
        yaxis_title="Frecuencia",
        height=400
    )
    
    return fig


def create_cumulative_chart(results: List[str]) -> go.Figure:
    """
    Crea gráfico acumulativo de resultados.
    
    Args:
        results (list): Lista de resultados
    
    Returns:
        go.Figure: Gráfico de Plotly
    """
    caras_acum = []
    cruces_acum = []
    caras_count = 0
    cruces_count = 0
    
    for result in results:
        if result == 'Cara':
            caras_count += 1
        else:
            cruces_count += 1
        caras_acum.append(caras_count)
        cruces_acum.append(cruces_count)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(1, len(results) + 1)),
        y=caras_acum,
        mode='lines',
        name='Caras',
        line=dict(color='#FFD700', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=list(range(1, len(results) + 1)),
        y=cruces_acum,
        mode='lines',
        name='Cruces',
        line=dict(color='#C0C0C0', width=2)
    ))
    
    fig.update_layout(
        title_text="Resultados Acumulativos",
        xaxis_title="Número de Lanzamiento",
        yaxis_title="Frecuencia Acumulada",
        height=400,
        hovermode='x unified'
    )
    
    return fig


def perform_binomial_test(n_caras: int, n_total: int, p: float = 0.5) -> dict:
    """
    Realiza prueba binomial para verificar si la moneda es justa.
    
    Args:
        n_caras (int): Número de caras obtenidas
        n_total (int): Total de lanzamientos
        p (float): Probabilidad esperada (0.5 para moneda justa)
    
    Returns:
        dict: Resultados de la prueba
    """
    # Prueba binomial bilateral (usando binomtest en lugar de binom_test deprecado)
    try:
        # SciPy >= 1.7.0
        result = stats.binomtest(n_caras, n_total, p, alternative='two-sided')
        p_value = result.pvalue
    except AttributeError:
        # Fallback para versiones antiguas de SciPy
        from scipy.stats import binom
        # Cálculo manual del p-value
        if n_caras <= n_total * p:
            p_value = 2 * binom.cdf(n_caras, n_total, p)
        else:
            p_value = 2 * (1 - binom.cdf(n_caras - 1, n_total, p))
        p_value = min(p_value, 1.0)  # Asegurar que no exceda 1.0
    
    # Intervalo de confianza
    confidence_interval = stats.binom.interval(0.95, n_total, p)
    
    return {
        'p_value': p_value,
        'is_fair': p_value > 0.05,
        'confidence_interval': confidence_interval
    }


# ═══════════════════════════════════════════════════════════════════════════
# INTERFAZ DE USUARIO
# ═══════════════════════════════════════════════════════════════════════════

# Título principal
st.title("🪙 Simulador de Lanzamiento de Moneda")
st.markdown("---")

# Sidebar - Configuración
st.sidebar.header("⚙️ Configuración")

# Número de lanzamientos
n_flips = st.sidebar.slider(
    "Número de lanzamientos",
    min_value=1,
    max_value=1000,
    value=10,
    step=1,
    help="Selecciona cuántas veces quieres lanzar la moneda"
)

# Probabilidad de cara (para simular moneda sesgada)
probability = st.sidebar.slider(
    "Probabilidad de Cara",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
    help="0.5 = moneda justa, otros valores = moneda sesgada"
)

# Mostrar si la moneda es justa
if probability == 0.5:
    st.sidebar.success("✅ Moneda justa")
else:
    st.sidebar.warning(f"⚠️ Moneda sesgada ({probability*100:.0f}% cara)")

st.sidebar.markdown("---")

# Botón para lanzar
if st.sidebar.button("🎲 Lanzar Moneda", type="primary", use_container_width=True):
    # Realizar lanzamientos
    with st.spinner('Lanzando moneda...'):
        results = flip_coin(n_flips, probability)
        stats_data = calculate_statistics(results)
        
        # Guardar en session_state
        st.session_state['results'] = results
        st.session_state['stats'] = stats_data

# Botón para limpiar
if st.sidebar.button("🗑️ Limpiar Resultados", use_container_width=True):
    if 'results' in st.session_state:
        del st.session_state['results']
        del st.session_state['stats']
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# MOSTRAR RESULTADOS
# ═══════════════════════════════════════════════════════════════════════════

if 'results' in st.session_state:
    results = st.session_state['results']
    stats_data = st.session_state['stats']
    
    # Métricas principales
    st.subheader("📊 Resultados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Lanzamientos",
            value=stats_data['total']
        )
    
    with col2:
        st.metric(
            label="🟡 Caras",
            value=stats_data['caras'],
            delta=f"{stats_data['porcentaje_caras']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="⚪ Cruces",
            value=stats_data['cruces'],
            delta=f"{stats_data['porcentaje_cruces']:.1f}%"
        )
    
    with col4:
        diferencia = abs(stats_data['caras'] - stats_data['cruces'])
        st.metric(
            label="Diferencia",
            value=diferencia
        )
    
    st.markdown("---")
    
    # Gráficos
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distribución", 
        "📈 Barras", 
        "📉 Acumulativo",
        "🧪 Análisis Estadístico"
    ])
    
    with tab1:
        st.plotly_chart(
            create_pie_chart(stats_data), 
            use_container_width=True
        )
    
    with tab2:
        st.plotly_chart(
            create_bar_chart(stats_data), 
            use_container_width=True
        )
    
    with tab3:
        st.plotly_chart(
            create_cumulative_chart(results), 
            use_container_width=True
        )
    
    with tab4:
        st.subheader("🧪 Prueba Binomial")
        st.markdown("""
        Esta prueba determina si los resultados son consistentes con una moneda justa.
        - **H₀**: La moneda es justa (p = 0.5)
        - **H₁**: La moneda NO es justa (p ≠ 0.5)
        - **Nivel de significancia**: α = 0.05
        """)
        
        test_results = perform_binomial_test(
            stats_data['caras'], 
            stats_data['total']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Valor p",
                value=f"{test_results['p_value']:.4f}"
            )
        
        with col2:
            if test_results['is_fair']:
                st.success("✅ La moneda parece justa")
            else:
                st.error("❌ La moneda parece sesgada")
        
        st.info(f"""
        **Interpretación:**
        - Valor p = {test_results['p_value']:.4f}
        - {'No rechazamos' if test_results['is_fair'] else 'Rechazamos'} la hipótesis nula
        - Intervalo de confianza 95%: [{test_results['confidence_interval'][0]:.0f}, {test_results['confidence_interval'][1]:.0f}]
        """)
    
    # Tabla de resultados detallados
    with st.expander("📋 Ver Resultados Detallados"):
        df_results = pd.DataFrame({
            'Lanzamiento': range(1, len(results) + 1),
            'Resultado': results
        })
        st.dataframe(df_results, use_container_width=True)
        
        # Opción para descargar
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name="resultados_moneda.csv",
            mime="text/csv"
        )

else:
    # Mensaje inicial
    st.info("👈 Configura los parámetros en la barra lateral y presiona **'Lanzar Moneda'** para comenzar")
    
    # Información adicional
    st.subheader("ℹ️ Acerca de esta aplicación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Características
        - Simula lanzamientos de moneda
        - Visualización interactiva
        - Análisis estadístico
        - Prueba de hipótesis binomial
        - Exportación de resultados
        """)
    
    with col2:
        st.markdown("""
        ### 📚 Conceptos
        - **Probabilidad**: 0.5 = moneda justa
        - **Distribución binomial**: Modelo matemático
        - **Prueba de hipótesis**: Verificar aleatoriedad
        - **Intervalo de confianza**: Rango esperado
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Desarrollado con ❤️ usando Streamlit | © 2026 Israel Castillo</p>
</div>
""", unsafe_allow_html=True)