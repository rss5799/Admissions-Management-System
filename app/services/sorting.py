from flask import request

# helper function to apply sorting functionality while filtering
def apply_sorting(df):
    sort_column = request.args.get("sort_by")
    sort_order = request.args.get("order", "asc")

    if sort_column and sort_column in df.columns:
        df = df.sort_values(by=sort_column, ascending=(sort_order == "asc"))

    return df

# Use this if you want to use modular classes instead 
# (and delete the above function)
'''







'''