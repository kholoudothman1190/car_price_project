import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('car_price_updated.csv')
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

#setup
st.set_page_config(layout="wide", page_title="Car Price Dashboard")

st.markdown("""
<h1 style='color: #2F4858;'>Car Sales Dashboard: Overview Analysis</h1>
<p style='font-size:16px;'><b>The car price dataset contains detailed information on various vehicles, including their price, brand, 
model, year, transmission, mileage, fuel type, engine size, and condition.This dataset helps identify factors influencing car prices and market trends.</b></p>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("Filters")
brand = st.sidebar.selectbox("Brand", ["All"] + sorted(df["brand"].unique().tolist()))
fuel_type = st.sidebar.selectbox("Fuel Type", ["All"] + sorted(df["fuel_type"].unique().tolist()))
transmission = st.sidebar.selectbox("Transmission", ["All"] + sorted(df["transmission"].unique().tolist()))
condition = st.sidebar.selectbox("Condition", ["All"] + sorted(df["condition"].unique().tolist()))
year = st.sidebar.selectbox("Year", ["All"] + sorted(df["year"].unique().tolist()))
price_range = st.sidebar.slider(
    "Select Price Range",
    float(df["price"].min()),
    float(df["price"].max()),
    (float(df["price"].min()), float(df["price"].max())),
    step=1.0)

#Filters
filtered_df = df.copy()
if brand != "All":
    filtered_df = filtered_df[filtered_df["brand"] == brand]
if fuel_type != "All":
    filtered_df = filtered_df[filtered_df["fuel_type"] == fuel_type] 
if transmission != "All":
    filtered_df = filtered_df[filtered_df["transmission"] == transmission]
if condition != "All":
    filtered_df = filtered_df[filtered_df["condition"] == condition]
if year != "All":
    filtered_df = filtered_df[filtered_df["year"] == year]
filtered_df = filtered_df[(filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1])]


#col
st.markdown("""
<style>
    .metric-card {
        background-color: #F5F7F8;
        padding: 5px;
        margin: 7px 0;
        border-radius: 5px;
        font-size: 10px;
        text-align: center;
        border: 1px solid #D1D5DB;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
        justify-content: center;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""<div class='metric-card'>
    <h5 style='color: #2F4858;'>Total Cars: {len(filtered_df):,}</h5></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='metric-card'>
    <h5 style='color: #2F4858;'>Average Price: ${filtered_df['price'].mean():,.2f} EGP</h5></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class='metric-card'>
    <h5 style='color: #2F4858;'>Average Mileage: {filtered_df['mileage'].mean():,.2f} miles</h5></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='metric-card'>
    <h5 style='color: #2F4858;'>Average Engine Size: {filtered_df['engine_size'].mean():,.2f}</h5></div>""", unsafe_allow_html=True)
    
#tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Distributions", "Brand Analysis", "Condition Analysis", "fuel type Analysis" ,"Year Analysis"])

color_palette = ["#D88C8C", "#E7B9B3", "#BFD7D1", "#6BA3B3", "#2F4858", "#A3C9A8", "#466C76"]

#Distribution
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='font-size:18px;'>Summary Statistics</h4>", unsafe_allow_html=True)
        summary_stats = filtered_df[["price", "mileage", "engine_size"]].describe()
        st.dataframe(summary_stats)
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-size:18px;'>Categorical Analysis</h4>", unsafe_allow_html=True)
        object_columns = df.select_dtypes(include=['object']).nunique().reset_index()
        object_columns.columns = ["Column Name", "Unique Values"]
        st.dataframe(object_columns , width= 315)
    with col2:
        st.plotly_chart(px.histogram(filtered_df, x="price", title="Price Distribution", color_discrete_sequence=[color_palette[0]])
                    .update_layout(margin=dict(l=40, r=40, t=40, b=40)), use_container_width=True)

        st.plotly_chart(px.histogram(filtered_df, x="engine_size", title="Engine Size Distribution", color_discrete_sequence=[color_palette[1]])
                    .update_layout(margin=dict(l=40, r=40, t=40, b=40)), use_container_width=True)

    with col3:
        st.plotly_chart(px.histogram(filtered_df, x="mileage", title="Mileage Distribution", color_discrete_sequence=[color_palette[2]])
                    .update_layout(margin=dict(l=40, r=40, t=40, b=40)), use_container_width=True)

        st.plotly_chart(px.histogram(filtered_df, x="year", title="Year Distribution", color_discrete_sequence=[color_palette[3]])
                    .update_layout(margin=dict(l=40, r=40, t=40, b=40)), use_container_width=True)
#brand
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='font-size:18px;'>Brand Analysis</h4>", unsafe_allow_html=True)
        brand_stats = filtered_df.groupby("brand").agg(
        Average_Price=("price", "mean"),
        Total_Cars=("brand", "count")
        ).reset_index().round(1).sort_values(by="Average_Price", ascending=False)
        st.dataframe(brand_stats , width= 350)
        st.plotly_chart(px.bar(brand_stats, x="brand", y="Average_Price", title="Average price by Brand", color="brand", color_discrete_sequence=color_palette), use_container_width=True)
        st.plotly_chart(px.pie(brand_stats, names="brand", title="Cars numbers by brand", color_discrete_sequence=color_palette), use_container_width=True)
    with col2:
        st.markdown("<h4 style='font-size:18px;'>Brand Analysis</h4>", unsafe_allow_html=True)
        brand_stats = filtered_df.groupby("brand").agg(
        Average_Mileage=("mileage", "mean"),
        Average_Engine_Size=("engine_size", "mean")
        ).reset_index().round(1)
        st.dataframe(brand_stats)
        st.plotly_chart(px.box(filtered_df, x="brand", y="mileage", title="mileage Distribution by Brand", color="brand", color_discrete_sequence=color_palette), use_container_width=True)
        st.plotly_chart(px.scatter(filtered_df, x="brand", y="engine_size", title="engine size vs Brand", color="brand", color_discrete_sequence=color_palette), use_container_width=True)    
        
        
# Condition
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='font-size:18px;'>Condition Analysis</h4>", unsafe_allow_html=True)
        condition_stats = filtered_df.groupby("condition").agg(
        Total_Cars=("condition", "count"),
        Average_Price=("price", "mean")
        ).reset_index().round(3).sort_values(by="Average_Price", ascending=False)
        st.dataframe(condition_stats, width= 350)
        st.plotly_chart(px.bar(condition_stats, x="condition", y="Average_Price", title="Average price by Condition", color="condition", color_discrete_sequence=color_palette), use_container_width=True)
        st.plotly_chart(px.pie(filtered_df, names="condition", title="Cars numbers by Condition", color_discrete_sequence=color_palette), use_container_width=True)
    with col2:
        st.markdown("<h4 style='font-size:18px;'>Condition Analysis</h4>", unsafe_allow_html=True)
        condition_stats = filtered_df.groupby("condition").agg(
        Average_Mileage=("mileage", "mean"),
        Average_Engine_Size=("engine_size", "mean")
        ).reset_index().round(3)
        st.dataframe(condition_stats)
        st.plotly_chart(px.box(filtered_df, x="condition", y="mileage", title="mileage Distribution by Condition", color="condition", color_discrete_sequence=color_palette), use_container_width=True)
        st.plotly_chart(px.scatter(filtered_df, x="condition", y="engine_size", title="Condition vs Price", color="condition", color_discrete_sequence=color_palette), use_container_width=True)

# fuel type
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='font-size:18px;'>Fuel Type Analysis</h4>", unsafe_allow_html=True)
        fuel_stats = filtered_df.groupby("fuel_type").agg(
        Count=("fuel_type", "count"),
        Average_Price=("price", "mean")
        ).reset_index().round(3).sort_values(by="Average_Price", ascending=False)
        st.dataframe(fuel_stats, width= 350)
        st.plotly_chart(px.bar(fuel_stats, x="fuel_type", y="Average_Price", title="Average Price by Fuel Type", color="fuel_type", color_discrete_sequence=color_palette), use_container_width=True)
        st.plotly_chart(px.pie(filtered_df, names="fuel_type", title="Cars numbers by Fuel Type", color_discrete_sequence=color_palette), use_container_width=True)
    with col2:
        st.markdown("<h4 style='font-size:18px;'>Fuel Type Analysis</h4>", unsafe_allow_html=True)
        fuel_stats = filtered_df.groupby("fuel_type").agg(
        Average_Mileage=("mileage", "mean"),
        Average_Engine_Size=("engine_size", "mean")
        ).reset_index().round(3)
        st.dataframe(fuel_stats)
        st.plotly_chart(px.box(filtered_df, x="fuel_type", y="mileage", title="Mileage Distribution by Fuel Type", color="fuel_type", color_discrete_sequence=color_palette), use_container_width=True)
        st.plotly_chart(px.scatter(filtered_df, x="fuel_type", y="engine_size", title="Fuel Type vs Price", color="fuel_type", color_discrete_sequence=color_palette), use_container_width=True)

#year 
with tab5:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='font-size:18px;'>Yearly Sales Analysis</h4>", unsafe_allow_html=True)
        year_stats = filtered_df.groupby("year").agg(
        Total_Cars=("year", "count"),
        Average_Price=("price", "mean")
        ).reset_index().round(1)
        year_stats["year"] = year_stats["year"].astype(str)
        max_avg_price_year = year_stats.loc[year_stats['Average_Price'].idxmax()]
        max_total_cars_year = year_stats.loc[year_stats['Total_Cars'].idxmax()]
        min_avg_price_year = year_stats.loc[year_stats['Average_Price'].idxmin()]
        min_total_cars_year = year_stats.loc[year_stats['Total_Cars'].idxmin()]
        st.markdown(f"**Year with Highest Average Price:** {max_avg_price_year['year']} ($ {max_avg_price_year['Average_Price']:,})")
        st.markdown(f"**Year with Most Cars Sold:** {max_total_cars_year['year']} ({max_total_cars_year['Total_Cars']:,} cars)")
        st.markdown(f"**Year with Lowest Average Price:** {min_avg_price_year['year']} ($ {min_avg_price_year['Average_Price']:,})")
        st.markdown(f"**Year with Least Cars Sold:** {min_total_cars_year['year']} ({min_total_cars_year['Total_Cars']:,} cars)")
        st.dataframe(year_stats, height=290, width=400)
        st.plotly_chart(px.line(year_stats, x="year", y="Total_Cars", title="Total Cars numbers Per Year", markers=True, color_discrete_sequence=[color_palette[0]]), use_container_width=True)
    with col2:
        st.markdown("<h4 style='font-size:18px;'>Yearly Price Trends</h4>", unsafe_allow_html=True)
        st.plotly_chart(px.bar(year_stats, x="year", y="Average_Price", title="Average Car Price Per Year", color_discrete_sequence=[color_palette[5]]), use_container_width=True)
        st.plotly_chart(px.box(filtered_df, x="year", y="price", title="Price Distribution by Year", color_discrete_sequence=[color_palette[6]]), use_container_width=True)
