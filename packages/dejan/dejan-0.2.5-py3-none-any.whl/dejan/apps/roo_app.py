# apps/roo_app.py

import click
from dejan.roo import get_roo
from datetime import datetime, timedelta
import pandas as pd

@click.command()
@click.argument('date_or_days')
def roo(date_or_days):
    """
    Fetches ROO data for a specific date or for the last 'n' days.

    Usage:
      - dejan roo 2022-07-21  # Fetch ROO data for the specific date
      - dejan roo 7            # Fetch ROO data for the last 7 days
      - dejan roo 30           # Fetch ROO data for the last 30 days
    """
    try:
        # Check if the input is a date in the format 'YYYY-MM-DD'
        try:
            specific_date = datetime.strptime(date_or_days, '%Y-%m-%d').date()
            data = get_roo_data_for_date(specific_date)
        except ValueError:
            # If not a date, assume it's a number of days (7 or 30)
            days = int(date_or_days)
            data = get_roo_data_for_days(days)
        
        if isinstance(data, pd.DataFrame):
            print(data.to_string(index=False))
        else:
            print(f"Error: {data}")
    except Exception as e:
        print(f"Error fetching ROO data: {e}")

def get_roo_data_for_date(specific_date):
    """
    Fetches the ROO data for a specific date.

    :param specific_date: The specific date for which to fetch data.
    :return: A DataFrame with the ROO data.
    """
    # Fetch ROO data from the API (use get_roo or custom logic)
    # Placeholder for API interaction based on the specific date
    # Assuming 'get_roo' returns all data and filtering is done in this function
    data = get_roo(2, as_dataframe=True)  # Change '2' to the appropriate search engine
    data['rooDate'] = pd.to_datetime(data['rooDate']).dt.date
    filtered_data = data[data['rooDate'] == specific_date]
    return filtered_data

def get_roo_data_for_days(days):
    """
    Fetches the ROO data for the last 'n' days.

    :param days: The number of days to look back.
    :return: A DataFrame with the ROO data.
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Fetch ROO data from the API (use get_roo or custom logic)
    data = get_roo(2, as_dataframe=True)  # Change '2' to the appropriate search engine
    data['rooDate'] = pd.to_datetime(data['rooDate']).dt.date
    filtered_data = data[(data['rooDate'] >= start_date) & (data['rooDate'] <= end_date)]
    return filtered_data

if __name__ == "__main__":
    roo()
