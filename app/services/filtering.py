
import pandas as pd

# filters student data on the HLSV
class DataFilter:
    def __init__(self, df):
        self.df = df

    def apply(self, field=None, value=None):
        if not field:
            return self.df, None
        if value is None:
            return self.df, self._get_unique_values(field)
        
        df_filtered = self.df[self.df[field] == value]
        return df_filtered, self._get_unique_values(field)

    def _get_unique_values(self, field):
        if field not in self.df.columns:
            return []
        return sorted(self.df[field].dropna().astype(str).unique().tolist())
