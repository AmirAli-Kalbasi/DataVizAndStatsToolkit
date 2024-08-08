import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def advanced_line_plotter(data, col_names, line_settings, point_settings, symbol_settings,
                          title=None, xlabel=None, ylabel=None, fig_size=None, show_points=True,
                          jitter_range=0.1, mean_point_size=10, x_offset=0.5, y_offset = 10, y_symbol_offst = [10,10,10], base_symbols = [r'$\ast$', r'$+$', '\u25B3'] , legend_off=False,
                          category_spacing=1.0):
    """
    Create a line plot with custom distances between points, and add data points with customizable appearance and symbols.

    Parameters:
    - data: A DataFrame with customizable columns for group, category, and value.
    - col_names: Dictionary containing column names for 'group', 'category', and 'value'.
    - line_settings: Dictionary containing settings for lines ('colors', 'linestyles', 'linewidths', 'error_bar_color', 'error_bar_capsize', 'error_bar_capthick', 'error_bar_elinewidth', 'error_bar_orientation').
    - point_settings: Dictionary containing settings for points ('shapes', 'fills', 'edge_colors', 'sizes').
    - symbol_settings: Nested list containing settings for symbols per category per group.
    - title: Dictionary containing 'text' and 'font' keys for the title.
    - xlabel: Dictionary containing 'text' and 'font' keys for the x-axis label.
    - ylabel: Dictionary containing 'text' and 'font' keys for the y-axis label.
    - fig_size: Tuple specifying the size of the figure (width, height).
    - show_points: Boolean to specify whether to show individual data points or not.
    - jitter_range: Float specifying the range of jitter for individual data points.
    - mean_point_size: Integer specifying the size of the mean points.
    - x_offset: Float specifying the offset for the x-axis to create space.
    - legend_off: Boolean to specify whether to show the legend or not.
    - category_spacing: Float specifying the spacing between the x positions of the categories.
    """
    # Extract column names from the dictionary
    group_col = col_names.get('group', 'Group')
    category_col = col_names.get('category', 'Category')
    value_col = col_names.get('value', 'Value')

    # Extract line settings
    line_colors = line_settings.get('colors', ['red', 'green', 'blue'])
    linestyles = line_settings.get('linestyles', ['-', '--', '-.'])
    linewidths = line_settings.get('linewidths', [2, 2, 2])
    error_bar_color = line_settings.get('error_bar_color', ['black', 'black', 'black'])
    error_bar_capsize = line_settings.get('error_bar_capsize', [5, 5, 5])
    error_bar_capthick = line_settings.get('error_bar_capthick', [1, 1, 1])
    error_bar_elinewidth = line_settings.get('error_bar_elinewidth', [2, 2, 2])
    error_bar_orientation = line_settings.get('error_bar_orientation', ['both', 'both', 'both'])

    # Extract point settings
    point_shapes = point_settings.get('shapes', ['o', '^', 's'])
    point_fills = point_settings.get('fills', ['red', 'green', 'blue'])
    point_edge_colors = point_settings.get('edge_colors', ['darkred', 'darkgreen', 'darkblue'])
    point_sizes = point_settings.get('sizes', [50, 50, 50])

    # Extract symbol settings

    symbol_sizes = [14, 14, 14]
    symbol_colors = ['black', 'black', 'black']

    # Map categories to numeric values with custom spacing
    unique_categories = data[category_col].unique()
    category_mapping = {category: idx * category_spacing for idx, category in enumerate(unique_categories)}
    data['CategoryIndex'] = data[category_col].map(category_mapping)

    # Create figure and axis
    if fig_size:
        fig, ax = plt.subplots(figsize=fig_size)
    else:
        fig, ax = plt.subplots(figsize=(7, 4))

    # Function to calculate SEM
    def sem(x):
        return np.std(x) / np.sqrt(len(x))




    if show_points:
      max_vals_per_category = data.groupby(category_col)[value_col].apply(lambda x: max([item for sublist in x for item in sublist])).values
      min_vals_per_category = data.groupby(category_col)[value_col].apply(lambda x: min([item for sublist in x for item in sublist])).values
    else:
      max_vals_per_category = data.groupby(category_col)[value_col].apply(lambda x: max([np.mean(sublist)+sem(sublist) for sublist in x])).values
      min_vals_per_category = data.groupby(category_col)[value_col].apply(lambda x: min([np.mean(sublist)-sem(sublist) for sublist in x])).values

    overall_max_val = np.max(max_vals_per_category)
    overall_min_val = np.min(min_vals_per_category)

    # Plot lines and points for each group
    for i, (group, group_data) in enumerate(data.groupby(group_col)):
        positions = group_data['CategoryIndex'].values
        means = group_data[value_col].apply(np.mean).values
        sems = group_data[value_col].apply(sem).values
        ax.plot(positions, means, color=line_colors[i], linestyle=linestyles[i], linewidth=linewidths[i], label=group)

        # Plot the mean points with error bars and different shapes
        orientation = error_bar_orientation[i]
        if orientation == 'upper':
            errorbars = ax.errorbar(positions, means, yerr=sems, fmt=point_shapes[i], color=line_colors[i], ecolor=error_bar_color[i],
                                    elinewidth=error_bar_elinewidth[i], capsize=0, capthick=error_bar_capthick[i],
                                    markersize=mean_point_size, markerfacecolor=point_fills[i], markeredgecolor=point_edge_colors[i],
                                    lolims=True, uplims=False)
        elif orientation == 'lower':
            errorbars = ax.errorbar(positions, means, yerr=sems, fmt=point_shapes[i], color=line_colors[i], ecolor=error_bar_color[i],
                                    elinewidth=error_bar_elinewidth[i], capsize=0, capthick=error_bar_capthick[i],
                                    markersize=mean_point_size, markerfacecolor=point_fills[i], markeredgecolor=point_edge_colors[i],
                                    lolims=False, uplims=True)
        elif orientation == 'none':
            errorbars = ax.errorbar(positions, means, yerr=sems, fmt=point_shapes[i], color=line_colors[i], ecolor=error_bar_color[i],
                                    elinewidth=error_bar_elinewidth[i], capsize=0, capthick=0,
                                    markersize=mean_point_size, markerfacecolor=point_fills[i], markeredgecolor=point_edge_colors[i],
                                    lolims=True, uplims=True)
        else:
            errorbars = ax.errorbar(positions, means, yerr=sems, fmt=point_shapes[i], color=line_colors[i], ecolor=error_bar_color[i],
                                    elinewidth=error_bar_elinewidth[i], capsize=error_bar_capsize[i], capthick=error_bar_capthick[i],
                                    markersize=mean_point_size, markerfacecolor=point_fills[i], markeredgecolor=point_edge_colors[i])

        for cap in errorbars[1]:
            cap.set_marker('_')
            cap.set_markersize(error_bar_capsize[i])

        if show_points:
            # Plot individual data points for each group
            for _, row in group_data.iterrows():
                jitter = np.linspace(-jitter_range, jitter_range, len(row[value_col]))  # Adjusted jitter range
                for point, k in zip(row[value_col], jitter):
                    ax.scatter(row['CategoryIndex'] + k, point, color=point_fills[i], edgecolor=point_edge_colors[i],
                               s=point_sizes[i], marker=point_shapes[i], zorder=5)

    # Adjust y-limits to ensure symbols fit within the plot
    ylim_upper = overall_max_val + y_offset
    ylim_lower = overall_min_val - y_offset
    ax.set_ylim([ylim_lower, ylim_upper])

    # Add symbols uniformly across all groups above the max value for each category
    for cat_index, cat_symbols in enumerate(symbol_settings):
        current_layer = 0
        for symbol_layer, symbol_count in enumerate(cat_symbols):
            if symbol_count > 0:
                symbols = base_symbols[symbol_layer % len(base_symbols)]
                symbol_text = ''.join([symbols for _ in range(symbol_count)])
                max_val = max_vals_per_category[cat_index]
                symbol_y_offset = max_val + y_symbol_offst[cat_index] + current_layer * 1  # Adjusted symbol offset using current_layer
                ax.text(cat_index * category_spacing, symbol_y_offset, symbol_text, ha='center', va='bottom',
                        fontsize=symbol_sizes[symbol_layer % len(symbol_sizes)], color=symbol_colors[symbol_layer % len(symbol_colors)])
                current_layer += 1

    # Customize x-axis
    ax.set_xticks(np.arange(len(unique_categories)) * category_spacing)
    ax.set_xticklabels(unique_categories, fontproperties=xlabel['font'])
    ax.set_xlabel(xlabel['text'], fontproperties=xlabel['font'])

    # Customize y-axis
    ax.set_ylabel(ylabel['text'], fontproperties=ylabel['font'])

    # Set plot title
    if title:
        ax.set_title(title['text'], fontsize=title['font'].get('size', 16), fontproperties=title['font'])

    # Remove the top and right spines (bounding box)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set the bottom and left spines (x and y lines) to be more visible
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)

    # Adjust x-limits to create space on the left side
    ax.set_xlim([-x_offset, (len(unique_categories) - 1) * category_spacing + x_offset])

    # Show legend if legend_off is False
    if not legend_off:
       plt.legend(loc='upper right', bbox_to_anchor=(1.05, 1), borderaxespad=0., frameon=False)  # Adjusted legend position


    return fig, ax

    # Show plot
    plt.show()

# Example usage
data = pd.DataFrame({
    'Group': ['A', 'A', 'A', 'B', 'B', 'B'],
    'Category': [0, 1, 2, 0, 1, 2],
    'DataPoint': [[6, 7], [9, 8, 10], [55, 10], [19, 18, 21], [24, 23], [29, 28, 30]]  # Example multiple data points
})

# Define column names
col_names = {
    'group': 'Group',
    'category': 'Category',
    'value': 'DataPoint'
}

# Define custom fonts and labels
title = {'text': 'Custom Line Plot', 'font': {'family': 'serif', 'size': 18, 'weight': 'bold'}}
xlabel = {'text': 'Categories', 'font': {'family': 'sans-serif', 'size': 12}}
ylabel = {'text': 'Relative power (%)', 'font': {'family': 'sans-serif', 'size': 12}}

# Define settings
line_settings = {
    'colors': ['black', 'blue', 'red'],
    'linestyles': ['-', '-', '-'],
    'linewidths': [2, 2, 2],
    'error_bar_color': ['black', 'black', 'black'],  # Color of the error bars
    'error_bar_capsize': [10, 10, 10],  # Size of the caps
    'error_bar_capthick': [1, 1, 1],  # Thickness of the caps
    'error_bar_elinewidth': [2, 2, 2],  # Width of the error bar lines
    'error_bar_orientation': ['upper', 'upper', 'both']  # Orientation of the error bars
}

point_settings = {
    'shapes': ['o', '^', 's'],
    'fills': ['black', 'blue', 'red'],
    'edge_colors': ['black', 'blue', 'red'],
    'sizes': [50, 50, 50]
}

# Example symbol settings: Each inner list corresponds to a category
symbol_settings = [
    [1, 0, 1],  # Symbols for category 0
    [2, 0, 1],  # Symbols for category 1
    [1, 1, 0]   # Symbols for category 2
]

# Example: Plot with custom settings, symbols, and labels
advanced_line_plotter(data, col_names, line_settings, point_settings, symbol_settings,
                      title=title, xlabel=xlabel, ylabel=ylabel,
                      fig_size=(8, 6), show_points=False, mean_point_size=10, x_offset=0.5, legend_off=False,
                      category_spacing=0.5)
