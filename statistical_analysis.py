import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import f_oneway, ttest_rel

def statistical_analysis(df, method, columns):
    # Dynamically identify columns from the dictionary

    group_col = columns.get('group', 'Group')
    comparison_col = columns.get('category', 'Category')
    values_col = columns.get('value', 'Value')


    # Function to perform Tukey's HSD test
    def perform_tukey_hsd(df, comparison_col, group_col, values_col, group_name):
        df_subset = df[df[group_col] == group_name]
        tukey = pairwise_tukeyhsd(endog=df_subset[values_col], groups=df_subset[comparison_col], alpha=0.05)
        return tukey

    # Function to map p-values to significance annotations
    def pvalue_to_annotation(pvalue):
        if pvalue < 0.0001:
            return 4
        elif pvalue < 0.001:
            return 3
        elif pvalue < 0.01:
            return 2
        elif pvalue < 0.05:
            return 1
        else:
            return 0

    # Function to perform one-way ANOVA
    def perform_oneway_anova(df, comparison_col, group_col, values_col, group_name):
        df_subset = df[df[group_col] == group_name]
        compares = [df_subset[df_subset[comparison_col] == compare][values_col].values for compare in df_subset[comparison_col].unique()]
        f_stat, p_value = f_oneway(*compares)
        return f_stat, p_value

    # Function to perform paired t-test
    def perform_paired_ttest(df, comparison_col, group_col, values_col, group_name):
        df_subset = df[df[group_col] == group_name]
        unique_compares = df_subset[comparison_col].unique()
        compare1_values = df_subset[df_subset[comparison_col] == unique_compares[0]][values_col].values
        compare2_values = df_subset[df_subset[comparison_col] == unique_compares[1]][values_col].values
        t_stat, p_value = ttest_rel(compare1_values, compare2_values)
        return t_stat, p_value

    # Groups
    group_names = df[group_col].unique()

    # Collect results in a dictionary for each group
    results = {}
    mean_values = {}
    for group in group_names:
        results[group] = {}
        mean_values[group] = {}
        unique_compares = df[df[group_col] == group][comparison_col].unique()
        if method == '2way':
            tukey_results = perform_tukey_hsd(df, comparison_col, group_col, values_col, group)
            summary = tukey_results.summary().data[1:]  # Skip the header
            for row in summary:
                compare1, compare2, meandiff, p_adj, lower, upper, reject = row
                results[group][f"{compare1} vs {compare2}"] = (meandiff, p_adj)
                mean_values[group][compare1] = df[(df[group_col] == group) & (df[comparison_col] == compare1)][values_col].mean()
                mean_values[group][compare2] = df[(df[group_col] == group) & (df[comparison_col] == compare2)][values_col].mean()
        elif method == '1way':
            df_subset = df[df[group_col] == group]
            if len(unique_compares) == 2:
                t_stat, p_value = perform_paired_ttest(df, comparison_col, group_col, values_col, group)
                results[group][f"{unique_compares[0]} vs {unique_compares[1]}"] = (t_stat, p_value)
                mean_values[group][unique_compares[0]] = df_subset[df_subset[comparison_col] == unique_compares[0]][values_col].mean()
                mean_values[group][unique_compares[1]] = df_subset[df_subset[comparison_col] == unique_compares[1]][values_col].mean()
            else:
                f_stat, p_value = perform_oneway_anova(df, comparison_col, group_col, values_col, group)
                tukey_results = perform_tukey_hsd(df, comparison_col, group_col, values_col, group)
                summary = tukey_results.summary().data[1:]  # Skip the header
                for row in summary:
                    compare1, compare2, meandiff, p_adj, lower, upper, reject = row
                    results[group][f"{compare1} vs {compare2}"] = (meandiff, p_adj)
                    mean_values[group][compare1] = df[(df[group_col] == group) & (df[comparison_col] == compare1)][values_col].mean()
                    mean_values[group][compare2] = df[(df[group_col] == group) & (df[comparison_col] == compare2)][values_col].mean()

    # Convert results to a list of lists based on mean differences
    final_results = {}
    for group, comparisons in results.items():
        unique_compares = df[df[group_col] == group][comparison_col].unique()
        n_categories = len(unique_compares)
        matrix = [[0] * n_categories for _ in range(n_categories)]

        for i in range(n_categories):
            for j in range(n_categories):
                if i != j:
                    compare1 = unique_compares[i]
                    compare2 = unique_compares[j]
                    compare_key = f"{compare1} vs {compare2}" if f"{compare1} vs {compare2}" in comparisons else f"{compare2} vs {compare1}"
                    if compare_key in comparisons:
                        mean_diff, p_adj = comparisons[compare_key]
                        if mean_values[group][compare1] > mean_values[group][compare2]:
                            matrix[i][j] = pvalue_to_annotation(p_adj)
                        else:
                            matrix[i][j] = 0

        final_results[group] = matrix

    return final_results


# Example:
data = pd.DataFrame({
    'Group': ['A', 'A', 'A', 'B', 'B', 'B'],
    'Category': [0, 1, 2, 0, 1, 2],
    'Value': [6, 7, 10, 8, 9, 12]
})

# Define column names and method
col_names = {'group': 'Group', 'category': 'Category', 'value': 'Value'}
method = '1way'

# Analyze data
results = statistical_analysis(data, method, col_names)
print(results)




