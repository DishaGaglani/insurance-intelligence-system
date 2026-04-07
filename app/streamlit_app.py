import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Insurance Intelligence System",
    page_icon="💼",
    layout="wide",
)

st.markdown(
    """
    <style>
        .title-band {
            background: #1e3a8a;
            color: #ffffff;
            padding: 0.9rem 1.1rem;
            border-radius: 10px;
            margin-bottom: 0.75rem;
        }
        .title-band h1 {
            margin: 0;
            font-size: 1.8rem;
        }
        .stForm {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem;
        }
        .stFormSubmitButton button {
            background-color: #2563eb;
            color: #ffffff;
            border: none;
            border-radius: 8px;
        }
        .stFormSubmitButton button:hover {
            background-color: #1d4ed8;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="title-band">
        <h1>Insurance Premium Intelligence</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Enter customer details and generate a premium recommendation.")

left_space, center_form, right_space = st.columns([1, 2.2, 1], gap="medium")
with center_form:
    st.subheader("Customer Details")
    with st.form("customer_input_form", clear_on_submit=False):
        identity_a, identity_b = st.columns(2)
        with identity_a:
            customer_name = st.text_input("Customer Name", placeholder="e.g. John Doe")
        with identity_b:
            customer_id = st.text_input("Customer ID", placeholder="e.g. CUST-1024")

        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input("Age", min_value=18, max_value=65, value=30, step=1)
            children = st.number_input("Children", min_value=0, max_value=5, value=1, step=1)
            sex = st.selectbox("Sex", ["male", "female"])
        with c2:
            bmi = st.number_input("BMI", min_value=15.0, max_value=40.0, value=25.0, step=0.1)
            smoker = st.selectbox("Smoker", ["yes", "no"])
            region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

        predict_clicked = st.form_submit_button("Generate Recommendation", type="primary", use_container_width=True)
    st.caption("Submit to calculate risk, loss, and premium.")

if predict_clicked:
    # Simulated model logic (demo)
    smoker_val = 1 if smoker == "yes" else 0
    risk_score = (age * 0.02 + bmi * 0.03 + smoker_val * 0.5)
    risk_score = min(risk_score, 1.0)
    predicted_loss = 2000 + age * 100 + bmi * 80 + smoker_val * 10000
    cluster = 2 if risk_score > 0.6 else 1 if risk_score > 0.3 else 0

    base_premium = 5000
    risk_loading = risk_score * 8000
    loss_loading = predicted_loss * 0.1
    cluster_loading = 2000 if cluster == 2 else 0
    premium = base_premium + risk_loading + loss_loading + cluster_loading

    risk_label = {0: "Low", 1: "Medium", 2: "High"}[cluster]
    risk_msg = {
        0: "Low risk profile. Standard pricing is suitable.",
        1: "Moderate risk profile. Review with regular underwriting checks.",
        2: "High risk profile. Apply strict underwriting and additional checks.",
    }[cluster]

    st.subheader("Recommendation Summary")

    k1, k2, k3 = st.columns(3)
    k1.metric("Risk Score", f"{risk_score:.2f}")
    k2.metric("Predicted Loss", f"₹{int(predicted_loss):,}")
    k3.metric("Premium", f"₹{int(premium):,}")

    st.progress(float(np.clip(risk_score, 0.0, 1.0)))
    st.caption(f"Risk Category: {risk_label}")

    st.markdown("#### Premium Breakdown")
    b1, b2 = st.columns(2)
    with b1:
        st.write(f"- Base Premium: `₹{int(base_premium):,}`")
        st.write(f"- Risk Loading: `₹{int(risk_loading):,}`")
    with b2:
        st.write(f"- Loss Loading: `₹{int(loss_loading):,}`")
        st.write(f"- Cluster Adjustment: `₹{int(cluster_loading):,}`")

    if cluster == 2:
        st.error(risk_msg)
    elif cluster == 1:
        st.warning(risk_msg)
    else:
        st.success(risk_msg)
