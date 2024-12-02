import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_trade_data(file_path):
    # Load and preprocess the data
    data = pd.read_csv(file_path, delimiter=';')
    
    # Filter for both value types we're interested in
    value_filters = ['Dollar', 'WERTA']  # Include both dollar values and percentage changes
    data_filtered = data[data['value_variable_label'].str.contains('|'.join(value_filters), case=False, na=False)]
    
    # Create datetime and handle the conversion
    data_filtered['datetime'] = pd.to_datetime(
        data_filtered['time'].astype(str) + ' ' + data_filtered['1_variable_attribute_label'],
        format='%Y %B',
        errors='coerce'
    )
    
    # Basic data cleaning
    data_filtered = data_filtered.dropna(subset=['datetime'])
    data_filtered['value'] = pd.to_numeric(data_filtered['value'], errors='coerce')
    
    # Separate dollar values and percentage changes
    dollar_data = data_filtered[data_filtered['value_variable_label'].str.contains('Dollar', case=False, na=False)]
    percent_data = data_filtered[data_filtered['value_variable_label'].str.contains('WERTA', case=False, na=False)]
    
    # Analyze both metrics
    results = {
        'dollar': analyze_period_comparison(dollar_data),
        'percentage': analyze_period_comparison(percent_data)
    }
    
    # Visualize results
    create_visualizations(results)
    
    return results

def analyze_period_comparison(data):
    # Split data into periods
    before_feb_2022 = data[data['datetime'] < '2022-03-01']
    after_feb_2022 = data[data['datetime'] >= '2022-03-01']
    
    # Calculate monthly averages
    before_avg = before_feb_2022.groupby('3_variable_attribute_label')['value'].agg(['mean', 'std', 'count'])
    after_avg = after_feb_2022.groupby('3_variable_attribute_label')['value'].agg(['mean', 'std', 'count'])
    
    # Merge periods for comparison
    comparison_df = pd.DataFrame({
        'Before_Mean': before_avg['mean'],
        'Before_Std': before_avg['std'],
        'Before_Count': before_avg['count'],
        'After_Mean': after_avg['mean'],
        'After_Std': after_avg['std'],
        'After_Count': after_avg['count']
    })
    
    # Calculate additional metrics
    comparison_df['Absolute_Change'] = comparison_df['After_Mean'] - comparison_df['Before_Mean']
    comparison_df['Percentage_Change'] = ((comparison_df['After_Mean'] - comparison_df['Before_Mean']) / 
                                        comparison_df['Before_Mean'] * 100)
    
    # Perform statistical tests
    results = {}
    for country in comparison_df.index:
        before_values = before_feb_2022[before_feb_2022['3_variable_attribute_label'] == country]['value']
        after_values = after_feb_2022[after_feb_2022['3_variable_attribute_label'] == country]['value']
        
        # Only perform test if we have enough data points
        if len(before_values) >= 2 and len(after_values) >= 2:
            t_stat, p_value = ttest_ind(before_values, after_values, equal_var=False, nan_policy='omit')
            # Calculate Cohen's d effect size
            pooled_std = np.sqrt((before_values.std()**2 + after_values.std()**2) / 2)
            cohens_d = (after_values.mean() - before_values.mean()) / pooled_std if pooled_std != 0 else np.nan
            
            results[country] = {
                't-statistic': t_stat,
                'p-value': p_value,
                'cohens_d': cohens_d
            }
    
    # Combine statistical results with comparison data
    results_df = pd.DataFrame(results).T
    final_results = pd.concat([comparison_df, results_df], axis=1)
    
    # Add significance levels
    final_results['Significance'] = final_results['p-value'].apply(
        lambda x: '***' if x < 0.001 else ('**' if x < 0.01 else ('*' if x < 0.05 else 'ns'))
    )
    
    return final_results

def create_visualizations(results):
    # Create visualization for dollar values
    plt.figure(figsize=(15, 8))
    
    # Sort by absolute change and get top 15
    top_changes = results['dollar'].sort_values('Absolute_Change', ascending=False).head(15)
    
    # Create grouped bar chart
    x = np.arange(len(top_changes.index))
    width = 0.35
    
    plt.bar(x - width/2, top_changes['Before_Mean'], width, label='Before Feb 2022',
            yerr=top_changes['Before_Std'], capsize=5)
    plt.bar(x + width/2, top_changes['After_Mean'], width, label='After Feb 2022',
            yerr=top_changes['After_Std'], capsize=5)
    
    plt.xlabel('Country')
    plt.ylabel('Average Trade Value (USD)')
    plt.title('Top 15 Countries by Absolute Change in Trade Value')
    plt.xticks(x, top_changes.index, rotation=45, ha='right')
    plt.legend()
    
    # Add significance indicators
    for i, country in enumerate(top_changes.index):
        plt.text(i, max(top_changes.loc[country, ['Before_Mean', 'After_Mean']].max() * 1.1),
                top_changes.loc[country, 'Significance'],
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

# Run the analysis
file_path = 'data/import_volume_data.csv'
results = analyze_trade_data(file_path)

# Display results
print("\nTop 20 Countries by Absolute Change in Dollar Values:")
print(results['dollar'].sort_values('Absolute_Change', ascending=False).head(20)[
    ['Before_Mean', 'After_Mean', 'Absolute_Change', 'Percentage_Change', 'p-value', 'Significance'
    ]].round(2))

print("\nTop 20 Countries by Change in Growth Rate (Percentage):")
print(results['percentage'].sort_values('Absolute_Change', ascending=False).head(20)[
    ['Before_Mean', 'After_Mean', 'Absolute_Change', 'p-value', 'Significance'
    ]].round(2))