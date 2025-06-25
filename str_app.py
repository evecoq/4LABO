import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# GitHub raw file URL (replace with your actual URL)
url = "https://raw.githubusercontent.com/evecoq/4LABO/main/final_export.csv"

# Load the dataset from GitHub
df = pd.read_csv(url, delimiter=';')

# Dictionary mapping column names to labels
column_labels = {
    'Country_Name': 'Country',
    'region': 'Region',
    'Homicide_per_100k': 'Homicide total per 100k',
    'Homicide_F_percentage': 'Homicide percentage females',
    'Homicide_M_percentage': 'Homicide percentage males',
    'Electoral_Democracy': 'Electoral Democracy',
    'Liberal_Democracy': 'Liberal Democracy',
    'Deliberative_Democracy': 'Deliberative Democracy',
    'Participatory_Democracy': 'Participatory Democracy',
    'Egalitarian_Democracy': 'Egalitarian Democracy',
    'Primary_Enrolled_per_K': 'Enrollment ratio primary',
    'Secondary_Low_Enrolled_per_K': 'Students enrolled in lower secondary education (thousands)',
    'Secondary_Up_Enrolled_per_K': 'Students enrolled in upper secondary education (thousands)',
    'Happiness_Score': 'Happiness score',
    'Gdp_per_Capita': 'Gdp per capita',
    'Social_Support': 'Social Support',
    'Healthy_Life_Exp': 'Healthy life expectancy',
    'Freedom_of_Choices': 'Freedom to make life choices',
    'Generosity': 'Perception of generosity',
    'Corruption': 'Perception of corruption',
    'Infant_mortality_per_K': 'Infant mortality for both sexes (per 1k live births)',
    'Increase_Rase_Percent': 'Increase Rase Percent',
    'Life_Exp_Birth_F_Y': 'Life expectancy at birth for females (years)',
    'Life_Exp_Birth_Y': 'Life expectancy at birth for both sexes (years)',
    'Child_per_W': 'Children per women',
    'Life_Exp_Birth_M_Y': 'Life expectancy at birth for males (years)',
    'Population': 'Total population',
    'Area_km2': 'Country area km2',
    'Density_per_km2': 'Population density per km2',
    'Growth_Rate': 'Population Growth Rate',
    'World_Population_Percentage': 'World Population Percentage',
    'Seats_percentage': 'Women seats percentage in parlament',
    'pop_80_plus_male_pct': 'Population ages 80 and above, male (% of male population)',
    'pop_male_pct_total': 'Population, male (% of total population)',
    'adolescent_fertility_rate': 'Adolescent fertility rate (births per 1,000 women ages 15-19)',
    'age_dependency_ratio_pct': 'Age dependency ratio (% of working-age population)',
    'pop_80_plus_female_pct': 'Population, female (% of total population)',
    'pop_female_pct_total': 'Population, female (% of total population)',
    'pop_80_plus_female': 'Population ages 80 and above, female',
    'pop_80_plus_male': 'Population ages 80 and above, male',
    'urban_population': 'Urban population',
    'urban_pop_growth_pct': 'Urban population growth (annual %)',
    'net_migration': 'Net migration',
    'rural_population': 'Rural population',
    'rural_pop_pct_total': 'Rural population (% of total population)',
    'rural_pop_growth_pct': 'Rural population growth (annual %)',
    'birth_rate_crude': 'Birth rate, crude (per 1,000 people)',
    'stillbirths_number': 'Number of stillbirths',
    'basic_sanitation_pct': 'People using at least basic sanitation services (% of population)',
    'death_rate_crude': 'Death rate, crude (per 1,000 people)',
    'unemployment_female_pct': 'Unemployment, female (% of female labor force)',
    'labor_force_total': 'Labor force, total',
    'unemployment_male_pct': 'Unemployment, male (% of male labor force)',
    'alcohol_consumption_liters': 'Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)',
    'death_communicable_pct': 'Cause of death, by communicable diseases and maternal, prenatal and nutrition conditions (% of total)',
    'death_injury_pct': 'Cause of death, by injury (% of total)',
    'death_noncommunicable_pct': 'Cause of death, by non-communicable diseases (% of total)',
    'education_spending_gdp_pct': 'Public spending on education, total (% of GDP)',
    'health_spending_gdp_pct': 'Domestic general government health expenditure (% of GDP)',
    'safe_sanitation_pct': 'People using safely managed sanitation services (% of population)',
    'tuberculosis_incidence_per_100k': 'Incidence of tuberculosis (per 100,000 people)',
    'tobacco_use_pct': 'Prevalence of current tobacco use (% of adults)',
    'nb_terrorist_events': 'Number of terrorist events'
}

st.set_page_config(layout="wide")

#Get the label from the column name
def get_label(column_name):
    return column_labels.get(column_name, column_name)  

#Display the first page with scatter plot
def first_page():
    st.title("Interactive Dashboard: Social, Economic, and Demographic Data Comparison")
    
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    st.subheader("Select variables for the scatter plot")
    x_axis = st.selectbox("Select the X-axis variable", numeric_columns, format_func=get_label)
    y_axis = st.selectbox("Select the Y-axis variable", numeric_columns, format_func=get_label)
    size_param = st.selectbox("Select the size variable", numeric_columns, format_func=get_label)

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
                     color_continuous_scale=px.colors.sequential.Viridis,
                     labels={x_axis: get_label(x_axis), y_axis: get_label(y_axis)}
                     )

    fig.update_layout(
        xaxis_title=get_label(x_axis),
        yaxis_title=get_label(y_axis),
        height=600,
        xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig, use_container_width=True)

#Display the map page
def map_page():
    st.title("World Map: Select a Democracy Indicator")

    democracy_columns = [
        "Electoral_Democracy", 
        "Liberal_Democracy", 
        "Participatory_Democracy", 
        "Deliberative_Democracy", 
        "Egalitarian_Democracy"
    ]

    #Dropdown to select a democracy indicator for the map
    selected_democracy = st.selectbox("Select a democracy indicator to visualize on the map", democracy_columns, format_func=get_label)

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
    selected_column = st.selectbox("Select a numeric variable to view as a gauge", numeric_columns, format_func=get_label)

    #Display the gauge for the selected column
    st.subheader(f"Range of values for the **{get_label(selected_column)}** and {selected_country} placement in this range")
    country_data = df[df['Country_Name'] == selected_country]

    if not country_data.empty:
        min_value = df[selected_column].min()
        max_value = df[selected_column].max()
        country_value = country_data[selected_column].values[0]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=country_value,
                title={'text': get_label(selected_column).replace(", ", ",<br>")},
                gauge={
                    'axis': {'range': [min_value, max_value]},
                    'bar': {'color': "darkblue"},
                }
            ))
            gauge.update_layout(height=300)
            st.plotly_chart(gauge, use_container_width=True)

        with col2:
            df_diff = df[["Country_Name", selected_column]].dropna()
            df_diff["diff"] = abs(df_diff[selected_column] - country_value)
            closest_countries = df_diff.sort_values("diff").head(15)[["Country_Name", selected_column]]
            closest_countries = closest_countries.rename(columns={selected_column: get_label(selected_column)})
            st.write("##### Countries with closest values")
            st.dataframe(closest_countries.set_index("Country_Name"))
    else:
        st.write(f"No data available for {selected_country}")
        
    # Min & Max countries for the selected variable
    min_row = df[df[selected_column] == min_value][['Country_Name', selected_column]].dropna().head(1)
    max_row = df[df[selected_column] == max_value][['Country_Name', selected_column]].dropna().head(1)

    # Rename columns for display
    min_country = min_row.iloc[0]['Country_Name']
    min_val = min_row.iloc[0][selected_column]

    max_country = max_row.iloc[0]['Country_Name']
    max_val = max_row.iloc[0][selected_column]

    # Display under gauge
    st.markdown(f"**Minimum value**: {get_label(selected_column)} = `{min_val}` in **{min_country}**")
    st.markdown(f"**Maximum value**: {get_label(selected_column)} = `{max_val}` in **{max_country}**")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "World Map"])

if page == "Home":
    first_page()
elif page == "World Map":
    map_page() 
