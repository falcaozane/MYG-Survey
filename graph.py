import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Read data from CSV
data = pd.read_csv('your_data.csv')

# Title and data display using Pandas
st.title("Family Information")
st.write(data)

# Create a countplot using Seaborn for 'Occupation'
st.subheader("Occupation Count")
sns.set_style('whitegrid')
plt.figure(figsize=(8, 6))
sns.countplot(data=data, x='Occupation')
st.pyplot()

# Create a pie chart using Plotly for 'Faith'
st.subheader("Faith Distribution")
faith_counts = data['Faith'].value_counts()
fig_faith = px.pie(names=faith_counts.index, values=faith_counts.values)
st.plotly_chart(fig_faith)

# Create a bar chart for 'Blood Group' using Plotly
st.subheader("Blood Group Distribution")
blood_group_counts = data['Blood Group'].value_counts()
fig_blood_group = px.bar(x=blood_group_counts.index, y=blood_group_counts.values)
st.plotly_chart(fig_blood_group)
