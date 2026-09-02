import streamlit as st
import pandas as pd
import plotly.express as px




st.set_page_config(
    page_title="Food Waste Intelligence Analyzer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)




st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f6f8ff 0%, #fff7f0 100%);
}

/* Main heading */
h1 {
    font-weight: 800 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.10);
    border: 1px solid rgba(0,0,0,0.05);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0f5, #f0f7ff);
}

/* Section headings */
h2, h3 {
    color: #333333;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)




@st.cache_data
def load_data():

    df = pd.read_csv("data/cleaned_food_waste_data.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()



st.markdown("""
<div style="
    background: linear-gradient(90deg, #FF6B6B, #FF8E53, #FFD93D);
    padding: 35px;
    border-radius: 22px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
">

<h1 style="color:white; margin-bottom:10px;">
🍽️ Food Waste Intelligence Analyzer
</h1>

<p style="font-size:18px; margin:0;">
Transforming Food Data into Meaningful Insights 📊✨
</p>

</div>
""", unsafe_allow_html=True)




st.sidebar.markdown("# 🎛️ Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore food waste patterns."
)


selected_locations = st.sidebar.multiselect(
    "📍 Select Location",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)


selected_categories = st.sidebar.multiselect(
    "🍽️ Select Food Category",
    options=df["Food_Category"].unique(),
    default=df["Food_Category"].unique()
)


selected_items = st.sidebar.multiselect(
    "🍎 Select Food Item",
    options=df["Food_Item"].unique(),
    default=df["Food_Item"].unique()
)



filtered_df = df[
    (df["Location"].isin(selected_locations))
    &
    (df["Food_Category"].isin(selected_categories))
    &
    (df["Food_Item"].isin(selected_items))
]



st.markdown("## 📊 Key Performance Indicators")


total_produced = filtered_df["Quantity_Produced"].sum()

total_wasted = filtered_df["Quantity_Wasted"].sum()

waste_percentage = (
    total_wasted / total_produced * 100
    if total_produced > 0
    else 0
)

total_financial_loss = filtered_df["Financial_Loss"].sum()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "🍽️ Food Produced",
        f"{total_produced:,.0f}"
    )


with col2:
    st.metric(
        "🗑️ Food Wasted",
        f"{total_wasted:,.0f}"
    )


with col3:
    st.metric(
        "📉 Waste Percentage",
        f"{waste_percentage:.2f}%"
    )


with col4:
    st.metric(
        "💰 Financial Loss",
        f"₹{total_financial_loss:,.0f}"
    )


st.divider()



st.markdown("## 🍽️ Food Waste by Category")


category_waste = (
    filtered_df
    .groupby("Food_Category")["Quantity_Wasted"]
    .sum()
    .reset_index()
    .sort_values("Quantity_Wasted", ascending=False)
)


fig_category = px.bar(
    category_waste,
    x="Food_Category",
    y="Quantity_Wasted",
    color="Food_Category",
    title="Total Food Waste by Category",
    color_discrete_sequence=px.colors.qualitative.Set3
)


fig_category.update_layout(
    showlegend=False,
    template="plotly_white"
)


st.plotly_chart(
    fig_category,
    use_container_width=True
)



st.markdown("## 📍 Food Waste by Location")


location_waste = (
    filtered_df
    .groupby("Location")["Quantity_Wasted"]
    .sum()
    .reset_index()
    .sort_values("Quantity_Wasted", ascending=False)
)


fig_location = px.bar(
    location_waste,
    x="Location",
    y="Quantity_Wasted",
    color="Location",
    title="Food Waste Across Locations",
    color_discrete_sequence=px.colors.qualitative.Pastel
)


fig_location.update_layout(
    showlegend=False,
    template="plotly_white"
)


st.plotly_chart(
    fig_location,
    use_container_width=True
)



st.markdown("## 🍩 Top 10 Most Wasted Food Items")


top_items = (
    filtered_df
    .groupby("Food_Item")["Quantity_Wasted"]
    .sum()
    .reset_index()
    .sort_values("Quantity_Wasted", ascending=False)
    .head(10)
)


fig_items = px.bar(
    top_items,
    x="Quantity_Wasted",
    y="Food_Item",
    orientation="h",
    color="Quantity_Wasted",
    title="Top 10 Most Wasted Food Items",
    color_continuous_scale="Sunset"
)


fig_items.update_layout(
    template="plotly_white",
    yaxis={"categoryorder": "total ascending"}
)


st.plotly_chart(
    fig_items,
    use_container_width=True
)



st.markdown("## 📈 Monthly Food Waste Trend")


monthly_waste = (
    filtered_df
    .groupby(["Month", "Month_Name"])["Quantity_Wasted"]
    .sum()
    .reset_index()
    .sort_values("Month")
)


fig_month = px.line(
    monthly_waste,
    x="Month_Name",
    y="Quantity_Wasted",
    markers=True,
    title="Monthly Food Waste Trend",
    color_discrete_sequence=["#FF6B6B"]
)


fig_month.update_layout(
    template="plotly_white"
)


st.plotly_chart(
    fig_month,
    use_container_width=True
)


st.markdown("## 🌡️ Temperature vs Food Waste")


fig_temperature = px.scatter(
    filtered_df,
    x="Temperature",
    y="Quantity_Wasted",
    color="Food_Category",
    hover_data=[
        "Location",
        "Food_Item",
        "Waste_Percentage"
    ],
    title="Relationship Between Temperature and Food Waste",
    color_discrete_sequence=px.colors.qualitative.Bold
)


fig_temperature.update_layout(
    template="plotly_white"
)


st.plotly_chart(
    fig_temperature,
    use_container_width=True
)


st.markdown("## 👥 Customers vs Food Waste")


fig_customers = px.scatter(
    filtered_df,
    x="Customers",
    y="Quantity_Wasted",
    color="Food_Category",
    hover_data=[
        "Location",
        "Food_Item"
    ],
    title="Relationship Between Customer Volume and Food Waste",
    color_discrete_sequence=px.colors.qualitative.Vivid
)


fig_customers.update_layout(
    template="plotly_white"
)


st.plotly_chart(
    fig_customers,
    use_container_width=True
)



st.markdown("## 💰 Financial Loss by Category")


financial_loss = (
    filtered_df
    .groupby("Food_Category")["Financial_Loss"]
    .sum()
    .reset_index()
    .sort_values("Financial_Loss", ascending=False)
)


fig_loss = px.bar(
    financial_loss,
    x="Food_Category",
    y="Financial_Loss",
    color="Food_Category",
    title="Financial Loss Due to Food Waste",
    color_discrete_sequence=px.colors.qualitative.Prism
)


fig_loss.update_layout(
    showlegend=False,
    template="plotly_white"
)


st.plotly_chart(
    fig_loss,
    use_container_width=True
)



st.markdown("## ⚠️ Food Waste Risk Distribution")


risk_distribution = (
    filtered_df["Waste_Risk"]
    .value_counts()
    .reset_index()
)


risk_distribution.columns = [
    "Waste_Risk",
    "Count"
]


fig_risk = px.pie(
    risk_distribution,
    names="Waste_Risk",
    values="Count",
    title="Distribution of Food Waste Risk Levels",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Set2
)


fig_risk.update_traces(
    textposition="inside",
    textinfo="percent+label"
)


fig_risk.update_layout(
    template="plotly_white"
)


st.plotly_chart(
    fig_risk,
    use_container_width=True
)



st.divider()

st.markdown("## 📄 Filtered Dataset")


st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)



st.markdown("""
<div style="
    text-align:center;
    padding:20px;
    margin-top:30px;
    background:linear-gradient(90deg,#FF6B6B,#FF8E53);
    border-radius:15px;
    color:white;
">

<b> Food Waste Intelligence Analyzer</b><br>


</div>
""", unsafe_allow_html=True)