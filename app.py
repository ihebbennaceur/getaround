import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np


data_url='https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'


### CONFIG
st.set_page_config(
    page_title="Getaround Project",

    layout="wide"
  )

### VIDEO EXPANDER
with st.expander("Getaround intro FR"):
    st.video("https://www.youtube.com/watch?v=dO7KX57xdDQ")
st.markdown("------------------")

st.markdown("""Getaround est une entreprise américaine spécialisée dans l'autopartage. C'est une plateforme mettant en relation propriétaires de véhicules, particuliers comme professionnels, et conducteurs """)

@st.cache_data #to keep the data in cache
# won't have to reload it each time you refresh your app

def load_data(nrows):
    data=pd.read_excel(data_url,nrows=nrows)
    return data

data= load_data(28000)   

## Run the below code if the check is checked ✅
if st.checkbox('Orignal data'):
    st.subheader('Raw data')
    st.write(data)  


### SIDEBAR
st.sidebar.header("Sections")
st.sidebar.markdown("""
    * **Contact**
""")
e = st.sidebar.empty()
e.write("")
st.sidebar.write(". [Iheb ben Naceur](https://fr.linkedin.com/in/ihebbennaceur)")
st.markdown("---")
 
#missing values  replace with 0
data["delay_at_checkout_in_minutes"].fillna(0, inplace=True) 
data['in time or late'] = data["delay_at_checkout_in_minutes"].apply(lambda x : 'Late' if x > 0
                                                     else 'in advance' if (x < 0) 
                                                     else 'in time')

#print new data after changes
st.write(data)

col1, col2 = st.columns(2)

with col1:
    st.metric(label="The number of cars", value=data['car_id'].nunique())

with col2:
    st.metric(label="Number of rentals", value=data['rental_id'].nunique())


st.markdown("")
st.markdown("")
st.markdown("")




st.markdown("as we can see the percentage of  checking type = mobile is represents 80% ")  

fig = px.pie(data, values='rental_id', names="checkin_type", width= 1000, color='checkin_type',color_discrete_map={'mobile':'red','connect':'green'})       
st.plotly_chart(fig, use_container_width=True)

  


checkin_type1 = st.selectbox("Checkin type", ['mobile', 'connect'], key=1)
    
    
 # Calculate statistics based on selected checkin_type
filtered_data = data[data['checkin_type'] == checkin_type1]
stats = filtered_data.groupby(['checkin_type', 'in time or late']).size().reset_index(name='count')
# Calculate percentages
total_counts = stats['count'].sum()
stats['percentage'] = (stats['count'] / total_counts) * 100

st.dataframe(stats)  # Display the statistics as a DataFrame


# Create pie chart for the distribution for column in time or late
fig_pie = px.pie(stats, values='percentage', names='in time or late',
                 title=f"the distribution of '{checkin_type1}' based on the delay at checkout ")
st.plotly_chart(fig_pie, use_container_width=True)



st.markdown("the checkout is quicker when the checking type is connect ")
st.markdown("")

#we will use the select box from above
    
 #  statistics based on selected checkin_type

filtered_data = data[data['checkin_type'] == checkin_type1]

stats2 = filtered_data.groupby(['checkin_type', 'state']).size().reset_index(name='count')
# calculate percentages
total_counts = stats2['count'].sum()
stats['percentage'] = (stats['count'] / total_counts) * 100

st.dataframe(stats2)  # DataFrame




st.markdown("**There are more cancellations with mobile rentals**")
st.markdown(" *** 80% of the checking_type = connect ended thier rentals and 72% of the checking type= mobile ended so we can assume that connect type is more effectivly ***")
st.markdown("")
st.markdown("")



