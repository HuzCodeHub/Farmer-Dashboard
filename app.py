# Importing necessary libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Uploading Dataset
file_path = r"C:\Users\Asus\Desktop\Sample Data Set.xlsx"
df = pd.read_excel(file_path)

# Streamlit App
def main():

    st.set_page_config(
        page_title="Farmer Dashboard ",
        page_icon=":bar_chart:",
        layout="wide"
    )
    st.markdown(
        """
        <style>
            div.block-container {
                padding-top: 1rem;
            }
            h1 {
                color: #FFFFFF;
                text-align: center;
                padding-top: 1rem;
            }
        </style>

        <div class="block-container">
            <h1>Farmer Dashboard🧑‍🌾</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display the dataset
    with st.expander("Farmer Dataset"):
        st.dataframe(df)

    # Sidebar for filtering options
    st.sidebar.subheader("Filter Options")

    # Multi-select for Taluka
    selected_Taluka = st.sidebar.multiselect("Select Talukas:", df['Taluka'].unique())

    # Multi-select for crop
    selected_crop = st.sidebar.multiselect("Select Crop:", df['Crop Name'].unique())

    # Filter the dataframe based on selected Talukas and crop
    filtered_df = df[(df['Taluka'].isin(selected_Taluka)) & (df['Crop Name'].isin(selected_crop))]

    col_1, col_2 = st.columns(2)

    with col_1:
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

    with col_2:
        st.subheader("Comparison of Acre of Land")
        st.bar_chart(filtered_df[['Farmer Name', 'Acre of Land']].set_index('Farmer Name'))

    # Scatter plot
    scatter_plot = alt.Chart(filtered_df).mark_circle().encode(
        x='Farmer Name',
        y='Crop Name',
        size='Acre of Land',
        color='Acre of Land',
        tooltip=['Farmer Name', 'Crop Name', 'Acre of Land']
    ).interactive()

    st.altair_chart(scatter_plot, use_container_width=True)

    # Pie chart for Crop distribution using Plotly
    fig = px.pie(filtered_df, names='Crop Name', title=f'Distribution of Crops in {", ".join(selected_Taluka)} Talukas')

    # Configure the pie chart as circular
    fig.update_traces(textinfo='percent+label', pull=[0.1] * len(filtered_df['Crop Name']))

    # Display the Plotly pie chart
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
