
import os
import pandas as pd


class gtd:
    """
    Various gtd functions:
        - gtd.snake2camel(snake_str)
        - gtd.col_to_str(df, colname, fill_na=False)
        - gtd.col_cast(dataframe, colname, cast_as, fill_na=False)
        - gtd.rename_col(df, current_colname, desired_colname)

    """

    def snake_to_camel(snake_str):
        """convert from snake_case to camelCase"""
        components = snake_str.split('_') 
        return components[0] + ''.join(x.capitalize() for x in components[1:])


    def col_to_str(df, colname, fill_na=False):
        """
        force formating of column to string
        """
        if fill_na:
            df[colname] = df[colname].fillna(fill_na).apply(int)
        df[colname] = df[colname].apply(str)



    def col_cast(dataframe, colname, cast_as, fill_na=False):
        """
        Cast a DataFrame column to a specified type and handle missing values.
        """
        if colname not in dataframe.columns:
            raise KeyError(f"column '{colname}' does not exist in the dataframe.")
        
        if fill_na == 'pd.NA':
            fill_na = pd.NA
        
        if fill_na is not False:
            dataframe.loc[:, colname] = dataframe[colname].fillna(fill_na).astype(cast_as)
        else:

            try:
            
                dataframe.loc[:, colname] = dataframe[colname].astype(cast_as)
                
            except ValueError as e:
                raise ValueError(f"Error casting column '{colname}' to {cast_as}: {e}")


    def rename_col(df, current_colname, desired_colname):
        """
        Convenience function to change column name
        """
        df[colname].rename(columns={current_colname:desired_colname}, inplace=True)
