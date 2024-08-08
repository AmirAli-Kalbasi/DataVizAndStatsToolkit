# DataVizAndStatsToolkit
DataVizAndStatsToolkit is a universal collection of scripts for advanced data visualization and statistical analysis. The toolkit includes:

- Functions to create highly customizable bar and line plots suitable for professional and publication-quality presentations.
- Tools to combine multiple figures into a cohesive layout, ideal for creating comprehensive visual representations.
- Statistical analysis scripts for performing ANOVA, Tukey's HSD, paired t-tests, and more, with easy-to-interpret results.

Whether you're a researcher, data scientist, or analyst, this toolkit will help you generate insightful visualizations and perform rigorous statistical analyses with ease.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Bar Chart Plotter](#bar-chart-plotter)
  - [Line Chart Plotter](#line-chart-plotter.py)
  - [Combine Figures](#combine-figures.py)
  - [statistical_analysis](#statistical_analysis.py)
- [License](#license)

## Installation

To use these scripts, you'll need to have Python installed along with the required libraries. You can install the necessary libraries using:

```sh
pip install matplotlib pandas numpy statsmodels scipy pillow
```

## advanced_bar_chart_plotter:
Description:
The advanced_bar_chart_plotter module provides a function to create highly customizable and professional-quality bar charts. This function allows users to control various aspects of the bar chart, including bar widths, distances between bars and groups, colors, error bars, data points, and symbols. It is ideal for creating complex research, presentations, and publications visualizations.

Key Features:
Customizable Bar Settings: Adjust bar width, distance, colors, and error bars.
Data Points Integration: Add data points with a customizable appearance.
Symbol Annotations: Include symbols above bars for additional data representation.
Flexible Layout: Supports group and category labels with customizable fonts.
Professional Presentation: Generates plots suitable for experienced and academic use.

## advanced_line_plotter
Description:
The advanced_line_plotter module provides a function to create highly customizable and professional-quality line plots. This function allows users to control various aspects of the line plot, including line styles, colors, data points, error bars, and symbols. It is ideal for creating complex research, presentations, and publications visualizations.

Key Features:
Customizable Line Settings: Adjust line colors, styles, and widths.
Data Points Integration: Add data points with customizable appearance and jittering.
Error Bars: Include error bars with adjustable orientation and appearance.
Symbol Annotations: Add symbols above data points for additional data representation.
Professional Presentation: Generates plots suitable for experienced and academic use.

## combine_figures
Description:
The combine_figures module provides a function to combine multiple matplotlib figures into a single cohesive layout. This function allows users to control the arrangement and appearance of the combined figures, making it ideal for creating comprehensive visual representations for research, presentations, and publications.

Key Features:
Flexible Layout: Arrange figures in customizable rows and columns.
Adjustable Sizes: Specify sizes for each figure to ensure optimal presentation.
Professional Titles: Add titles to each figure with customizable fonts and styles.
High-Quality Output: Generate high-resolution combined figures suitable for publication.


## statistical_analysis
Description:
The statistical_analysis module provides a function to perform various statistical analyses on datasets, including ANOVA, Tukey's HSD test, and paired t-tests. The function returns results in a structured format, making it ideal for extracting meaningful statistical inferences from your data.

Key Features:
ANOVA: Perform one-way ANOVA to analyze differences between group means.
Tukey's HSD Test: Conduct post-hoc comparisons to identify significant differences.
Paired T-Test: Compare means from two related groups.
Significance Annotations: Map p-values to significance levels for easy interpretation.
Structured Results: Output results in a format suitable for further analysis or visualization.
