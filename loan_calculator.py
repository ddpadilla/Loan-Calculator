import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO


def calculate_monthly_payment(principal, annual_rate, months):
    """
    Calcula la cuota mensual fija usando la fórmula de anualidades.
    
    Fórmula: Cuota = P * r * (1+r)^n / ((1+r)^n - 1)
    
    Args:
        principal (float): Monto del préstamo
        annual_rate (float): Tasa de interés anual (%)
        months (int): Plazo en meses
    
    Returns:
        float: Cuota mensual
    """
    if annual_rate == 0:
        return principal / months
    
    monthly_rate = annual_rate / 100 / 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    return payment


def generate_amortization_schedule(principal, annual_rate, months):
    """
    Genera la tabla de amortización completa del préstamo.
    
    Args:
        principal (float): Monto del préstamo
        annual_rate (float): Tasa de interés anual (%)
        months (int): Plazo en meses
    
    Returns:
        pd.DataFrame: Tabla de amortización con columnas:
                     - Pago: Número de pago
                     - Cuota: Cuota mensual
                     - Capital: Capital pagado
                     - Interés: Interés pagado
                     - Saldo: Saldo restante
    """
    monthly_payment = calculate_monthly_payment(principal, annual_rate, months)
    monthly_rate = annual_rate / 100 / 12
    
    schedule = []
    remaining_balance = principal
    
    for payment_number in range(1, months + 1):
        interest_payment = remaining_balance * monthly_rate
        # Capital
        principal_payment = monthly_payment - interest_payment

        if payment_number == months:
            principal_payment = remaining_balance
            monthly_payment = principal_payment + interest_payment
        
        # Actualiza saldo
        remaining_balance -= principal_payment
        
        # Agrega fila al cronograma
        schedule.append({
            'Pago': payment_number,
            'Cuota': monthly_payment,
            'Capital': principal_payment,
            'Interés': interest_payment,
            'Saldo': max(0, remaining_balance)  # Evita saldos negativos por redondeo
        })
    
    return pd.DataFrame(schedule)


def create_balance_evolution_chart(df):
    """
    Crea gráfica de evolución del saldo pendiente.
    
    Args:
        df (pd.DataFrame): Tabla de amortización
    
    Returns:
        plotly.graph_objects.Figure: Gráfica de línea del saldo
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Pago'],
        y=df['Saldo'],
        mode='lines+markers',
        name='Saldo Pendiente',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Evolución del Saldo Pendiente',
        xaxis_title='Número de Pago',
        yaxis_title='Saldo (L.)',
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def create_payment_composition_chart(df):
    """
    Crea gráfica de proporción capital vs intereses.
    
    Args:
        df (pd.DataFrame): Tabla de amortización
    
    Returns:
        plotly.graph_objects.Figure: Gráfica de barras apiladas
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Pago'],
        y=df['Capital'],
        name='Capital',
        marker_color='#2ca02c'
    ))
    
    fig.add_trace(go.Bar(
        x=df['Pago'],
        y=df['Interés'],
        name='Interés',
        marker_color='#ff7f0e'
    ))
    
    fig.update_layout(
        title='Composición de Pagos: Capital vs Interés',
        xaxis_title='Número de Pago',
        yaxis_title='Monto ($)',
        barmode='stack',
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def export_to_excel(df, principal, annual_rate, months):
    """
    Exporta la tabla de amortización a Excel.
    
    Args:
        df (pd.DataFrame): Tabla de amortización
        principal (float): Monto del préstamo
        annual_rate (float): Tasa de interés anual
        months (int): Plazo en meses
    
    Returns:
        BytesIO: Archivo Excel en memoria
    """
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Crea hoja de resumen
        summary_data = {
            'Concepto': [
                'Monto del Préstamo',
                'Tasa de Interés Anual (%)',
                'Plazo (meses)',
                'Cuota Mensual',
                'Total a Pagar',
                'Total Intereses'
            ],
            'Valor': [
                f"L.{principal:,.2f}",
                f"{annual_rate}%",
                months,
                f"L.{df['Cuota'].iloc[0]:,.2f}",
                f"L.{df['Cuota'].sum():,.2f}",
                f"L.{df['Interés'].sum():,.2f}"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Resumen', index=False)
        
        # Crea tabla de amortización
        df_formatted = df.copy()
        for col in ['Cuota', 'Capital', 'Interés', 'Saldo']:
            df_formatted[col] = df_formatted[col].apply(lambda x: f"L.{x:,.2f}")
        
        df_formatted.to_excel(writer, sheet_name='Tabla de Amortización', index=False)
    
    output.seek(0)
    return output


def main():
    """Función principal de la aplicación Streamlit."""

    st.set_page_config(
        page_title="Calculadora de Préstamos",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("💰 Calculadora de Préstamos")
    st.markdown("---")
    st.sidebar.header("📊 Parámetros del Préstamo")
    
    # Input
    principal = st.sidebar.number_input(
        "💵 Monto del Préstamo (L.)",
        min_value=1000.0,
        max_value=10000000.0,
        value=100000.0,
        step=1000.0,
        format="%.2f"
    )
    
    annual_rate = st.sidebar.number_input(
        "📈 Tasa de Interés Anual (%)",
        min_value=0.0,
        max_value=50.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )
    
    months = st.sidebar.number_input(
        "📅 Plazo en Meses",
        min_value=1,
        max_value=480,
        value=60,
        step=1
    )
    
    # Botón para calcular
    calculate_button = st.sidebar.button("🔢 Calcular Préstamo", type="primary")
    
    if calculate_button or 'calculated' in st.session_state:
        if calculate_button:
            st.session_state['calculated'] = True
            st.session_state['principal'] = principal
            st.session_state['annual_rate'] = annual_rate
            st.session_state['months'] = months

        principal = st.session_state['principal']
        annual_rate = st.session_state['annual_rate']
        months = st.session_state['months']
        
        # Calcula cuota mensual
        monthly_payment = calculate_monthly_payment(principal, annual_rate, months)
        
        # Genera tabla de amortización
        df = generate_amortization_schedule(principal, annual_rate, months)
        
        # Resultados principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Monto del Préstamo", f"L.{principal:,.2f}")
        
        with col2:
            st.metric("💳 Cuota Mensual", f"L.{monthly_payment:,.2f}")
        
        with col3:
            st.metric("💸 Total a Pagar", f"L.{df['Cuota'].sum():,.2f}")
        
        with col4:
            st.metric("📊 Total Intereses", f"L.{df['Interés'].sum():,.2f}")
        
        st.markdown("---")
        
        # Tabs para organizar el contenido
        tab1, tab2, tab3 = st.tabs(["📋 Tabla de Amortización", "📈 Gráficas", "💾 Exportar"])
        
        with tab1:
            st.subheader("📋 Plan de Pagos Detallado")
            
            # Formatear para mostrar
            df_display = df.copy()
            df_display['Cuota'] = df_display['Cuota'].apply(lambda x: f"L.{x:,.2f}")
            df_display['Capital'] = df_display['Capital'].apply(lambda x: f"L.{x:,.2f}")
            df_display['Interés'] = df_display['Interés'].apply(lambda x: f"L.{x:,.2f}")
            df_display['Saldo'] = df_display['Saldo'].apply(lambda x: f"L.{x:,.2f}")
            
            # Mostrar tabla
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Pago": st.column_config.NumberColumn("Pago #"),
                    "Cuota": st.column_config.TextColumn("Cuota"),
                    "Capital": st.column_config.TextColumn("Capital"),
                    "Interés": st.column_config.TextColumn("Interés"),
                    "Saldo": st.column_config.TextColumn("Saldo Restante")
                }
            )
        
        with tab2:
            st.subheader("📈 Visualizaciones")
            
            # Gráfica de evolución del saldo
            st.plotly_chart(
                create_balance_evolution_chart(df),
                use_container_width=True
            )
            
            st.markdown("---")
            
            # Gráfica de composición de pagos
            st.plotly_chart(
                create_payment_composition_chart(df),
                use_container_width=True
            )
        
        with tab3:
            st.subheader("💾 Exportar Datos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Descargar como Excel")
                excel_file = export_to_excel(df, principal, annual_rate, months)
                st.download_button(
                    label="⬇️ Descargar Excel",
                    data=excel_file,
                    file_name=f"amortizacion_prestamo_{principal:.0f}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                st.markdown("#### 📄 Descargar como CSV")
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Descargar CSV",
                    data=csv,
                    file_name=f"amortizacion_prestamo_{principal:.0f}.csv",
                    mime="text/csv"
                )
    
    else:
        st.info("👈 Ingresa los parámetros del préstamo en la barra lateral y presiona 'Calcular Préstamo' para comenzar.")
        st.markdown("### 📚 Información sobre el Cálculo")
        
        st.markdown("""
        Esta calculadora utiliza la **fórmula de anualidades** para calcular la cuota mensual fija:
        
        $$Cuota = P \\cdot \\frac{r \\cdot (1+r)^n}{(1+r)^n - 1}$$
        
        Donde:
        - **P** = Monto del préstamo
        - **r** = Tasa de interés mensual (tasa anual ÷ 12)
        - **n** = Número de meses
        """)
        
        st.markdown("""
        ### 🔧 Funcionalidades
        
        -  Cálculo de cuota mensual fija
        -  Tabla de amortización completa
        -  Gráficas interactivas
        -  Exportación a Excel y CSV
        -  Interfaz intuitiva y responsiva
        """)


if __name__ == "__main__":
    main()
