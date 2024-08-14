import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# GitHub raw file URL (replace with your actual URL)
url = "https://raw.githubusercontent.com/evecoq/4LABO/main/data_export.csv"

# Load the dataset from GitHub
df = pd.read_csv(url, delimiter=',')


#Display the first page with scatter plot
def first_page():
    st.title("Interactive Dashboard: Social, Economic, and Demographic Data Comparison")
    
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    st.subheader("Select variables for the scatter plot")
    x_axis = st.selectbox("Select the X-axis variable", numeric_columns)
    y_axis = st.selectbox("Select the Y-axis variable", numeric_columns)
    size_param = st.selectbox("Select the size variable", numeric_columns)

    #Handle NaN values in the selected size parameter
    df[size_param] = df[size_param].fillna(0.01)

    #Scatter plot
    fig = px.scatter(df, 
                     x=x_axis, 
                     y=y_axis,
                     size=size_param, 
                     color='region',  
                     hover_name='Country_Name',
                     size_max=20,
                     color_continuous_scale=px.colors.sequential.Viridis)

    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        height=600,
        xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig, use_container_width=True)

#Display the map page
def map_page():
    st.title("World Map: Select a Democracy Indicator and Country")

    democracy_columns = [
        "Electoral_Democracy", 
        "Liberal_Democracy", 
        "Participatory_Democracy", 
        "Deliberative_Democracy", 
        "Egalitarian_Democracy"
    ]

    #Dropdown to select a democracy indicator for the map
    selected_democracy = st.selectbox("Select a democracy indicator to visualize on the map", democracy_columns)

    #Create the map using Plotly Express
    fig = px.choropleth(df, 
                        locations="Country_Name",
                        locationmode='country names',
                        color=selected_democracy,
                        hover_name="Country_Name",
                        color_continuous_scale=px.colors.sequential.deep,
                        projection="natural earth")

    fig.update_layout(
        height=600,
        width=1200
    )
    st.plotly_chart(fig, use_container_width=True)

    #Dropdown to select a country
    selected_country = st.selectbox("Select a country to view its data", df['Country_Name'].unique())

    #Filter to get only numeric columns for the gauge
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    #Dropdown to select a column for the gauge
    selected_column = st.selectbox("Select a numeric variable to view as a gauge", numeric_columns)

    #Display the gauge for the selected column
    st.subheader(f"Range of values for the {selected_column} and {selected_country} placement in this range")
    country_data = df[df['Country_Name'] == selected_country]

    if not country_data.empty:
        min_value = df[selected_column].min()
        max_value = df[selected_column].max()
        country_value = country_data[selected_column].values[0]

        #Create gauge chart
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=country_value,
            title={'text': f"{selected_column}"},
            gauge={
                'axis': {'range': [min_value, max_value]},
                'bar': {'color': "darkblue"},
            }
        ))

        #Display gauge
        st.plotly_chart(gauge, use_container_width=True)
    else:
        st.write(f"No data available for {selected_country}")

#Main app navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "World Map"])

if page == "Home":
    first_page()
elif page == "World Map":
    map_page()    
