# Analog Communication Modulation Simulator

An interactive, high-fidelity engineering laboratory simulator built with Python, Streamlit, and Plotly to demonstrate the fundamentals of **Amplitude Modulation (AM)** and **Frequency Modulation (FM)**.

This simulator replicates the behavior of laboratory signal generators and multi-channel oscilloscopes, allowing engineers, students, and educators to visualize analog modulation patterns in real-time.

---

## 📟 Key Features

*   **Dual Simulation Modes:** Dedicated interactive tabs for both AM and FM simulators.
*   **Oscilloscope-style Visualizations:** Implements stacked 3-channel Plotly charts (Message Signal, Carrier Signal, and Modulated Signal) with shared axes for synced zooming and panning.
*   **Envelope Display:** AM signals show positive and negative boundary envelope traces to visually demonstrate modulation depth states.
*   **Dynamic Equation Substitution:** Renders raw LaTeX mathematical equations that update in real-time to show variables and frequencies substituted with your active parameters.
*   **Real-time Computations:** Live calculation of critical parameters:
    *   **AM:** Modulation Index ($\mu$), Modulation Percentage, Transmission Bandwidth, and Modulation Status (Under, Critical, Over modulation).
    *   **FM:** Modulation Index ($\beta$), Carson's Bandwidth, and Frequency Swing.
*   **Strict Input Validation:** Real-time checking to prevent non-physical configurations (all parameters must be positive; carrier frequency $f_c$ must be strictly greater than message frequency $f_m$).
*   **Comprehensive Theory Manual:** Expandable laboratory reference section containing detailed summaries of mathematical principles, comparisons, and industrial applications.
*   **Interactive Parameters & Reset:** Parameter generator cards equipped with reset callbacks to instantly restore standard defaults.

---

## 🛠️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd analog-communication-modulation-simulator
    ```

2.  **Install Dependencies:**
    Make sure you have Python 3.8+ installed. Install the required visualization and server packages:
    ```bash
    pip install streamlit numpy plotly
    ```

---

## 🚀 Running the App

To run the application, you can execute the main Streamlit script directly or run the provided entry-point launcher:

### Option A: Using the launcher (Convenient)
Run the launcher script:
```bash
python am_gui.py
```

### Option B: Using Streamlit directly
```bash
streamlit run app.py
```

Once started, the server will open the application in your default web browser (usually at `http://localhost:8501`).

---

## ⚙️ Mathematical Formulations

### Amplitude Modulation (AM)
*   **AM Waveform:** $s(t) = [A_c + A_m \cos(2\pi f_m t)] \cos(2\pi f_c t)$
*   **Modulation Index:** $\mu = \frac{A_m}{A_c}$
*   **Transmission Bandwidth:** $BW_{AM} = 2 f_m$

### Frequency Modulation (FM)
*   **FM Waveform:** $s(t) = A_c \cos(2\pi f_c t + \beta \sin(2\pi f_m t))$
*   **Modulation Index:** $\beta = \frac{\Delta f}{f_m}$
*   **Carson's Bandwidth:** $BW_{FM} = 2(\Delta f + f_m)$

---

## 🎨 Design Theme
Built with a sleek, modern **Engineering Laboratory Dark Theme** leveraging:
*   Oscilloscope Dark Background (`#0b0f19`) and Grid Indicators
*   Neon Cyberpunk Highlights (Cyan `#00f0ff` for AM, Magenta `#ff007f` for FM)
*   Custom typography integrating *Orbitron* (headers) and *JetBrains Mono* (metric values and numerical readouts)
