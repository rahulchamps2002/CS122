import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('accident_100k.csv')
df = df.dropna()
df = df[df['State'].isin(['CA', 'TX', 'FL', 'NY'])]

df['date'] = pd.to_datetime(df['Weather_Timestamp']).dt.date
df['day_of_week'] = pd.to_datetime(df['Weather_Timestamp']).dt.day_name()

# Task 1:
acc_per_day = df.groupby(['date', 'State']).size().reset_index(name='accident_count')

plt.figure(figsize=(25, 10))
for state, group in acc_per_day.groupby('State'):
    plt.plot(group['date'], group['accident_count'], label=state)

plt.title("Number of Accidents per Day")
plt.xlabel("Date")
plt.ylabel("Accident Count")
plt.legend(title='State')
plt.grid(True)
plt.tight_layout()
plt.savefig('accidents_per_day.png')
plt.show()

# Task 2:
grouped = df.groupby(['day_of_week', 'State']).size().reset_index(name='accident_count')
total_per_state = df['State'].value_counts()
grouped['density'] = grouped.apply(lambda row: row['accident_count'] / total_per_state[row['State']], axis=1)

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot_table = grouped.pivot(index='day_of_week', columns='State', values='density').reindex(days_order)

plt.figure(figsize=(8, 6))
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt=".2f", linewidths=.5)
plt.title("🚗 Accident Density by Day of Week and State")
plt.ylabel("Day of the Week")
plt.xlabel("State")
plt.tight_layout()
plt.savefig('accident_density_heatmap.png')
plt.show()

# Task 3:
weather_conditions = ['Fair', 'Mostly Cloudy', 'Cloudy', 'Clear']
filtered_df = df[df['Weather_Condition'].isin(weather_conditions)]

plt.figure(figsize=(12, 8))
sns.boxplot(
    data=filtered_df,
    x='Weather_Condition',
    y='Severity',
    hue='State',
    showfliers=False
)
plt.title('Accident Severity by Weather Condition and State')
plt.xlabel('Weather Condition')
plt.ylabel('Severity')
plt.legend(title='State')
plt.tight_layout()
plt.savefig('severity_boxplot_weather_state.png')
plt.show()

# Task 4:
plt.figure(figsize=(12, 8))
for state in ['CA', 'TX', 'FL', 'NY']:
    state_data = df[df['State'] == state]
    sns.histplot(state_data['Severity'], label=state, kde=False, bins=range(1, 6), element="step", stat='count')

plt.title('Accident Severity Distribution by State')
plt.xlabel('Severity Level')
plt.ylabel('Frequency')
plt.legend(title='State')
plt.tight_layout()
plt.savefig('histogram_severity_by_state.png')
plt.show()

# Task 5:  Does lower visibility increase accident severity?
df_visibility = df.dropna(subset=['Visibility(mi)', 'Severity'])

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_visibility, x='Visibility(mi)', y='Severity', alpha=0.3)
plt.title('🌫️ Visibility vs. Accident Severity')
plt.xlabel('Visibility (miles)')
plt.ylabel('Accident Severity')
plt.tight_layout()
plt.savefig('visibility_vs_severity.png')
plt.show()
