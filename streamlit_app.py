import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from datetime import date, datetime
import os
# ---------------- SIDEBAR ----------------

st.sidebar.title("💊 Medicine AI")

st.sidebar.markdown("""
### Navigation

🏠 Dashboard  
💊 Medicine Search  
🤖 Demand Prediction  
📊 Analytics  
📜 Prediction History
""")

st.sidebar.divider()

st.sidebar.info(
    "AI-Powered Medicine Shortage & Demand Prediction System"
)
# ---------------- MAIN HEADER ----------------

st.title("💊 AI-Powered Medicine Shortage & Demand Prediction System")

st.markdown(
    """
    <p style='font-size:18px;'>
    Predict medicine demand, identify shortage risks, monitor stock levels,
    and track medicine expiry using Artificial Intelligence.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Medicine Shortage Prediction",
    page_icon="💊",
    layout="wide"
)

st.title("💊 AI-Powered Medicine Shortage & Demand Prediction System")
st.write("Predict medicine demand, shortage risks, and manage medicine data.")

# ---------------- FILE UPLOAD ----------------
st.sidebar.header("📤 Upload Medicine Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# ---------------- LOAD DATA ----------------
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.sidebar.success("Dataset uploaded successfully!")
else:
    data = pd.read_csv("medicine_data.csv")

# ---------------- CHECK REQUIRED COLUMNS ----------------
required_columns = [
    "Medicine_Name",
    "Current_Stock",
    "Sales_Quantity",
    "Demand"
]

missing_columns = [
    col for col in required_columns
    if col not in data.columns
]

if missing_columns:
    st.error(
        f"Missing required columns: {missing_columns}"
    )
    st.stop()

# ---------------- AI MODEL ----------------
X = data[["Current_Stock", "Sales_Quantity"]]
y = data["Demand"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# ---------------- DASHBOARD ----------------
st.subheader("📊 Medicine Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💊 Total Records", len(data))

with col2:
    st.metric(
        "📦 Total Stock",
        int(data["Current_Stock"].sum())
    )

with col3:
    st.metric(
        "📈 Average Demand",
        round(data["Demand"].mean())
    )
    # ---------------- SMART MEDICINE INSIGHTS ----------------
st.subheader("🚨 Smart Medicine Insights")

col1, col2 = st.columns(2)

# Low Stock Medicines
with col1:
    st.markdown("### ⚠️ Low Stock Medicines")

    low_stock = data[data["Current_Stock"] < 150]

    if not low_stock.empty:
        st.dataframe(
            low_stock[
                ["Medicine_Name", "Current_Stock", "Demand"]
            ],
            use_container_width=True
        )
    else:
        st.success("✅ No low stock medicines found!")

# Top High-Demand Medicines
with col2:
    st.markdown("### 📈 Top High-Demand Medicines")

    high_demand = data.sort_values(
        by="Demand",
        ascending=False
    ).head(5)

    st.dataframe(
        high_demand[
            ["Medicine_Name", "Demand", "Current_Stock"]
        ],
        use_container_width=True
    )
    # ---------------- MEDICINE SEARCH ----------------
st.subheader("🔍 Medicine Search & Details")

medicine_list = sorted(data["Medicine_Name"].unique())

selected_medicine = st.selectbox(
    "Select a Medicine",
    medicine_list
)

medicine_details = data[
    data["Medicine_Name"] == selected_medicine
]

st.write(f"### 💊 Details for {selected_medicine}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📦 Current Stock",
        int(medicine_details["Current_Stock"].iloc[-1])
    )

with col2:
    st.metric(
        "📈 Latest Demand",
        int(medicine_details["Demand"].iloc[-1])
    )

with col3:
    st.metric(
        "🛒 Latest Sales",
        int(medicine_details["Sales_Quantity"].iloc[-1])
    )

st.dataframe(
    medicine_details,
    use_container_width=True
)

# ---------------- CHARTS ----------------
st.subheader("📈 Medicine Data Analysis")

chart1 = px.bar(
    data,
    x="Medicine_Name",
    y="Demand",
    color="Medicine_Name",
    title="Medicine Demand Analysis"
)

st.plotly_chart(
    chart1,
    use_container_width=True
)

chart2 = px.bar(
    data,
    x="Medicine_Name",
    y="Current_Stock",
    color="Medicine_Name",
    title="Current Medicine Stock"
)

st.plotly_chart(
    chart2,
    use_container_width=True
)
# ---------------- STOCK VS DEMAND GRAPH ----------------

st.subheader("📊 Current Stock vs Demand")

chart_data = data[
    ["Medicine_Name", "Current_Stock", "Demand"]
]

fig = px.bar(
    chart_data,
    x="Medicine_Name",
    y=["Current_Stock", "Demand"],
    barmode="group",
    title="Medicine Stock vs Demand Comparison"
)

st.plotly_chart(fig, use_container_width=True)
# ---------------- SHORTAGE STATUS CHART ----------------

st.subheader("🚨 Medicine Shortage Status")

shortage_data = data.copy()

shortage_data["Status"] = shortage_data.apply(
    lambda row: "Shortage Risk"
    if row["Demand"] > row["Current_Stock"]
    else "Stock Available",
    axis=1
)

status_count = shortage_data["Status"].value_counts()

fig_status = px.pie(
    values=status_count.values,
    names=status_count.index,
    title="Medicine Shortage Status"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)
# ---------------- TOP 5 HIGH DEMAND GRAPH ----------------

st.subheader("🏆 Top 5 High-Demand Medicines")

top_demand = data.sort_values(
    by="Demand",
    ascending=False
).head(5)

fig_top = px.bar(
    top_demand,
    x="Medicine_Name",
    y="Demand",
    title="Top 5 High-Demand Medicines"
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)
# ---------------- LOW STOCK GRAPH ----------------

st.subheader("⚠️ Low Stock Medicines")

low_stock_chart = data[
    data["Current_Stock"] < 150
]

if not low_stock_chart.empty:

    fig_low = px.bar(
        low_stock_chart,
        x="Medicine_Name",
        y="Current_Stock",
        title="Low Stock Medicines"
    )

    st.plotly_chart(
        fig_low,
        use_container_width=True
    )

else:
    st.success("✅ No Low Stock Medicines Found!")

# ---------------- PREDICTION ----------------
st.subheader("🔮 Predict Medicine Demand")

medicine_name = st.text_input(
    "Medicine Name"
)

current_stock = st.number_input(
    "Current Stock",
    min_value=0,
    value=100
)

sales_quantity = st.number_input(
    "Sales Quantity",
    min_value=0,
    value=50
)

expiry_date = st.date_input(
    "Expiry Date",
    value=date.today()
)

if st.button("🔮 Predict Demand"):

    new_data = pd.DataFrame(
        [[current_stock, sales_quantity]],
        columns=["Current_Stock", "Sales_Quantity"]
    )

    predicted_demand = round(
        model.predict(new_data)[0]
    )

    st.success(
        f"💊 Predicted Demand: {predicted_demand} units"
    )

    # SHORTAGE RISK SCORE
    if predicted_demand > current_stock:
        shortage_amount = predicted_demand - current_stock
        risk_score = round(
            (shortage_amount / predicted_demand) * 100,
            2
        )
    else:
        risk_score = 0

    st.subheader("🚨 Shortage Risk Score")

    st.metric(
        "Risk Percentage",
        f"{risk_score}%"
    )

    if risk_score == 0:
        st.success("🟢 Low Risk: Stock is sufficient.")
    elif risk_score <= 30:
        st.warning("🟠 Medium Risk: Monitor medicine stock.")
    else:
        st.error("🔴 High Risk: Immediate action required!")

    # ---------------- SHORTAGE DETECTION ----------------
    if predicted_demand > current_stock:
        shortage_status = "Shortage Risk"
        shortage = predicted_demand - current_stock
        reorder_quantity = shortage + 20
        
        st.error(
            f"⚠️ SHORTAGE RISK! "
            f"Expected shortage: {shortage} units"
        )

        st.warning(
            f"📦 Recommended Reorder Quantity: "
            f"{reorder_quantity} units"
        )

    else:

        shortage_status = "Stock Sufficient"

        reorder_quantity = 0

        st.success(
            "✅ Stock is sufficient. "
            "No shortage expected."
        )
        # ---------------- EXPIRY ALERT ----------------

st.subheader("📅 Medicine Expiry Alert")

today = pd.Timestamp.today()

expiry_date = pd.to_datetime(expiry_date)

days_left = (expiry_date - today).days

if days_left < 0:
    st.error(f"❌ Medicine Expired! Expired {abs(days_left)} days ago")

elif days_left <= 30:
    st.warning(f"⚠️ Medicine will expire in {days_left} days")

else:
    st.success(f"✅ Medicine is safe. {days_left} days remaining")
    
 # ---------------- EXPIRY CHECK ----------------
    days_left = (
        expiry_date - date.today()
    ).days

    if days_left < 0:

        expiry_status = "Expired"

        st.error(
            "❌ Medicine is already expired!"
        )

    elif days_left <= 7:

        expiry_status = "Critical"

        st.error(
            f"🔴 Critical: "
            f"Expires in {days_left} days!"
        )

    elif days_left <= 30:

        expiry_status = "Warning"

        st.warning(
            f"🟠 Warning: "
            f"Expires in {days_left} days!"
        )

    else:

        expiry_status = "Safe"

        st.success(
            f"🟢 Safe: "
            f"{days_left} days remaining."
        )

    # ---------------- SAVE HISTORY ----------------
    history_data = pd.DataFrame({

        "Timestamp": [
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ],

        "Medicine_Name": [
            medicine_name
        ],

        "Current_Stock": [
            current_stock
        ],

        "Sales_Quantity": [
            sales_quantity
        ],
        "Predicted_Demand": [
            predicted_demand
        ],

        "Shortage_Status": [
            shortage_status
        ],

        "Reorder_Quantity": [
            reorder_quantity
        ],

        "Expiry_Date": [
            expiry_date
        ],

        "Expiry_Status": [
            expiry_status
        ]

    })

    history_file = (
        "prediction_history.csv"
    )

    if os.path.exists(history_file):

        history_data.to_csv(
            history_file,
            mode="a",
            header=False,
            index=False
        )

    else:

        history_data.to_csv(
            history_file,
            index=False
        )

    st.info(
        "💾 Prediction saved successfully!"
    )

# ---------------- PREDICTION HISTORY ----------------
st.subheader("📜 Prediction History")

history_file = "prediction_history.csv"

if os.path.exists(history_file):

    history = pd.read_csv(
        history_file
    )

    st.dataframe(
        history,
        use_container_width=True
    )

    # ---------------- DOWNLOAD ----------------
    st.download_button(

        label="⬇️ Download Prediction History",

        data=history.to_csv(
            index=False
        ),

        file_name="prediction_history.csv",

        mime="text/csv"
    )

    # ---------------- CLEAR HISTORY ----------------
    if st.button("🗑️ Clear Prediction History"):

        os.remove(
            history_file
        )

        st.success(
            "Prediction history cleared successfully!"
        )

        st.rerun()

else:

    st.info(
        "No prediction history available yet."
    )
