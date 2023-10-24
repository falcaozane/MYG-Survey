import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load the CSV file
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

st.title("Parish Education and Data Visualization")

# Specify the file path
file_path = 'MYG-Survey-new.csv'  # Replace with the actual file path

data = load_data(file_path)

# Sidebar for selecting entity to visualize
entity = st.sidebar.selectbox("Select Entity", ["Age", "Village", "Gender", "Parish Education"])

if entity == "Age":
    # Create a histogram for age in specified ranges
    st.subheader("Age Distribution")
    age_ranges = [0, 5, 15, 25, 35, 60, 80, 99, 1000]
    age_labels = ['0-5', '6-15', '16-24', '25-35', '36-60', '61-80', '81-99', '100+']
    data['Age Range'] = pd.cut(data['Age'], age_ranges, labels=age_labels)
    age_distribution = data['Age Range'].value_counts().sort_index()
    st.bar_chart(age_distribution)
    st.write("Count Labels:")
    st.write(age_distribution)

elif entity == "Village":
    # Create a pie chart for village population distribution
    st.subheader("Village Population Distribution")
    village_distribution = data['Village'].value_counts()
    fig = px.pie(values=village_distribution, names=village_distribution.index, title="Village Population Distribution")
    st.plotly_chart(fig)
    st.write("Count Labels:")
    st.write(village_distribution)

elif entity == "Gender":
   # Create a pie chart for gender distribution
    st.subheader("Gender Distribution")
    gender_distribution = data['Gender'].value_counts()
    
    # Define custom colors
    custom_colors = ['#ff7f0e','#1f77b4']  # You can add more colors as needed
    
    fig = px.pie(values=gender_distribution, names=gender_distribution.index, title="Gender Distribution", color_discrete_sequence=custom_colors)
    
    # Add count labels to the pie chart
    fig.update_traces(textinfo='value+percent', textposition='inside', insidetextfont=dict(color='white'))
    
    st.plotly_chart(fig)

elif entity == "Parish Education":
    st.subheader("Parish Education Distribution")
    education_distribution = data['Qualification'].value_counts()
    fig = px.bar(x=education_distribution.index, y=education_distribution.values, labels={'x': 'Qualification', 'y': 'Count'})
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig)
    st.write("Count Labels:")
    st.write(education_distribution)

# Calculate the number of educated people (completed SSC)
educated_count = len(data[data['Qualification'] == 'SSC Completed'])

st.subheader("Distribution of Educated People (Completed SSC)")
st.write(f"Number of educated people (Completed SSC): {educated_count}")

# Use Seaborn for more advanced visualization
st.header("Seaborn Plots")
sns.set(style="whitegrid")

# Example: Count plot for Marital-Status
st.subheader("Count Plot for Marital-Status")

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()
count_plot = sns.countplot(data=data, x="Marital-Status", ax=ax)

# Rotate x-axis labels
count_plot.set_xticklabels(count_plot.get_xticklabels(), rotation=45)

# Display the Seaborn plot using st.pyplot(fig)
st.pyplot(fig)

# Use Plotly for interactive visualization
st.header("Plotly Interactive Plot")

# Example: Pie chart for Blood-Group
fig = px.pie(data, names="Blood-Group", title="Blood Group Distribution")
st.plotly_chart(fig)
