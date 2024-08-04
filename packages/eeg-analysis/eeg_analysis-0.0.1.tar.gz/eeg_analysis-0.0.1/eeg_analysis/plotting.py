import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_median_across_bands(data: pd.DataFrame):
    melted = data.melt(id_vars=['Subject', 'Band'], value_vars=['Before', 'During', 'After'], 
                       var_name='State', value_name='Power')
    
    summary = melted.groupby(['Subject', 'Band', 'State']).agg({'Power': 'median'}).reset_index()
    
    bands = summary['Band'].unique()
    
    for band in bands:
        band_data = summary[summary['Band'] == band]
        
        plt.figure(figsize=(12, 8))
        sns.lineplot(x='State', y='Power', hue='Subject', style='Subject', data=band_data, markers=True)
        plt.title(f'Median Power by State for {band} Band')
        plt.xticks(rotation=45)
        plt.legend(title='Subject')
        plt.show()
