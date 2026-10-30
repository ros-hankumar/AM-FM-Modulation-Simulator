import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration to wide layout and set title/icon
st.set_page_config(
    page_title="Analog Communication Modulation Simulator",
    page_icon="📟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark engineering laboratory UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Orbitron:wght@500;700;900&display=swap');

    /* Font configurations */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Laboratory Title Bar */
    .lab-title-container {
        background: linear-gradient(135deg, #0e1624 0%, #111827 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #1e293b;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 240, 255, 0.1);
        text-align: center;
    }
    .lab-title {
        color: #00f0ff;
        margin: 0;
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        letter-spacing: 2px;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    }
    .lab-subtitle {
        color: #94a3b8;
        margin: 6px 0 0 0;
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        font-weight: 400;
    }

    /* Section Panels */
    .panel-header {
        font-family: 'Orbitron', sans-serif;
        color: #00f0ff;
        font-size: 1.15rem;
        font-weight: 600;
        letter-spacing: 1px;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 8px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .panel-header-fm {
        color: #ff007f;
        border-bottom: 2px solid #1e293b;
    }

    /* Code/Formula styling */
    .formula-display {
        background-color: #080c14;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 12px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to generate custom metrics cards with oscilloscope theme
def metric_card(label, value, unit="", border_color="#00f0ff", label_color="#94a3b8", value_color="#ffffff", shadow_color="rgba(0, 240, 255, 0.08)"):
    return f"""
    <div style="
        background-color: #111827;
        padding: 16px;
        border-radius: 8px;
        border-left: 5px solid {border_color};
        margin-bottom: 12px;
        box-shadow: 0 4px 12px {shadow_color};
        border-top: 1px solid #1f2937;
        border-right: 1px solid #1f2937;
        border-bottom: 1px solid #1f2937;
        font-family: 'Inter', sans-serif;
    ">
        <div style="color: {label_color}; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">{label}</div>
        <div style="display: flex; align-items: baseline; margin-top: 5px;">
            <span style="color: {value_color}; font-family: 'JetBrains Mono', monospace; font-size: 1.6rem; font-weight: 700; text-shadow: 0 0 5px {shadow_color};">{value}</span>
            {f'<span style="color: {label_color}; font-family: \'JetBrains Mono\', monospace; font-size: 0.9rem; margin-left: 4px;">{unit}</span>' if unit else ''}
        </div>
    </div>
    """

# Title Bar
st.markdown("""
<div class="lab-title-container">
    <h1 class="lab-title">ANALOG COMMUNICATION MODULATION SIMULATOR</h1>
    <p class="lab-subtitle">High-Fidelity Virtual Oscilloscope & Signals Analysis Workspace</p>
</div>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE & RESET LOGIC -----------------
# Default parameter values
AM_DEFAULTS = {"am_Ac": 5.0, "am_Am": 3.0, "am_fc": 100.0, "am_fm": 10.0}
FM_DEFAULTS = {"fm_Ac": 5.0, "fm_fc": 100.0, "fm_fm": 10.0, "fm_df": 25.0}

# Initialize session state variables
for key, val in AM_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

for key, val in FM_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Callback functions to reset parameters
def reset_am_params():
    for key, val in AM_DEFAULTS.items():
        st.session_state[key] = val

def reset_fm_params():
    for key, val in FM_DEFAULTS.items():
        st.session_state[key] = val


# Create Tabs for AM and FM Modulators
tab1, tab2 = st.tabs(["📟 AM MODULATION SIMULATOR", "📡 FM MODULATION SIMULATOR"])

# ==========================================
# TAB 1: AM MODULATION SIMULATOR
# ==========================================
with tab1:
    col_input, col_output = st.columns([1, 2.5], gap="large")

    # --- INPUT COLUMN ---
    with col_input:
        st.markdown('<div class="panel-header">📟 PARAMETER GENERATOR</div>', unsafe_allow_html=True)
        
        # User controls for AM Parameters using sliders and number inputs
        Ac = st.slider("Carrier Amplitude (Ac)", min_value=0.1, max_value=20.0, step=0.1, key="am_Ac")
        Am = st.slider("Message Amplitude (Am)", min_value=0.1, max_value=20.0, step=0.1, key="am_Am")
        fc = st.number_input("Carrier Frequency (fc) [Hz]", min_value=1.0, max_value=2000.0, step=10.0, key="am_fc")
        fm = st.number_input("Message Frequency (fm) [Hz]", min_value=1.0, max_value=200.0, step=1.0, key="am_fm")
        
        # Reset Button for AM parameters
        st.button("🔄 Reset AM Parameters", on_click=reset_am_params, type="secondary", use_container_width=True)

    # --- OUTPUT & PLOT COLUMN ---
    with col_output:
        st.markdown('<div class="panel-header">📈 ANALYZER & OSCILLOSCOPE</div>', unsafe_allow_html=True)
        
        # Input Validation
        validation_error = None
        if Ac <= 0 or Am <= 0 or fc <= 0 or fm <= 0:
            validation_error = "All parameter values must be positive and greater than zero."
        elif fc <= fm:
            validation_error = "Carrier frequency (fc) must be strictly greater than Message frequency (fm) to avoid aliasing and severe distortion."

        if validation_error:
            st.error(f"⚠️ **INSTRUMENT ALERT:** {validation_error}")
        else:
            # Perform calculations
            mu = Am / Ac
            mod_percentage = mu * 100
            bw_am = 2 * fm
            
            # Determine Modulation Status
            if mu < 1.0:
                status = "Under Modulation"
                status_color = "#00e676"  # green
                status_shadow = "rgba(0, 230, 118, 0.12)"
            elif abs(mu - 1.0) < 1e-9:
                status = "Critical Modulation"
                status_color = "#00e5ff"  # cyan
                status_shadow = "rgba(0, 229, 255, 0.12)"
            else:
                status = "Over Modulation"
                status_color = "#ff1744"  # red/magenta
                status_shadow = "rgba(255, 23, 68, 0.12)"

            # Display metrics cards in columns
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(metric_card("Modulation Index (μ)", f"{mu:.3f}", shadow_color="rgba(0, 240, 255, 0.08)"), unsafe_allow_html=True)
                st.markdown(metric_card("Modulation Percentage", f"{mod_percentage:.1f}", "%", shadow_color="rgba(0, 240, 255, 0.08)"), unsafe_allow_html=True)
            with m_col2:
                st.markdown(metric_card("Calculated Bandwidth", f"{bw_am:.1f}", "Hz", shadow_color="rgba(0, 240, 255, 0.08)"), unsafe_allow_html=True)
            with m_col3:
                st.markdown(metric_card("Modulation Status", status, border_color=status_color, value_color=status_color, shadow_color=status_shadow), unsafe_allow_html=True)

            # Display Equations
            st.markdown("##### 🧮 SYSTEM EQUATION")
            st.latex(r"s(t) = [A_c + A_m \cos(2\pi f_m t)] \cos(2\pi f_c t)")
            st.latex(fr"s(t) = [{Ac:.1f} + {Am:.1f} \cos({2*np.pi*fm:.2f} t)] \cos({2*np.pi*fc:.2f} t)")

            # Generate Waveform Signals
            num_periods = 3
            T_max = num_periods / fm
            needed_points = int(20 * fc * T_max)
            N = min(10000, max(2000, needed_points))
            t = np.linspace(0, T_max, N)

            m_t = Am * np.cos(2 * np.pi * fm * t)
            c_t = Ac * np.cos(2 * np.pi * fc * t)
            s_t = (Ac + m_t) * np.cos(2 * np.pi * fc * t)
            env_pos = Ac + m_t
            env_neg = - (Ac + m_t)

            # Build Multi-row Plotly Oscilloscope Chart
            fig = make_subplots(
                rows=3, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.07,
                subplot_titles=(
                    "📟 <b>Channel 1: Message Signal m(t)</b>",
                    "📟 <b>Channel 2: Carrier Signal c(t)</b>",
                    "📟 <b>Channel 3: Amplitude Modulated Signal s(t)</b>"
                )
            )

            # Add traces
            # Message trace (Neon orange)
            fig.add_trace(go.Scatter(x=t, y=m_t, name="m(t)", line=dict(color="#FF9100", width=2.5)), row=1, col=1)
            # Carrier trace (Neon cyan)
            fig.add_trace(go.Scatter(x=t, y=c_t, name="c(t)", line=dict(color="#00E5FF", width=1.5)), row=2, col=1)
            # AM trace (Neon green)
            fig.add_trace(go.Scatter(x=t, y=s_t, name="s(t)", line=dict(color="#00E676", width=2)), row=3, col=1)
            
            # Envelopes
            fig.add_trace(go.Scatter(x=t, y=env_pos, name="Upper Envelope", line=dict(color="rgba(255, 255, 255, 0.4)", width=1.5, dash='dash')), row=3, col=1)
            fig.add_trace(go.Scatter(x=t, y=env_neg, name="Lower Envelope", line=dict(color="rgba(255, 255, 255, 0.4)", width=1.5, dash='dash')), row=3, col=1)

            # Layout adjustments
            fig.update_layout(
                height=720,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor="#0b0f19",
                paper_bgcolor="#0b0f19",
                font=dict(family="JetBrains Mono, monospace", color="#ffffff"),
                margin=dict(t=50, b=40, l=40, r=40),
                hovermode="x unified"
            )

            # Set grid styles and titles
            for i in range(1, 4):
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#1e293b", zeroline=True, zerolinewidth=1, zerolinecolor="#475569", row=i, col=1)
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#1e293b", zeroline=True, zerolinewidth=1, zerolinecolor="#475569", row=i, col=1)

            fig.update_xaxes(title_text="Time (seconds)", row=3, col=1)
            fig.update_yaxes(title_text="Amplitude (V)", row=1, col=1)
            fig.update_yaxes(title_text="Amplitude (V)", row=2, col=1)
            fig.update_yaxes(title_text="Amplitude (V)", row=3, col=1)

            # Plot interactive chart
            st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})


# ==========================================
# TAB 2: FM MODULATION SIMULATOR
# ==========================================
with tab2:
    col_input, col_output = st.columns([1, 2.5], gap="large")

    # --- INPUT COLUMN ---
    with col_input:
        st.markdown('<div class="panel-header panel-header-fm">📟 PARAMETER GENERATOR</div>', unsafe_allow_html=True)
        
        # User controls for FM Parameters
        Ac_fm = st.slider("Carrier Amplitude", min_value=0.1, max_value=20.0, step=0.1, key="fm_Ac")
        fc_fm = st.number_input("Carrier Frequency (fc) [Hz] ", min_value=1.0, max_value=2000.0, step=10.0, key="fm_fc")
        fm_fm = st.number_input("Message Frequency (fm) [Hz] ", min_value=1.0, max_value=200.0, step=1.0, key="fm_fm")
        df_fm = st.slider("Frequency Deviation (Δf) [Hz]", min_value=0.1, max_value=200.0, step=0.5, key="fm_df")
        
        # Reset Button for FM parameters
        st.button("🔄 Reset FM Parameters", on_click=reset_fm_params, type="secondary", use_container_width=True)

    # --- OUTPUT & PLOT COLUMN ---
    with col_output:
        st.markdown('<div class="panel-header panel-header-fm">📈 ANALYZER & OSCILLOSCOPE</div>', unsafe_allow_html=True)
        
        # Input Validation for FM
        validation_error_fm = None
        if Ac_fm <= 0 or fc_fm <= 0 or fm_fm <= 0 or df_fm <= 0:
            validation_error_fm = "All parameter values must be positive and greater than zero."
        elif fc_fm <= fm_fm:
            validation_error_fm = "Carrier frequency (fc) must be strictly greater than Message frequency (fm) to avoid aliasing and display constraints."

        if validation_error_fm:
            st.error(f"⚠️ **INSTRUMENT ALERT:** {validation_error_fm}")
        else:
            # Perform calculations
            beta = df_fm / fm_fm
            bw_fm = 2 * (df_fm + fm_fm)
            freq_swing = 2 * df_fm

            # Display metrics cards in columns
            fm_col1, fm_col2, fm_col3 = st.columns(3)
            with fm_col1:
                st.markdown(metric_card("Modulation Index (β)", f"{beta:.3f}", border_color="#ff007f", shadow_color="rgba(255, 0, 127, 0.08)"), unsafe_allow_html=True)
            with fm_col2:
                st.markdown(metric_card("Carson's Bandwidth (BW)", f"{bw_fm:.1f}", "Hz", border_color="#ff007f", shadow_color="rgba(255, 0, 127, 0.08)"), unsafe_allow_html=True)
            with fm_col3:
                st.markdown(metric_card("Frequency Swing (2Δf)", f"{freq_swing:.1f}", "Hz", border_color="#ff007f", shadow_color="rgba(255, 0, 127, 0.08)"), unsafe_allow_html=True)

            # Display Equations
            st.markdown("##### 🧮 SYSTEM EQUATION")
            st.latex(r"s(t) = A_c \cos\left(2\pi f_c t + \beta \sin(2\pi f_m t)\right)")
            st.latex(fr"s(t) = {Ac_fm:.1f} \cos\left({2*np.pi*fc_fm:.2f} t + {beta:.2f} \sin({2*np.pi*fm_fm:.2f} t)\right)")

            # Generate Waveform Signals
            num_periods_fm = 3
            T_max_fm = num_periods_fm / fm_fm
            # FM needs higher resolution to capture frequency deviations accurately
            needed_points_fm = int(25 * (fc_fm + df_fm) * T_max_fm)
            N_fm = min(10000, max(3000, needed_points_fm))
            t_fm = np.linspace(0, T_max_fm, N_fm)

            # Message (Assume normalized message for FM where df is driven by parameters)
            m_t_fm = np.cos(2 * np.pi * fm_fm * t_fm)
            c_t_fm = Ac_fm * np.cos(2 * np.pi * fc_fm * t_fm)
            
            # FM signal formula: Ac * cos(2*pi*fc*t + beta * sin(2*pi*fm*t))
            s_t_fm = Ac_fm * np.cos(2 * np.pi * fc_fm * t_fm + beta * np.sin(2 * np.pi * fm_fm * t_fm))

            # Build Multi-row Plotly Oscilloscope Chart
            fig_fm = make_subplots(
                rows=3, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.07,
                subplot_titles=(
                    "📡 <b>Channel 1: Message Signal m(t) (Normalized)</b>",
                    "📡 <b>Channel 2: Carrier Signal c(t)</b>",
                    "📡 <b>Channel 3: Frequency Modulated Signal s(t)</b>"
                )
            )

            # Add traces
            # Message trace (Neon orange)
            fig_fm.add_trace(go.Scatter(x=t_fm, y=m_t_fm, name="m(t)", line=dict(color="#FF9100", width=2.5)), row=1, col=1)
            # Carrier trace (Neon cyan)
            fig_fm.add_trace(go.Scatter(x=t_fm, y=c_t_fm, name="c(t)", line=dict(color="#00E5FF", width=1.5)), row=2, col=1)
            # FM trace (Neon magenta)
            fig_fm.add_trace(go.Scatter(x=t_fm, y=s_t_fm, name="s(t)", line=dict(color="#FF007F", width=2)), row=3, col=1)

            # Layout adjustments
            fig_fm.update_layout(
                height=720,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor="#0b0f19",
                paper_bgcolor="#0b0f19",
                font=dict(family="JetBrains Mono, monospace", color="#ffffff"),
                margin=dict(t=50, b=40, l=40, r=40),
                hovermode="x unified"
            )

            # Set grid styles and titles
            for i in range(1, 4):
                fig_fm.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#1e293b", zeroline=True, zerolinewidth=1, zerolinecolor="#475569", row=i, col=1)
                fig_fm.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#1e293b", zeroline=True, zerolinewidth=1, zerolinecolor="#475569", row=i, col=1)

            fig_fm.update_xaxes(title_text="Time (seconds)", row=3, col=1)
            fig_fm.update_yaxes(title_text="Amplitude (V)", row=1, col=1)
            fig_fm.update_yaxes(title_text="Amplitude (V)", row=2, col=1)
            fig_fm.update_yaxes(title_text="Amplitude (V)", row=3, col=1)

            # Plot interactive chart
            st.plotly_chart(fig_fm, use_container_width=True, config={"displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})


# ==========================================
# THEORY SECTION (EXPANDER)
# ==========================================
st.write("")  # Spacing
st.markdown("---")
with st.expander("📚 LABORATORY MANUAL: MODULATION THEORY & PRINCIPLES"):
    st.markdown(r"""
    ### 1. What is Modulation?
    Modulation is the process of translating an information-bearing baseband signal (message signal) to a higher frequency range by varying one or more parameters of a high-frequency carrier wave.
    
    **Why is Modulation necessary?**
    *   **Antenna Height Reduction:** The required size of a transmitting antenna is inversely proportional to frequency ($L \approx \lambda/4$). By modulating signals to a higher frequency carrier, antenna dimensions are reduced to practical lengths.
    *   **Frequency Multiplexing:** Allows multiple information channels to share a single physical communication medium simultaneously by utilizing different carrier frequencies (Frequency Division Multiplexing).
    *   **Noise & Interference Resistance:** Some modulation schemes (like FM) exchange bandwidth for high immunity to channel noise and amplitude fluctuations.
    
    ---
    
    ### 2. Amplitude Modulation (AM) Principles
    In **Amplitude Modulation**, the instantaneous amplitude of the carrier wave is varied linearly with the message signal $m(t)$.
    
    The AM signal is defined by:
    $$s(t) = [A_c + m(t)] \\cos(2\\pi f_c t) = A_c [1 + \\mu x(t)] \\cos(2\\pi f_c t)$$
    where:
    *   $A_c$ is the Carrier Amplitude.
    *   $m(t) = A_m \\cos(2\\pi f_m t)$ is the message signal, and $x(t) = \\cos(2\\pi f_m t)$ is the normalized message signal.
    *   $\\mu = \\frac{A_m}{A_c}$ is the **Modulation Index**.
    
    **Modulation Index States:**
    *   **Under-Modulation ($\\mu < 1$):** The carrier envelope never crosses zero. Demodulation is simple and inexpensive using a diode-envelope detector.
    *   **Critical Modulation ($\\mu = 1.0$):** The carrier envelope drops to zero exactly at the modulation valleys.
    *   **Over-Modulation ($\\mu > 1$):** The envelope crosses zero, leading to phase reversals and envelope distortion. A simple envelope detector will fail (causing audio clipping/distortion), and complex coherent detection is required.
    
    **Bandwidth of AM:**
    The bandwidth of a standard AM signal is double the message signal frequency:
    $$BW_{AM} = 2 f_m$$
    
    ---
    
    ### 3. Frequency Modulation (FM) Principles
    In **Frequency Modulation**, the instantaneous frequency $f_i(t)$ of the carrier signal is varied linearly in proportion to the message signal $m(t)$.
    
    The instantaneous frequency is:
    $$f_i(t) = f_c + k_f m(t)$$
    where $k_f$ is the frequency sensitivity of the modulator.
    
    Integrating the frequency yields the phase of the carrier:
    $$\\theta(t) = 2\\pi f_c t + 2\\pi k_f \\int_0^t m(\\tau) d\\tau$$
    
    If the message signal is $m(t) = A_m \\cos(2\\pi f_m t)$, the FM wave is:
    $$s(t) = A_c \\cos(2\\pi f_c t + \\beta \\sin(2\\pi f_m t))$$
    where:
    *   $\\Delta f = k_f A_m$ is the **Frequency Deviation** (the peak difference between the instantaneous frequency and the carrier frequency).
    *   $\\beta = \\frac{\\Delta f}{f_m}$ is the **FM Modulation Index**.
    
    **Bandwidth of FM (Carson's Rule):**
    Because FM contains an infinite number of sidebands (Bessel functions), its bandwidth is theoretically infinite. In practice, Carson's Rule estimates the transmission bandwidth containing 98% of the power:
    $$BW_{FM} = 2(\\Delta f + f_m) = 2 f_m (\\beta + 1)$$
    
    ---
    
    ### 4. Comparison Matrix  
    
    | Design Metric | Amplitude Modulation (AM) | Frequency Modulation (FM) |
    | :--- | :--- | :--- |
    | **Noise Immunity** | Poor (Noise directly modulates amplitude) | Excellent (Amplitudes are clipped; frequency is preserved) |
    | **Bandwidth Requirement**| Narrow ($BW = 2 f_m$) | Wide ($BW = 2(\\Delta f + f_m)$) |
    | **Power Efficiency** | Low (Carrier is transmitted and carries no data) | High (Constant envelope power is distributed) |
    | **Equipment Complexity** | Very Low (Diode envelope detector) | Moderate to High (PLLs, Discriminators, VCOs) |
    | **Propagation Mode** | Skywave / Groundwave (Long distances) | Direct line-of-sight VHF/UHF (Short distances) |
    
    ---
    
    ### 5. Practical Engineering Applications
    *   **Amplitude Modulation (AM):**
        *   Standard commercial AM broadcasting (Medium Wave: 535 kHz - 1705 kHz).
        *   Aviation radio communication (VHF: 118 MHz - 137 MHz). AM is selected so that simultaneous signals do not block each other completely, allowing controllers to detect when multiple pilots speak.
        *   Analog television (Vestigial Sideband AM for video delivery).
    *   **Frequency Modulation (FM):**
        *   High-fidelity (Hi-Fi) stereo broadcasting (VHF Band II: 88 MHz - 108 MHz).
        *   Mobile communications (public safety, police, and emergency services).
        *   Audio subcarriers in satellite television.
        *   Frequency Shift Keying (FSK) in digital modems and telemetric networks.
    """)



