from .data_processing import load_data, clean_data
from .plotting import plot_median_across_bands
import pkg_resources

def load_clean_and_plot(filepath: str = None):
    if filepath is None:
        # Use default path to the data file included in the package
        filepath = pkg_resources.resource_filename('eeg_analysis', 'data/id_iskcon_data.csv')
    
    data = load_data(filepath)
    cleaned_data = clean_data(data)
    plot_median_across_bands(cleaned_data)
