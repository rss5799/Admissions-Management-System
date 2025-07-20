from flask import request

# helper function to apply sorting functionality while filtering
def apply_sorting(df):
    sort_column = request.args.get("sort_by")
    sort_order = request.args.get("order", "asc")

    # Normalize sort_column casing
    if sort_column:
        match = [col for col in df.columns if col.lower() == sort_column.lower()]
        sort_column = match[0] if match else None

    # Apply sorting if column is valid
    if sort_column:
        df = df.sort_values(by=sort_column, ascending=(sort_order == "asc"))

    return df

