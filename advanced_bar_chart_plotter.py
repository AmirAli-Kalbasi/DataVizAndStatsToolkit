import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def advanced_bar_chart_plotter(data, col_names, bar_settings, point_settings, symbol_settings, show_labels=None,
                               title=None, xlabel=None, ylabel1=None, ylabel2=None, fig_size=None):
    """
    Create a bar chart with custom bar width and distances between bars and groups,
    and add data points with customizable appearance and fonts.

    Parameters:
    - data: A DataFrame with customizable columns for group, category, and value.
    - col_names: Dictionary containing column names for 'group', 'category', and 'value'.
    - bar_settings: Dictionary containing settings for bars ('width', 'distance', 'group_distance', 'colors', 'edge_colors', 'error_bar_orientation', 'error_bar_color', 'error_bar_capsize', 'error_bar_capthick', 'error_bar_elinewidth').
    - point_settings: Dictionary containing settings for points ('shapes', 'fills', 'edge_colors', 'sizes').
    - symbol_settings: Dictionary containing settings for symbols ('base_symbols', 'symbol_indices', 'sizes', 'colors').
    - show_labels: Boolean indicating whether to show category names below each bar and group names in the middle of categories.
    - title: Dictionary containing 'text' and 'font' keys for the title.
    - xlabel: Dictionary containing 'text' and 'font' keys for the x-axis label.
    - ylabel1: Dictionary containing 'text' and 'font' keys for the primary y-axis label.
    - ylabel2: Dictionary containing 'text' and 'font' keys for the secondary y-axis label.
    - fig_size: Tuple specifying the size of the figure (width, height).
    - return_show: String specifying whether to 'show' the plot or 'return' the figure and axis.
    """
    # Extract column names from the dictionary
    group_col = col_names.get('group', 'Group')
    category_col = col_names.get('category', 'Category')
    value_col = col_names.get('value', 'Value')

    # Extract bar settings
    bar_width = bar_settings.get('width', 0.8)
    bar_distance = bar_settings.get('distance', 0.2)
    group_distance = bar_settings.get('group_distance', 1.0)
    bar_colors = bar_settings.get('colors', ['red', 'green', 'blue'])
    bar_edge_colors = bar_settings.get('edge_colors', ['black', 'black', 'black'])
    error_bar_orientation = bar_settings.get('error_bar_orientation', ['both', 'both', 'both'])
    error_bar_color = bar_settings.get('error_bar_color', ['black', 'black', 'black'])
    error_bar_capsize = bar_settings.get('error_bar_capsize', [5, 5, 5])
    error_bar_capthick = bar_settings.get('error_bar_capthick', [1, 1, 1])
    error_bar_elinewidth = bar_settings.get('error_bar_elinewidth', [2, 2, 2])

    # Extract point settings
    point_shapes = point_settings.get('shapes', ['o', '^', 's'])
    point_fills = point_settings.get('fills', ['red', 'green', 'blue'])
    point_edge_colors = point_settings.get('edge_colors', ['darkred', 'darkgreen', 'darkblue'])
    point_sizes = point_settings.get('sizes', [50, 50, 50])

    # Extract symbol settings
    base_symbols = symbol_settings.get('base_symbols', [[r'$\ast$', r'$+$', '\u25B3'], ['\u25A1', '\u25B3', r'$+$'], [r'$+$', '\u25B3', '\u25A1']])
    symbol_indices = symbol_settings.get('symbol_indices', [[0, 0, 0], [1, 1, 0], [3, 1, 2], [1, 1, 0], [1, 2, 1], [1, 0, 0]])
    symbol_sizes = symbol_settings.get('sizes', [14, 12, 12])
    symbol_colors = symbol_settings.get('colors', ['black', 'black', 'black'])

    # Map categories to numeric values
    category_mapping = {category: idx for idx, category in enumerate(data[category_col].unique())}
    data['CategoryIndex'] = data[category_col].map(category_mapping)

    # Create a position for each bar
    unique_groups = data[group_col].unique()
    unique_categories = data['CategoryIndex'].unique()
    n_categories = len(unique_categories)

    # Calculate positions
    group_positions = {group: i * (n_categories * (bar_width + bar_distance) + group_distance) for i, group in enumerate(unique_groups)}
    data['Position'] = data.apply(lambda row: group_positions[row[group_col]] + row['CategoryIndex'] * (bar_width + bar_distance), axis=1)

    # Create figure and axis
    if fig_size:
        fig, ax = plt.subplots(figsize=fig_size)
    else:
        fig, ax = plt.subplots(figsize=(7, 4))

    # Plot bars
    for i, (group, group_data) in enumerate(data.groupby(group_col)):
        for j, (category, cat_data) in enumerate(group_data.groupby('CategoryIndex')):
            bar_position = group_positions[group] + j * (bar_width + bar_distance)

            # Calculate mean and SEM
            mean_value = np.mean(cat_data[value_col].values[0])
            sem = np.std(cat_data[value_col].values[0]) / np.sqrt(len(cat_data[value_col].values[0]))
            max_value = np.max(cat_data[value_col].values[0])

            # Plot bar
            ax.bar(bar_position, mean_value, color=bar_colors[j], edgecolor=bar_edge_colors[j], width=bar_width)

            # Add error bar based on the orientation setting
            orientation = error_bar_orientation[j % len(error_bar_orientation)]
            color = error_bar_color[j % len(error_bar_color)]
            capsize = error_bar_capsize[j % len(error_bar_capsize)]
            capthick = error_bar_capthick[j % len(error_bar_capthick)]
            elinewidth = error_bar_elinewidth[j % len(error_bar_elinewidth)]

            if orientation == 'upper':
                errorbars = ax.errorbar(bar_position, mean_value, yerr=sem, fmt='none', ecolor=color, elinewidth=elinewidth, capsize=0, capthick=capthick, lolims=True, uplims=False)
            elif orientation == 'lower':
                errorbars = ax.errorbar(bar_position, mean_value, yerr=sem, fmt='none', ecolor=color, elinewidth=elinewidth, capsize=0, capthick=capthick, lolims=False, uplims=True)
            elif orientation == 'none':
                errorbars = ax.errorbar(bar_position, mean_value, yerr=sem, fmt='none', ecolor=color, elinewidth=elinewidth, capsize=0, capthick=0, lolims=True, uplims=True)
            else:
                errorbars = ax.errorbar(bar_position, mean_value, yerr=sem, fmt='none', ecolor=color, elinewidth=elinewidth, capsize=capsize, capthick=capthick)

            for cap in errorbars[1]:
                cap.set_marker('_')
                cap.set_markersize(capsize)

            # Add symbols
            current_layer = 0  # Initialize current layer counter
            for layer, symbol_count in enumerate(symbol_indices[i * n_categories + j]):
                if symbol_count > 0:
                    symbols = base_symbols[layer]
                    symbol_text = ''.join([symbols[layer % len(symbols)] for _ in range(symbol_count)])
                    symbol_y_offset = max_value + 0.3 + current_layer * 2  # Adjusted symbol offset using current_layer
                    ax.text(bar_position, symbol_y_offset, symbol_text, ha='center', va='bottom',
                            fontsize=symbol_sizes[layer % len(symbol_sizes)], color=symbol_colors[layer % len(symbol_colors)], fontproperties=None, weight='bold')
                    current_layer += 1  # Increment the current layer only if a symbol is added


    # Plot data points
    for i, row in data.iterrows():
        jitter = np.linspace(-bar_width/8, bar_width/8, len(row[value_col]))  # Jitter the points horizontally within the bar
        for point, j in zip(row[value_col], jitter):
            ax.scatter(row['Position'] + j, point, color=point_fills[row['CategoryIndex']], edgecolor=point_edge_colors[row['CategoryIndex']],
                       s=point_sizes[row['CategoryIndex']], marker=point_shapes[row['CategoryIndex']], zorder=5)

    # Customize x-axis
    if show_labels:
      ax.set_xticks([group_positions[group] + (n_categories - 1) * (bar_width + bar_distance) / 2 for group in unique_groups])
      ax.set_xticklabels('', fontproperties=xlabel['font'])
    else:
      ax.set_xticks([group_positions[group] + (n_categories - 1) * (bar_width + bar_distance) / 2 for group in unique_groups])
      ax.set_xticklabels(unique_groups, fontproperties=xlabel['font'])
      ax.set_xlabel(xlabel['text'], fontproperties=xlabel['font'])

    # Customize y-axis
    ax.set_ylabel(ylabel1['text'], fontproperties=ylabel1['font'])

    # Add secondary y-axis label on the left side without an axis line
    if ylabel2:
        secondary_label_pos = ax.yaxis.get_label().get_position()
        fig.text(secondary_label_pos[0] + 0.1, 0.5, ylabel2['text'], va='center', ha='right', rotation='vertical', fontsize=ylabel2['font'].get('size', ax.yaxis.get_label().get_size()), fontproperties=ylabel2['font'])

    # Set plot title, ensuring it's above the highest point
    title_position_y = 1.05
    plt.suptitle(title['text'], y=title_position_y, fontsize=title['font'].get('size', 16), fontproperties=title['font'])

    # Remove the top and right spines (bounding box)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set the bottom and left spines (x and y lines) to be more visible
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)

    # Adjust layout to make sure the title is fully visible
    plt.subplots_adjust(left=0.2, top=0.8)

    # Custom y-axis ticks
    y_ticks = ax.get_yticks()
    y_minor_ticks = []
    for i in range(len(y_ticks) - 1):
        step = (y_ticks[i + 1] - y_ticks[i]) / 5
        y_minor_ticks.extend(np.arange(y_ticks[i], y_ticks[i + 1], step))
    ax.set_yticks(y_minor_ticks, minor=True)
    y_min, y_max = ax.get_ylim()

    # Show category names below each bar and group names below them if show_labels is True
    if show_labels:

        for group, group_data in data.groupby(group_col):
            positions = group_data['Position'].unique()
            category_names = group_data[category_col].unique()
            for j, (pos, cat_name) in enumerate(zip(positions, category_names)):
                ax.text(pos, 0, cat_name, ha='center', va='top', fontsize=10, rotation=45)

            mid_position = np.mean(positions)
            ax.text(mid_position, show_labels, group, ha='center', va='top', fontsize=12, fontproperties=xlabel['font'])
    return fig, ax
    plt.show()

# Example usage
data = pd.DataFrame({
    'Group': ['A', 'A', 'A', 'B', 'B', 'B'],
    'Category': ['Cat1', 'Cat2', 'Cat3', 'Cat1', 'Cat2', 'Cat3'],
    'DataPoint': [[6, 7], [9, 8, 10], [55, 10], [19, 18, 21], [24, 23], [29, 28, 30]]  # Example multiple data points
})

# Define column names
col_names = {
    'group': 'Group',
    'category': 'Category',
    'value': 'DataPoint'
}

# Define custom fonts and labels
title = {'text': 'Custom Bar Chart', 'font': {'family': 'serif', 'size': 18, 'weight': 'bold'}}
xlabel = {'text': 'Groups', 'font': {'family': 'sans-serif', 'size': 12}}
ylabel1 = {'text': 'Primary Y-axis', 'font': {'family': 'sans-serif', 'size': 12}}
ylabel2 = {'text': 'Secondary Y-axis', 'font': {'family': 'sans-serif', 'size': 12}}

# Define settings
bar_settings = {
    'width': 0.1,
    'distance': 0.01,
    'group_distance': 0.15,
    'colors': ['white', 'black', 'gray'],
    'edge_colors': ['black', 'black', 'black'],
    'error_bar_orientation': ['upper', 'upper', 'upper'],  # Options are 'upper', 'lower', 'both', 'none'
    'error_bar_color': ['black', 'black', 'black'],  # Color of the error bars
    'error_bar_capsize': [15, 15, 15],  # Size of the caps
    'error_bar_capthick': [2, 2, 2],  # Thickness of the caps
    'error_bar_elinewidth': [2, 2, 2]  # Width of the error bar lines
}

point_settings = {
    'shapes': ['o', 'o', '^'],
    'fills': ['black', 'white', 'black'],
    'edge_colors': ['black', 'black', 'black'],
    'sizes': [20, 20, 20]
}

symbol_settings = {
    'base_symbols': [[r'$\ast$', r'$+$', '\u25B3'],[r'$\ast$', r'$+$', '\u25B3'], [r'$\ast$', r'$+$', '\u25B3']],  # Base symbols for each category
    'symbol_indices': [[0, 0, 0], [0, 0, 1], [3, 1, 2], [1, 1, 0], [1, 2, 1], [1, 0, 0]],  # Indices pointing to the number of symbols
    'sizes': [14, 12, 12],  # Repeated for each group
    'colors': ['black', 'black', 'black']  # Repeated for each group
}

# Example: Plot with custom settings, symbols, and labels
fig1, ax1 = advanced_bar_chart_plotter(data, col_names, bar_settings, point_settings, symbol_settings, show_labels=True,
                                       title=title, xlabel=xlabel, ylabel1=ylabel1, ylabel2=ylabel2,
                                       fig_size=(6, 4))
