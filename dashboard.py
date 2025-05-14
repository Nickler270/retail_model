import os
import subprocess
import sys
import streamlit as st
import pandas as pd
import json

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

# upld
st.markdown("### Upload Data")
uploaded_file = st.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        data = pd.read_csv(uploaded_file)
        st.write("CSV File Loaded:")
        st.dataframe(data.head())  
    elif uploaded_file.type == "application/json":
        data = json.load(uploaded_file)
        st.write("JSON File Loaded:")
        st.json(data)  

if st.button("Run Model"):
    if uploaded_file is None:
        st.warning("No file uploaded, proceeding with random data generation.")
        file_path = None 
    else:
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    with st.spinner("Running model..."):
        result = subprocess.run(
            [sys.executable, "main.py", file_path] if file_path else [sys.executable, "main.py"],
            capture_output=True,
            text=True
        )

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

                st.markdown(f"""
                <div style="
                    background-color: #f9f9f9;
                    border-left: 4px solid #4CAF50;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    border-radius: 6px;
                    font-size: 0.95rem;
                    color: black
                ">

                ### Forecasting Conclusion & Business Implications

                The chart above shows forecasted demand and simulated sales trends over a 30-day period for selected retail products. Demand patterns were generated using historical-style synthetic data, allowing us to evaluate planning strategies even without real-world inputs.

                #### Key Observations:
                - Products with **high and volatile demand** (e.g., fresh goods or daily essentials) require **frequent restocking** and potentially **shorter replenishment cycles** to prevent stockouts.  
                *Action:* Consider dynamic ordering and keeping buffer inventory to handle variability.

                - Products with **moderate and steady demand** benefit from **scheduled procurement** and tighter inventory control.  
                *Action:* Forecasts can be used to reduce excess holding without risking availability.

                - Products showing **low, consistent sales** are ideal for **minimal stock strategies**.  
                *Action:* Biweekly or monthly restocking may suffice, reducing storage and spoilage risk.

                #### Operational Insight:
                This forecasting model enables:
                - Better alignment between **supply and demand**.
                - Reduction in **waste and stockouts**.
                - More efficient **use of storage space and budget**.
                - **Adaptable planning** even when working with incomplete or generated datasets.

                By integrating forecasting and optimization, retail managers can make smarter, data-informed resource decisions that scale across changing sales patterns and unpredictable demand.

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
