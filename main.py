import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================================
# 🎨 LAYER 3: CORE APPLICATION CONFIGURATION
# ==========================================================
st.set_page_config(page_title="Enterprise Supply Chain Suite", layout="wide")

# Local hard drive storage path configuration
LOG_FILE_PATH = "operations_ledger.csv"

# Initialize persistent background session memory states
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Background Helper: Load hard drive data back into browser memory smoothly
def load_local_database():
    if os.path.exists(LOG_FILE_PATH):
        return pd.read_csv(LOG_FILE_PATH).to_dict(orient="records")
    return []

if "log_book" not in st.session_state:
    st.session_state.log_book = load_local_database()

# ==========================================================
# 🔒 PANEL A: SECURE LOGIN & RECOVERY CONTROL SHIELD
# ==========================================================
if not st.session_state.authenticated:
    st.title("🔐 Enterprise Portal Authentication")
    st.write("---")
    
    # Core User Accounts Directory Database Registry
    USER_REGISTRY = {
        "admin": {"pass": "uet123", "secret_hint": "University Initial?", "answer": "uet"},
        "hassan": {"pass": "secure786", "secret_hint": "First School Name?", "answer": "uet school"},
        "client": {"pass": "boutique2026", "secret_hint": "Your Brand City?", "answer": "lahore"}
    }
    
    col_login, _ = st.columns([1, 1])
    with col_login:
        username = st.text_input("User Identification ID")
        password = st.text_input("Security Access Code", type="password")
        
        if st.button("🔐 Authorize Access Handshake"):
            if username in USER_REGISTRY and password == USER_REGISTRY[username]["pass"]:
                st.session_state.authenticated = True
                st.success(f"Handshake Established. Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Authentication Failed: Invalid user signature or access keys.")
        
        # 🛡️ THE FORGOT PASSWORD RECOVERY INTERFACE
        st.write("---")
        with st.expander("❓ Forgot Access Code? Initialize System Recovery"):
            st.info("💡 Enter your ID and answer your security matrix question to recover your access key.")
            recovery_user = st.text_input("Enter Target Account ID")
            
            if recovery_user in USER_REGISTRY:
                st.warning(f"**Security Hint:** {USER_REGISTRY[recovery_user]['secret_hint']}")
                security_answer = st.text_input("Enter Secret Recovery Answer", type="password", key="rec_ans")
                
                if st.button("🔓 Verify Recovery Token Key"):
                    if security_answer.strip().lower() == USER_REGISTRY[recovery_user]["answer"].lower():
                        st.success(f"🔑 **Recovery Cleared:** The password for account '{recovery_user}' is: **`{USER_REGISTRY[recovery_user]['pass']}`**")
                    else:
                        st.error("Recovery Verification Failed: Incorrect secret answer patch.")
            elif recovery_user:
                st.error("Account ID not found inside local system registries.")
                
    st.stop()  # Strict block prevents interface dashboard loading if not authenticated

# ==========================================================
# 🧭 PANEL B: MULTI-PAGE WORKSPACE NAVIGATION
# ==========================================================
st.sidebar.title("🏛️ Enterprise Workspace")
st.sidebar.info(f"👤 Operational User: **admin**")
current_page = st.sidebar.radio("Navigate Workspace Modules", [
    "📋 Interactive Cost Matrix", 
    "📖 Operations Log Book"
])

if st.sidebar.button("🚪 Terminate Session"):
    st.session_state.authenticated = False
    st.rerun()

# Master background registry datasets
BAG_REGISTRY = {
    "Pro Backpack": {"base_cost": 2500, "weight_kg": 1.2, "carbon_factor": 1.8},
    "Eco Canvas Tote": {"base_cost": 800, "weight_kg": 0.3, "carbon_factor": 0.5},
    "Heavy Duffle": {"base_cost": 3500, "weight_kg": 2.0, "carbon_factor": 2.5},
    "Urban Messenger": {"base_cost": 1800, "weight_kg": 0.9, "carbon_factor": 1.4}
}
MATERIAL_MULTIPLIERS = {
    "Low (Standard Synthetic)": 1.0,
    "Medium (Reinforced Nylon)": 1.4,
    "Premium (Ballistic Grade)": 2.1
}
FREIGHT_RATE_PER_KG_KM = 0.05

# ==========================================================
# 📦 WORKSPACE MODULE 1: THE CORE MATRIX PANEL
# ==========================================================
if current_page == "📋 Interactive Cost Matrix":
    st.title("🏛️ B2B Supply Chain Cost & Risk Matrix Engine")
    st.markdown("### *Global Enterprise Freight Optimization & Margin Protection Platform*")
    st.write("---")
    
    st.sidebar.write("---")
    st.sidebar.subheader("📦 Configuration Parameters")
    selected_bag = st.sidebar.selectbox("Select Target Product Style", list(BAG_REGISTRY.keys()))
    selected_quality = st.sidebar.selectbox("Select Material Quality Tier", list(MATERIAL_MULTIPLIERS.keys()))
    distance = st.sidebar.slider("Cross-Border Shipping Distance (KM)", 10, 2000, 250, 10)
    
    spec = BAG_REGISTRY[selected_bag]
    multiplier = MATERIAL_MULTIPLIERS[selected_quality]
    
    production_cost = spec["base_cost"] * multiplier
    freight_surcharge = spec["weight_kg"] * distance * FREIGHT_RATE_PER_KG_KM
    total_landed_cost = production_cost + freight_surcharge
    carbon_footprint = spec["carbon_factor"] * (1 + (distance * 0.001))
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Base Production Cost", value=f"PKR {production_cost:,.2f}")
    col2.metric(label="Multi-Mile Freight Surcharge", value=f"PKR {freight_surcharge:,.2f}")
    col3.metric(label="Total Landed Cost", value=f"PKR {total_landed_cost:,.2f}")
    col4.metric(label="Sustainability Footprint", value=f"{carbon_footprint:.2f} kg CO2e")
    
    # 💾 INTERACTIVE HARD DRIVE PERMANENT LEDGER WRITER
    st.write("")
    if st.button("💾 Log Current Calculation to Permanent Ledger"):
        new_entry = {
            "Timestamp": datetime.now().strftime("%I:%M:%S %p"),
            "Product Style": selected_bag,
            "Quality Tier": selected_quality.split(" ("),
            "Distance (KM)": distance,
            "Production Cost (PKR)": round(production_cost, 2),
            "Freight Surcharge (PKR)": round(freight_surcharge, 2),
            "Total Landed Cost (PKR)": round(total_landed_cost, 2)
        }
        st.session_state.log_book.append(new_entry)
        
        # Instantly dump running database list onto cloud/local storage disk
        pd.DataFrame(st.session_state.log_book).to_csv(LOG_FILE_PATH, index=False)
        st.success(f"✅ Calculation safely secured into permanent database disk memory!")

    st.write("---")
    st.subheader("Integrated Supply Chain Multi-Variable Analytics")
    
    # 1. RISK VOLATILITY ENGINE GRAPH (Vertical Labels)
    st.write("#### 🛡️ 1. Logistics Risk Volatility Index")
    risk_factor = 2.5 if distance > 500 else 1.0
    risk_data = {
        "Route Checkpoints": ["Hub A", "Checkpoint B", "Customs C", "Port D", "Final Destination"],
        "Risk Volatility Score": [0.1 * risk_factor, 1.4 * risk_factor, 0.5 * risk_factor, 1.9 * risk_factor, 1.0 * risk_factor]
    }
    st.line_chart(data=risk_data, x="Route Checkpoints", y="Risk Volatility Score", color="#D32F2F")
    
    # 2. LABOR OVERHEAD MATRIX GRAPH (Vertical Labels)
    st.write("#### 👷 2. Operational Labor Overhead Matrix")
    base_labor = production_cost * 0.15
    labor_data = {
        "Route Checkpoints": ["Hub A", "Checkpoint B", "Customs C", "Port D", "Final Destination"],
        "Labor Overhead (PKR)": [base_labor, base_labor * 1.2, base_labor * 0.9, base_labor * 1.5, base_labor]
    }
    st.line_chart(data=labor_data, x="Route Checkpoints", y="Labor Overhead (PKR)", color="#1976D2")
    
    # 3. OVERALL LANDED COST ACCUMULATION GRAPH (Vertical Labels)
    st.write("#### 💰 3. Comprehensive Landed Cost Accumulation")
    overall_data = {
        "Route Checkpoints": ["Hub A", "Checkpoint B", "Customs C", "Port D", "Final Destination"],
        "Total Landed Cost (PKR)": [
            production_cost + (freight_surcharge * 0.2),
            production_cost + (freight_surcharge * 1.5),
            production_cost + (freight_surcharge * 0.4),
            production_cost + (freight_surcharge * 1.8),
            total_landed_cost
        ]
    }
    st.line_chart(data=overall_data, x="Route Checkpoints", y="Total Landed Cost (PKR)", color="#388E3C")

# ==========================================================
# 📖 WORKSPACE MODULE 2: OPERATIONS LOG BOOK VIEW
# ==========================================================
elif current_page == "📖 Operations Log Book":
    st.title("📖 Permanent Operations Log Book")
    st.markdown("### *Hard-Drive Backed Ledger of Supply Chain Matrix Computations*")
    st.write("---")
    
    if len(st.session_state.log_book) == 0:
        st.info("ℹ️ The ledger database is currently empty. Record a calculation from the Matrix panel.")
    else:
        df_log_book = pd.DataFrame(st.session_state.log_book)
        st.write("#### 📄 Database Spreadsheet Records (Saved to Disk)")
        st.dataframe(df_log_book, use_container_width=True)
        
        # Reset button to wipe hard drive storage file
        if st.button("🗑️ Completely Wipe Database File"):
            st.session_state.log_book = []
            if os.path.exists(LOG_FILE_PATH):
                os.remove(LOG_FILE_PATH)
            st.rerun()
