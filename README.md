# 🪙 Simulador de Lanzamiento de Moneda

Aplicación interactiva desarrollada con Streamlit que simula el lanzamiento de una moneda y proporciona análisis estadístico de los resultados.

## 🎯 Características

- ✅ Simulación de lanzamientos de moneda (1-1000 lanzamientos)
- ✅ Configuración de probabilidad (moneda justa o sesgada)
- ✅ Visualizaciones interactivas con Plotly:
  - Gráfico de pastel
  - Gráfico de barras
  - Gráfico acumulativo
- ✅ Análisis estadístico:
  - Prueba binomial
  - Intervalos de confianza
  - Prueba de hipótesis
- ✅ Exportación de resultados a CSV
- ✅ Interfaz responsive y moderna

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Streamlit_test
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Parámetros configurables

- **Número de lanzamientos**: 1-1000
- **Probabilidad de Cara**: 0.0-1.0 (0.5 = moneda justa)

## 📊 Funcionalidades

### 1. Simulación Básica
- Lanza la moneda n veces
- Muestra resultados en tiempo real
- Calcula estadísticas automáticamente

### 2. Visualizaciones
- **Distribución**: Gráfico de pastel mostrando proporción Cara/Cruz
- **Barras**: Frecuencia absoluta de cada resultado
- **Acumulativo**: Evolución de resultados a lo largo de los lanzamientos

### 3. Análisis Estadístico
- Prueba binomial para verificar si la moneda es justa
- Cálculo de valor p
- Intervalos de confianza al 95%
- Interpretación automática de resultados

### 4. Exportación
- Descarga resultados en formato CSV
- Incluye número de lanzamiento y resultado

## 🧪 Conceptos Estadísticos

### Distribución Binomial
Modelo matemático que describe el número de éxitos en n ensayos independientes con probabilidad p.

### Prueba de Hipótesis
- **H₀**: La moneda es justa (p = 0.5)
- **H₁**: La moneda NO es justa (p ≠ 0.5)
- **α**: 0.05 (nivel de significancia)

Si p-value < 0.05: Rechazamos H₀ (moneda sesgada)
Si p-value ≥ 0.05: No rechazamos H₀ (moneda justa)

## 📁 Estructura del Proyecto

```
Streamlit_test/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
└── README.md          # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **SciPy**: Análisis estadístico
- **Plotly**: Visualizaciones interactivas

## 📝 Ejemplos de Uso

### Moneda Justa (p=0.5)
```python
# Configurar:
- Lanzamientos: 100
- Probabilidad: 0.5

# Resultado esperado:
- ~50 caras
- ~50 cruces
- p-value > 0.05
```

### Moneda Sesgada (p=0.7)
```python
# Configurar:
- Lanzamientos: 100
- Probabilidad: 0.7

# Resultado esperado:
- ~70 caras
- ~30 cruces
- p-value < 0.05
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

**Israel Castillo**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Streamlit por el excelente framework
- Comunidad de Python por las librerías

---

**Última actualización:** 2026-02-22