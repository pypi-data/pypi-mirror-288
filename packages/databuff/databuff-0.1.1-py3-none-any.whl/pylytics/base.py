import pandas as pd 
import numpy as np
import logging

class Analytics_Base():

    def __init__(self, df=pd.DataFrame(), time_column="", log_level=logging.INFO):

        """initialising class with dataframe
        args:
            df(dataframe): timeseries dataframe
            time_column(str): column name to use as time 
            log_level(logging.level): log level for the class
        """

        self.log = logging.getLogger("analytics-logger")
        self.log.setLevel(log_level)
        self.df = df

        try:
            if not df.empty:
                self.log.info("Running some analysis on the dataframe with columns X Rows:[%s X %s]" % (
                    self.df.shape[0], self.df.shape[1]))
            else:
                self.log.error("Empty Data Frame Provided")

            if not self.check_column(time_column):
                self.log.error("Column not found:[%s]" % (time_column))

            self.timeseries_column = time_column

        except:
            self.log.error("Check the Dataframe")

    def sum_filtered(self, column_name, filter_condition=None):
        if filter_condition:
            filtered_df = self.df.query(filter_condition)
        else:
            filtered_df = self.df
        if column_name not in filtered_df.columns:
            raise KeyError(f"Column '{column_name}' not found in DataFrame.")
        return filtered_df[column_name].sum()

    def subsample_timeseries_custom(self, time_column, interval):
        """
        Perform custom subsampling of time series data based on time intervals using pandas resample.

        Args:
        - time_column: str
            The name of the column containing timestamps or time values.
        - interval: str
            The custom interval for subsampling. Specifies the time frequency for resampling, e.g., '1D' for daily, '1H' for hourly, etc.

        Returns:
        - subsampled_df: DataFrame
            The subsampled time series data.
        """
        try:
            # Convert the time_column to datetime if not already
            self.df[time_column] = pd.to_datetime(self.df[time_column])
            
            # Set the time_column as the index
            self.df.set_index(time_column, inplace=True)
            
            # Perform resampling using the specified interval
            subsampled_df = self.df.resample(interval).first()  # Use 'first' to select the first value in each interval
            
            return subsampled_df
        except Exception as e:
            self.log.error(f"Error occurred while custom subsampling timeseries data: {e}")

    def check_column(self, column_name):
        """check if a given column exists or not
        args:
            self
        """

        if column_name in self.df:
            return True
        else:
            return False

    def __validate_timeseries_df(self):
        """check the timeseries column in the df
        args:
            self
        """
        self.log.debug("Checking for time column")
        timestamp_column_names = [
            "timestamp", 'time_s', "time", "Time", "Time_s", "Timestamp"]

    def max_value(self, column_name="", filter_condition=""):
        """calculate max of a given column
        args:
           column_name(str): column to run operation on
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].max()
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found:[%s]" % (column_name))

            temp = self.df[column_name].max()

            return temp

    def min_value(self, column_name="", filter_condition=""):
        """calculate min of a given column
        args:
            column_name(str): column to run operation on
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].min()
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found:[%s]" % (column_name))

            temp = self.df[column_name].min()

            return temp

    def first_value(self, column_name="", filter_condition=""):
        """calculate first value of a given column
        args:
            column_name(str): column to run operation on
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].iloc[1]
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.info("Column not found:[%s]" % (column_name))
                temp = 0
            else:
                temp = self.df[column_name].iloc[1]

            return temp

    def last_value(self, column_name="", filter_condition=""):
        """calculate last value of a given column
        args:
            column_name(str): column to run operation on
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].iloc[-1]
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.info("Column not found:[%s]" % (column_name))
                temp = 0
            else:
                temp = self.df[column_name].iloc[-1]

            return temp

    def mean_value(self, column_name="", filter_condition=""):
        """calculate mean value of a given column
        args:
            column_name(str): column to run operation on
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].mean()
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found:[%s]" % (column_name))

            temp = self.df[column_name].mean()

            return temp

    def manipulate_column(self, column_name="", result_col_name="", operation="",factor=0,with_cols=False):
        """calculate mean value of a given column
        args:
            column_name(str): column to run operation on
            result_col_name(str): column to return results in the given dataframe
            operation(str): product or add ie * or +
            factor(float64): value to be added or multiplied or divided
        """
        if not self.check_column(column_name):
            self.log.error("Column not found:[%s]" % (column_name))

        if result_col_name == "":
            result_col_name = column_name + "_manipulated"
    
        if not self.check_column(factor):
            factor = eval(factor)
        else:
            factor = self.df[factor]
            

        if operation == "+":
            # __delta_time_compute(self)
            self.log.info(("Performing summation on column with factor: [%s,%s%s]") % (
                column_name, operation, factor))
            self.df[result_col_name] = (self.df[column_name]+factor)
        elif operation == "*":
            self.log.info(("Performing mutiplication on column with factor: [%s,%s%s]") % (
                column_name, operation, factor))
            self.df[result_col_name] = (self.df[column_name]*factor)

    def std_deviation(self, column_name="", filter_condition=""):
        """calculate standard deviation of a given column
        args:
            column_name(str): column to run operation on
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].std()
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found:[%s]" % (column_name))

            temp = self.df[column_name].std()

            return temp

    

    def filter_data(self, column_name="", condition=""):
        """
    Perform conditional filtering on the DataFrame.

    Args:
        column_name (str): Name of the column to run condition on.
        condition (str): Condition to apply, e.g., 'column_name > 5'.

    Returns:
        pandas.DataFrame: Filtered DataFrame.
    """
        if not self.check_column(column_name):
            self.log.error("Column not found: [%s]" % column_name)
            return pd.DataFrame()

        try:
            filtered_df = self.df[self.df.eval(condition)]
            return filtered_df
        except Exception as e:
            self.log.error(f"Error occurred while filtering data: {e}")

        try:
            filtered_df = self.df.query(condition)
            return filtered_df
        except Exception as e:
            self.log.error("Error filtering data: %s" % str(e))
            return pd.DataFrame()

    def timeseries_integrator(self, column_name, multiplier, result_col_name, timeseries_integrator=False, condition=""):
        """
         Integrate a column over time with optional multiplier and condition.
    
        Args:
        column_name (str): Name of the column to integrate.
        multiplier (float): Multiplier for the integration.
        result_col_name (str): Name of the column to store the integrated result.
        timeseries_integrator (bool): Whether to perform timeseries integration.
        condition (str, optional): Condition to filter the DataFrame.

        """
        if timeseries_integrator:
            if condition:
                filtered_df = self.filter_data(column_name, condition)
                integrated_values = filtered_df[column_name].cumsum() * multiplier
                self.df[result_col_name] = integrated_values
            else:
                integrated_values = self.df[column_name].cumsum() * multiplier
                self.df[result_col_name] = integrated_values
        else:
            pass  # If timeseries_integrator is False, do nothing

        
    def delta_time_computation(self):
        """calculate delta time between consecutive timestamps"""

        if not self.check_column(self.timeseries_column):
            self.log.error("Time column not found:[%s]" %
                           (self.timeseries_column))
            return None

        try:
            delta_times = self.df[self.timeseries_column].diff().dropna()
            return delta_times
        except Exception as e:
            self.log.error(
                f"Error occurred while computing delta time: {e}")
            return None
        
    def cumulative_sum(self, column_name="", filter_condition=""):
        """Calculate cumulative sum of a column.
    
    Args:
        column_name (str): Name of the column to run the operation on.
        filter_condition (str): Condition to filter the DataFrame.
    
    Returns:
        pandas.Series or None: Series containing the cumulative sum, or None if no data is available.
    """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                filtered_df['bms_current_A_cumsum'] = filtered_df[column_name].cumsum()
                return filtered_df['bms_current_A_cumsum']
            else:
                self.log.error("No data after applying filter condition")
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found: [%s]" % column_name)

        self.df['bms_current_A_cumsum'] = self.df[column_name].cumsum()
        return self.df['bms_current_A_cumsum']
    
    def calculate_gradient(self, X, Y):
        """
        Calculate the gradient deltaY/deltaX given arrays X and Y.
        
        Parameters:
            X (array-like): Array of independent variable values.
            Y (array-like): Array of dependent variable values.
            
        Returns:
            gradient (array-like): Array of gradient values.
        """
        gradient = []
        for i in range(1, len(X)):
            deltaY = Y[i] - Y[i-1]
            deltaX = X[i] - X[i-1]
            if deltaX != 0:
                gradient.append(deltaY / deltaX)
            else:
                gradient.append(None)  # Avoid division by zero
        return gradient

    def integration_multiplier(self, column_name="", multiplier=1, filter_condition=""):
        """calculate integration of a column with a multiplier
        args:
            column_name(str): column to run operation on
            multiplier(int/float): multiplier to apply
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = (filtered_df[column_name] * multiplier).sum()
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found:[%s]" % (column_name))

            temp = (self.df[column_name] * multiplier).sum()

            return temp

    def std_deviation(self, column_name="", filter_condition=""):
        """calculate standard deviation of a given column
        args:
            column_name(str): column to run operation on
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].std()
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found:[%s]" % (column_name))

            temp = self.df[column_name].std()

            return temp
        
    def std_deviation(self, column_name="", filter_condition=""):
        """calculate standard deviation of a given column
        args:
            column_name(str): column to run operation on
        """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].std()
                del filtered_df
                return temp
            else:
                self.log.error("No data after applying filter condition")
                del filtered_df
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found:[%s]" % (column_name))

            temp = self.df[column_name].std()

            return temp
        
    def quantile(self, column_name="", percentile=0.5, filter_condition=""):
        """calculate Xth quantile of a given column
    args:
        column_name(str): column to run operation on
        percentile(float): percentile to calculate
    """
        if filter_condition:
            filtered_df = self.filter_data(column_name, filter_condition)
            if not filtered_df.empty:
                temp = filtered_df[column_name].quantile(percentile)
                return temp
        
            else:
                self.log.error("No data after applying filter condition")
                return None
        else:
            if not self.check_column(column_name):
                self.log.error("Column not found:[%s]" % (column_name))
                return None
            
            temp = self.df[column_name].quantile(percentile)
            return temp

    def filter_data(self, column_name="", condition=""):
        """perform conditional filtering on the DataFrame
        args:
            column_name(str): column to run condition on
            condition(str): condition to apply, e.g., 'column_name > 5'
        """
        if not self.check_column(column_name):
            self.log.error("Column not found:[%s]" % (column_name))

        try:
            filtered_df = self.df[self.df.eval(condition)]
            return filtered_df
        except Exception as e:
            self.log.error(f"Error occurred while filtering data: {e}")

    def XX(self):
        """Placeholder for XX metric"""
        pass

    def YY(self):
        """Placeholder for YY metric"""
        pass

    def get_data(self):
        return self.df

