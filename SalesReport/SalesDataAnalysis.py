import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stat
import streamlit as st

# Create a sidebar
st.sidebar.title("Navigation")

# Define navigation options
nav_options = ["Dataset", "Descriptive Stats", "Inferential Stats", "Visualizations"]

# Create radio buttons with selected option in bold
selected_option = st.sidebar.radio("Select an option", nav_options)
np.random.seed(42)
data = {
'product_id': range(1,21),
'product_name' : [f'Product {i}' for i in range(1,21)],
'category' : np.random.choice(['Electronics','Clothing','Home','Sports'],20 ) ,
'units_sold' : np.random.poisson(lam=20,size=20),
'sale_date' : pd.date_range(start='2023-01-01',periods=20, freq='D')
}
sales_data = pd.DataFrame(data)
# Display content based on the selected option
st.markdown("<h1 style='font-size: 40px'>Sales Data Analysis</h1>", unsafe_allow_html=True)
#st.header("Sales Data Analysis")
descriptive_stats = sales_data['units_sold'].describe()
mean_sales = sales_data['units_sold'].mean()
median_sales = sales_data['units_sold'].median()
mode_sales= sales_data['units_sold'].mode()[0]
variance_sales = sales_data['units_sold'].var()
std_deviation_sales = sales_data['units_sold'].std()
category_stats = sales_data.groupby('category')['units_sold'].agg(['sum','mean','std']).reset_index()
category_stats.columns= ['Category','Total Units Sold','Average Units sold','Standard deviation']
if selected_option == "Dataset":
    st.header("Sales Data")
    sales_data
    #st.write("Dataset data will be displayed here")
elif selected_option == "Descriptive Stats":
    st.header("Descriptive Statistics")
    sales_data.to_csv('sales_data.csv',index=False)
    descriptive_stats
    st.write('\n Statistics Analysis:')
    st.write(f'Mean Units sold : {mean_sales}')
    st.write(f'Median Units sold : {median_sales}')
    st.write(f'Mode units sold : {mode_sales}')
    st.write(f'variance of units sold : {variance_sales}' )
    st.write(f'Standard Deviation of units sold : {std_deviation_sales}')
    st.write('\n Categorical Statistics')
    category_stats
    #st.write("Descriptive stats data will be displayed here")
elif selected_option == "Inferential Stats":
    confidence_level = 0.95
    degress_of_freedom = len(sales_data['units_sold']) - 1
    t_score = stat.t.ppf((1+confidence_level)/2, degress_of_freedom)
    sample_mean= mean_sales
    standard_error= std_deviation_sales / np.sqrt(len(sales_data['units_sold']))
    margin_of_error = t_score * standard_error
    confidence_interval =(sample_mean + margin_of_error ,sample_mean - margin_of_error )
    st.write('\n Confidence interval for the Mean of Units sold. with confidence level = 95% ')
    confidence_interval

    onfidence_level=0.99
    degrees_of_freedom = len(sales_data['units_sold'])-1
    sample_mean=mean_sales
    standard_error= std_deviation_sales / np.sqrt(len(sales_data['units_sold']))
    t_score = stat.t.ppf((1+confidence_level)/2 , degrees_of_freedom)
    margin_of_error = t_score*standard_error
    confidence_interval =(sample_mean-margin_of_error , sample_mean+margin_of_error)
    st.write('\n Confidence interval for the Mean of Units sold. with confidence level = 99% ')
    st.write(confidence_interval)
    # Hypothesis Testing
    #Null hypothesis : Mean units sold is equal to 20
    # alternate hypothesis : Mean units sold is not equal to 20
    t_statisics,p_value = stat.ttest_1samp(sales_data['units_sold'],20)
    st.write(f'\n Hypothesis Testing (t-test):')
    st.write(f'\nT-statistics:{t_statisics},p-value :{p_value}')
    if p_value < 0.05 :
        st.write('Reject the null hypothesis: The mean units sold is significantly different from 20.')
    else:
        st.write('Fail to reject the null hypothesis : The mean units sold is not significantly difference from 20.')
    #st.write("Inferential stats data will be displayed here")
elif selected_option == "Visualizations":
    sns.set_theme(style='whitegrid')
    fig, ax = plt.subplots(figsize=(10,6))
    sns.histplot(sales_data['units_sold'],bins=10,kde=True, ax=ax)
    ax.set_title('Distrubution of units sold')
    ax.set_xlabel('Units sold')
    ax.set_ylabel('Frequencey')
    ax.axvline(mean_sales,color='red',linestyle='--',label='Mean')
    ax.axvline(median_sales,color='blue',linestyle='--',label='Median')
    ax.axvline(mode_sales,color='green',linestyle='--',label='Mode')
    ax.legend()
    st.pyplot(fig)     
    #st.write("Visualizations data will be displayed here")
    fig = plt.figure(figsize=(10,6))
    sns.boxplot(x='category',y='units_sold',data=sales_data)
    plt.title('Boxplot of units sold by category')
    plt.xlabel('Category')
    plt.ylabel('Units sold')
    st.pyplot(fig)

    fig, ax = plt.subplots(2, figsize=(10,10))
    sns.barplot(x='Category',y='Total Units Sold',data=category_stats,ax=ax[0])
    sns.barplot(x='Category',y='Average Units sold',data=category_stats,ax=ax[1])
    st.pyplot(fig)