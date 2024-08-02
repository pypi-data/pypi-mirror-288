from .base import Analytics_Base
import pandas as pd

def timeseries_integrator(self, column_name="", result_col_name="", multiplier=1, timeseries_integrator=False, filter_condition=""):
    """Integrate a column with delta time or cumsum, separately for filtered and unfiltered data.
    
    Args:
        column_name (str): Column to run the operation on.
        result_col_name (str): Column to return results in the given dataframe.
        multiplier (float64): Value to multiply with the integrated sum.
        timeseries_integrator (bool): Integrate with delta time or perform a cumulative sum.
        filter_condition (str): Condition to filter the DataFrame.

    Returns:
        None
    """
    if not self.check_column(column_name):
        self.log.error("Column not found:[%s]" % (column_name))
        return None
    
    # Integrate for unfiltered data
    self._timeseries_integration(column_name, result_col_name, multiplier, timeseries_integrator)

    # Integrate for filtered data
    if filter_condition:
        filtered_df = self.filter_data(column_name, filter_condition)
        if not filtered_df.empty:
            result_col_name_filtered = result_col_name + "_filtered"
            self._timeseries_integration(filtered_df, result_col_name_filtered, multiplier, timeseries_integrator)
        else:
            self.log.error("No data after applying filter condition")
    else:
        self.log.info("No filter condition provided")

def _timeseries_integration(self, column_name, result_col_name, multiplier, timeseries_integrator):
    """Internal method to perform timeseries integration."""
    if timeseries_integrator:
        if not self._delta_time_compute():
            self.log.error("Failed to compute delta time, check time column: [%s]" % (self.timeseries_column))
            return None
        self.log.info("Performing Timeseries Integration on column with time column: [%s, %s]" % (
            column_name, self.timeseries_column))

        if result_col_name == "":
            result_col_name = column_name + "_integrated"

        self.df[result_col_name] = (
            self.df[column_name] * self.df['delta_time'] * multiplier).cumsum()

    else:
        if result_col_name == "":
            result_col_name = column_name + "_cumsum"
        self.df[result_col_name] = (self.df[column_name] * multiplier).cumsum()

def _delta_time_compute(self):
    """Compute delta time for a given time column."""
    try:
        self.df[self.timeseries_column] = pd.to_datetime(
            self.df[self.timeseries_column])

        # Sort the DataFrame by timestamp (if not already sorted)
        self.df.sort_values(by=self.timeseries_column, inplace=True)

        # Compute the delta time
        self.df['delta_time'] = self.df[self.timeseries_column].diff().dt.total_seconds().astype(float)
        self.df['delta_time'] = self.df['delta_time'].fillna(0)

        self.log.info("Computed Delta Time with mean, max delta time: [%s, %s]" % (
            self.df['delta_time'].mean(), self.df['delta_time'].max()))

        return True

    except Exception as e:
        self.log.debug(e)
        return False

# Dynamically Add the methods to parent Class
Analytics_Base.timeseries_integrator = timeseries_integrator
Analytics_Base._timeseries_integration = _timeseries_integration
Analytics_Base._delta_time_compute = _delta_time_compute
