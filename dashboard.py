# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import streamlit as st

st.set_page_config(
    page_title="Retail Resource Allocation",  
    page_icon="public/webgav icon_dark.png", 
    layout="centered", 
    initial_sidebar_state="auto" 
)

st.title("🧠 Retail Resource Allocation Dashboard")
st.markdown("""
### Model Overview

This dashboard runs a Python-based computational model for data-driven resource allocation in retail. The model combines **forecasting**, **optimization**, and **simulation** to support planning for inventory and staffing.

---

### Components

- **Forecasting**: Predicts product demand using **exponential smoothing**.  
""")
st.image("eqtns/exp_mth.png", caption="Exponential Smoothing")
st.markdown("""
- **Optimization**: Uses **linear programming (LP)** to allocate resources efficiently under constraints. 
""")
st.image("eqtns/lp.png", caption="Linear Programming")
st.markdown("""
- **Simulation**: Models store operations over time to evaluate the impact of demand and resource decisions.

---

### Process Flow

1. Load historical sales and resource data  
2. Forecast demand  
3. Allocate stock/staff using LP  
4. Simulate operations  
5. View outputs in plots and metrics

This approach enhances decision-making by improving accuracy, efficiency, and adaptability in resource planning.
""")


if st.button("Run Model"):
    with st.spinner("Running model..."):
        result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)

        if result.returncode == 0:
            st.success("Model ran successfully!")
            stdout_lines = result.stdout.splitlines()
            result_path = None
            plot_path = None
            for line in stdout_lines:
                if "RESULT_FILE::" in line:
                    result_path = line.split("::")[1].strip()
                if "PLOT_FILE::" in line:
                    plot_path = line.split("::")[1].strip()

            if result_path and plot_path:
                # sess state
                st.session_state["result_file"] = result_path
                st.session_state["plot_file"] = plot_path

                st.image(plot_path, caption="Forecast")

                with open(result_path, "rb") as file:
                    st.download_button(
                        label="📄 Download Results File",
                        data=file,
                        file_name=os.path.basename(result_path),
                        mime="text/plain"
                    )

                with open(plot_path, "rb") as img_file:
                    st.download_button(
                        label="🖼️ Download Forecast Plot",
                        data=img_file,
                        file_name=os.path.basename(plot_path),
                        mime="image/png"
                    )

            st.markdown("""
            <div style="
                background-color: #f9f9f9;
                border-left: 4px solid #4CAF50;
                padding: 1rem;
                margin-bottom: 1rem;
                border-radius: 6px;
                font-size: 0.95rem;
                color: black
            ">

            ### Forecasting Results

            A representation of synthetic sales data and corresponding forecasted values for three products—Product A, Product B, and Product C—over a 30-day period.

            The solid lines represent actual daily sales, while the dashed lines indicate the model's forecasted average demand using exponential smoothing. Product B shows the highest variability in sales, while Product C remains relatively stable. The forecasts effectively capture the central trend for each product, providing a basis for resource planning decisions.

            This output supports stock allocation and simulation by providing expected demand levels for future operational periods.

            </div>
            """, unsafe_allow_html=True)

        else:
            st.error("Model failed to run")
            st.text(result.stderr)


st.markdown("""
<hr style="margin-top: 3rem; margin-bottom: 1rem;"/>

<div style='text-align: center; font-size: 0.9rem; color: gray;'>
    © 2025 SOME_GROUP? | BSc Computer Science (NUST) | Supervised by Mr. Taapatsa
</div>
""", unsafe_allow_html=True)
