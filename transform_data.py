import pandas as pd

def transform_data(data, group_col, category_col, value_col):
    """
    Transforms the given data into the desired format.

    Parameters:
    data (dict): Dictionary containing data with keys corresponding to group, category, and value columns.
    group_col (str): The name of the column to be used as the group.
    category_col (str): The name of the column to be used as the category.
    value_col (str): The name of the column to be used as the value.

    Returns:
    pd.DataFrame: Transformed DataFrame with columns 'Group', 'Category', and 'DataPoint'.
    """
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Group the data by the specified group and category columns, and aggregate the values into lists
    grouped = df.groupby([group_col, category_col], sort=False)[value_col].apply(list).reset_index()

    # Rename columns to match the desired format
    grouped.rename(columns={group_col: 'Group', category_col: 'Category', value_col: 'DataPoint'}, inplace=True)

    return grouped

'''
# Example usage
data = {
    'group': ['G1', 'G1', 'G1', 'G1', 'G1', 'G1', 'G1', 'G1', 'G1', 'G1', 'G3', 'G3', 'G3', 'G3', 'G3', 'G3', 'G3', 'G3', 'G3', 'G3'],
    'category': ['PreTest', 'PreTest', 'PreTest', 'PreTest', 'PreTest', 'PostTest', 'PostTest', 'PostTest', 'PostTest', 'PostTest', 'PreTest', 'PreTest', 'PreTest', 'PreTest', 'PreTest', 'PostTest', 'PostTest', 'PostTest', 'PostTest', 'PostTest'],
    'value': [2.514314, 76.693249, 82.172950, 37.825574, 19.836951, 115.028152, 33.399374, 38.453926, 111.290791, 70.494726, 69.594363, 44.958743, 46.034314, 72.171554, 6.109105, 83.384743, 44.886817, 115.374077, 93.757062, 0.034183]
}

group_col = 'group'
category_col = 'category'
value_col = 'value'

formatted_df = transform_data(data, group_col, category_col, value_col)
print(formatted_df)
'''
