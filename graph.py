import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load the CSV file
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

st.title("Mulgaon Parish Data Visualization")

# Specify the file path
file_path = 'MYG-Survey-new.csv'  # Replace with the actual file path

data = load_data(file_path)

# Create a histogram for age in specified ranges
st.subheader("Age Distribution")
age_ranges = [0, 5, 15, 25, 35, 60, 80, 99, 1000]
age_labels = ['0-5', '6-15', '16-24', '25-35', '36-60', '61-80', '81-99', '100-150']
data['Age Range'] = pd.cut(data['Age'], age_ranges, labels=age_labels)
age_distribution = data['Age Range'].value_counts().sort_index()
st.bar_chart(age_distribution)
st.write("Count Labels:")
st.write(age_distribution)

# Create a pie chart for village population distribution
st.subheader("Village Population Distribution")
village_distribution = data['Village'].value_counts()
fig = px.pie(values=village_distribution, names=village_distribution.index, title="Village Population Distribution")
st.plotly_chart(fig)
st.write("Count Labels:")
st.write(village_distribution)

# Create a pie chart for gender distribution
st.subheader("Gender Distribution")
gender_distribution = data['Gender'].value_counts()

# Define custom colors
custom_colors = ['#ff7f0e', '#1f77b4']  # You can add more colors as needed

fig = px.pie(values=gender_distribution, names=gender_distribution.index, title="Gender Distribution", color_discrete_sequence=custom_colors)

# Add count labels to the pie chart
fig.update_traces(textinfo='value+percent', textposition='inside', insidetextfont=dict(color='white'))

st.plotly_chart(fig)

st.subheader("Parish Education Distribution")
education_distribution = data['Qualification'].value_counts()
fig = px.bar(x=education_distribution.index, y=education_distribution.values, labels={'x': 'Qualification', 'y': 'Count'})
fig.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig)
st.write("Count Labels:")
st.write(education_distribution)

# Calculate the number of educated people (completed SSC)
#educated_count = len(data[data['Qualification'] == 'SSC Completed'])

#st.subheader("Distribution of Educated People (Completed SSC)")
#st.write(f"Number of educated people (Completed SSC): {educated_count}")

# Use Seaborn for more advanced visualization
st.header("Seaborn Plots")
sns.set(style="whitegrid")

# Example: Count plot for Marital-Status
st.subheader("Count Plot for Marital-Status")

# Define custom colors
custom_colors = ['#1f77b4', '#ff7f0e']  # You can add more colors as needed

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()

# Create the count plot with custom colors
count_plot = sns.countplot(data=data, x="Marital-Status", ax=ax, palette=custom_colors)

# Rotate x-axis labels
count_plot.set_xticklabels(count_plot.get_xticklabels(), rotation=45)

# Display the Seaborn plot using st.pyplot(fig)
st.pyplot(fig)

# Add count labels inside the bars
for p in count_plot.patches:
    count_plot.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                        textcoords='offset points')

# Show the count labels inside the labels for each graph
st.write("Count Labels (Inside the Bars):")
st.pyplot(fig)

# Use Plotly for interactive visualization
st.header("Plotly Interactive Plot")

# Example: Pie chart for Blood-Group
fig = px.pie(data, names="Blood-Group", title="Blood Group Distribution")
st.plotly_chart(fig)
st.write("Almost 32% of Mulgaonkar's don't know their blood group")

# Create a new DataFrame with age and marital status
age_marital_data = data[['Age Range', 'Marital-Status']].copy()

# Filter for married and unmarried individuals
married_data = age_marital_data[age_marital_data['Marital-Status'] == 'Married']
unmarried_data = age_marital_data[age_marital_data['Marital-Status'] == 'Unmarried']

# Group and count married and unmarried individuals by age range
married_counts = married_data['Age Range'].value_counts().reindex(age_labels, fill_value=0)
unmarried_counts = unmarried_data['Age Range'].value_counts().reindex(age_labels, fill_value=0)

# Create a bar graph to show married and unmarried for different age groups
st.subheader("Married and Unmarried Individuals by Age Group")

# Add margin and padding to the figure
fig, ax = plt.subplots(figsize=(12, 8))
plt.margins(x=0.1)  # Add margin to the x-axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Adjust the subplot margins

width = 0.4
x = range(len(age_labels))
ax.bar(x, married_counts, width, label='Married')
ax.bar([i + width for i in x], unmarried_counts, width, label='Unmarried')
ax.set_xlabel('Age Group')
ax.set_ylabel('Count')
ax.set_title('Married and Unmarried Individuals by Age Group')
ax.set_xticks([i + width/2 for i in x])
ax.set_xticklabels(age_labels, rotation=85)
ax.legend()
st.pyplot(fig)

# Create a graph showing population distribution age-group wise for different villages
village_list = data['Village'].unique()
selected_village = st.selectbox("Select a Village", village_list)

if selected_village:
    st.subheader(f"Population Distribution for Age Groups in {selected_village}")
    village_data = data[data['Village'] == selected_village]
    age_village_distribution = village_data['Age Range'].value_counts().reindex(age_labels, fill_value=0)
    st.bar_chart(age_village_distribution)
    st.write("Count Labels:")
    st.write(age_village_distribution)


# Count the number of families
family_counts = data['Head-of-Family'].value_counts()

# Count the number of family members associated with each family head
family_size = data.groupby('Head-of-Family')['Full-Name '].count()

st.subheader("Number of Families and Family Members")

st.write("Number of Families:")
st.write(len(family_counts))

st.write("Number of Family Members Associated with Each Family Head:")
st.write(family_size)

# Create a donut chart of the number of families in each village
village_families = data.groupby('Village')['Head-of-Family'].nunique()
fig = px.pie(names=village_families.index, values=village_families.values, title="Number of Families in Each Village")
fig.update_traces(hole=0.4, pull=[0.05, 0.05, 0.05, 0.05])  # Create a donut chart
st.plotly_chart(fig)


message = """
Special Thanks to : 
Saneal Carneiro 
Alpha Andrades 
Nathan Dias
Zane Falcao
And  all the members of the Mariam Youth Group who have helped to conduct this survey.
Also, a heartfelt thanks  to the youth director Fr.Vijay Almeida, Parish Council members and Sevak Netas  for their cooperation.
"""

st.markdown(message)