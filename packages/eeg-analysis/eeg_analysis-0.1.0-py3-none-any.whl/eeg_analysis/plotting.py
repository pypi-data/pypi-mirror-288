import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_median_across_bands(data, output_dir='plots'):
    """
    Plot median band power across different states for each band and save the plots.

    Parameters:
    - data: DataFrame containing the cleaned data.
    - output_dir: Directory where the plots will be saved.
    """
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Reshape the DataFrame for seaborn
    melted = data.melt(id_vars=['Subject', 'Band'], value_vars=['Before', 'During', 'After'], 
                       var_name='State', value_name='Power')
    
    # Calculate median power for each subject, band, and state
    summary = melted.groupby(['Subject', 'Band', 'State']).agg({'Power': 'median'}).reset_index()
    
    # Get the unique bands
    bands = summary['Band'].unique()
    
    for band in bands:
        # Filter data for the current band
        band_data = summary[summary['Band'] == band]
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        sns.lineplot(x='State', y='Power', hue='Subject', style='Subject', data=band_data, markers=True)
        plt.title(f'Median Power by State for {band} Band')
        plt.xticks(rotation=45)
        plt.legend(title='Subject')
        
        # Save the plot
        plot_filename = os.path.join(output_dir, f'{band}_band_median_power.png')
        plt.savefig(plot_filename)
        plt.close()
