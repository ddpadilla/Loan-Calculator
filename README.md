# 💰 Calculadora de Préstamos con Streamlit

Una aplicación web interactiva para calcular préstamos, generar tablas de amortización y visualizar datos financieros.

## 🚀 Características

- **Cálculo de Cuota Mensual**: Utiliza la fórmula de anualidades para calcular pagos fijos
- **Tabla de Amortización**: Plan de pagos detallado mes a mes
- **Visualizaciones Interactivas**: 
  - Evolución del saldo pendiente
  - Composición de pagos (capital vs interés)
- **Exportación de Datos**: Descarga en formato Excel y CSV
- **Interfaz Intuitiva**: Diseño responsivo y fácil de usar

## 📋 Requisitos

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- OpenPyXL

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**

2. **Activar el entorno virtual** (ya configurado):
   ```bash
   source venv/bin/activate
   ```

3. **Instalar dependencias** (ya instaladas):
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Uso

1. **Ejecutar la aplicación**:
   ```bash
   streamlit run loan_calculator.py
   ```

2. **Abrir en el navegador**: 
   - La aplicación se abrirá automáticamente en `http://localhost:8501`

3. **Usar la calculadora**:
   - Ingresa el monto del préstamo
   - Especifica la tasa de interés anual (%)
   - Define el plazo en meses
   - Presiona "Calcular Préstamo"

## 📊 Funcionalidades

### Cálculo de Préstamo
La aplicación utiliza la fórmula de anualidades:

```
Cuota = P × [r × (1+r)^n] / [(1+r)^n - 1]
```

Donde:
- **P** = Monto del préstamo
- **r** = Tasa de interés mensual
- **n** = Número de meses

### Tabla de Amortización
Muestra para cada pago:
- Número de pago
- Cuota mensual
- Capital pagado
- Interés pagado
- Saldo restante

### Visualizaciones
- **Gráfica de Saldo**: Evolución del saldo pendiente a lo largo del tiempo
- **Composición de Pagos**: Proporción de capital e interés en cada pago

### Exportación
- **Excel**: Archivo completo con resumen y tabla de amortización
- **CSV**: Tabla de amortización en formato plano

## 🎯 Ejemplo de Uso

```
Monto del Préstamo: L.100,000
Tasa de Interés Anual: 5%
Plazo: 60 meses (5 años)

Resultado:
- Cuota Mensual: L.1,887.12
- Total a Pagar: L.113,227.20
- Total Intereses: L.13,227.20
```

## 📁 Estructura del Proyecto

```
.
├── loan_calculator.py    # Aplicación principal
├── requirements.txt      # Dependencias
├── README.md            # Este archivo
└── venv/               # Entorno virtual
```


