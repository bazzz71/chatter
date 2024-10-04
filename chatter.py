import pandas as pd

def is_data_stable(data: str, site: str, print_unstable_periods: bool = False) -> str:
    # Load the data into a DataFrame
    df = pd.read_csv(data)
    
    # Convert the Time column to datetime
    df['DateTime'] = pd.to_datetime(df['Time'], format='%d/%m/%Y %H:%M:%S')
    
    # Sort the data by Site and DateTime in ascending order
    df = df.sort_values(by=['Site', 'DateTime'], ascending=[True, True])
    
    # Create previous state and time columns
    df['prev_state'] = df.groupby('Site')['State'].shift(1)
    df['prev_time'] = df.groupby('Site')['DateTime'].shift(1)
    
    # Determine if the state has changed
    df['state_changed'] = df['State'] != df['prev_state']
    df['time_diff'] = df['DateTime'] - df['prev_time']
    
    # Define time threshold for chatter detection (30 seconds)
    time_threshold = pd.Timedelta(seconds=30)
    
    # Identify chatter based on state changes within the time threshold
    df['is_chatter'] = df['state_changed'] & (df['time_diff'] <= time_threshold)

    # Identify stable periods: time differences greater than 30 seconds between "In Operation" and "Off"
    df['is_stable'] = (df['State'] == 'In Operation') & (df['time_diff'] > time_threshold)
    
    # Print the unstable periods if requested
    if print_unstable_periods:
        # Extract the periods of instability (chatter)
        unstable_periods = df[df['is_chatter']]
        print(f"Unstable (chatter) periods for {site}:")
        for _, row in unstable_periods.iterrows():
            print(f"Time: {row['DateTime']}, Previous State: {row['prev_state']}, Current State: {row['State']}, Time Difference: {row['time_diff']}")
    
    # Filter data for the specified site
    df_site = df[df['Site'] == site]
    
    # Calculate the full data window (earliest and latest timestamps)
    start_time = df_site['DateTime'].min()
    end_time = df_site['DateTime'].max()
    
    # Total data window duration (difference between start and end times)
    total_data_window_duration = (end_time - start_time).total_seconds()
    
    # Calculate total time in "In Operation" for stable periods
    df_site['next_time'] = df_site['DateTime'].shift(-1)  # Next time for each row
    
    # Calculate the duration for each row where the sensor was in a stable "In Operation" period
    df_site['operation_duration'] = df_site.apply(
        lambda row: (row['next_time'] - row['DateTime']).total_seconds() 
        if row['State'] == 'In Operation' and not row['is_chatter'] else 0,
        axis=1
    )
    
    # Sum the durations of "In Operation" (excluding chatter)
    total_stable_operation_time = df_site['operation_duration'].sum()

    # Calculate the percentage of time in operation
    operation_percentage = (total_stable_operation_time / total_data_window_duration) * 100 if total_data_window_duration > 0 else 0

    # Convert total time to a more readable format (hours, minutes, seconds)
    total_stable_operation_time_str = str(pd.to_timedelta(total_stable_operation_time, unit='s'))
    total_data_window_duration_str = str(pd.to_timedelta(total_data_window_duration, unit='s'))
    
    # Count the occurrences of chatter
    chatter_count = df_site[df_site['is_chatter']].shape[0]
    
    # Return the stability status, total time in operation, the data window, and the percentage
    stability_status = "stable" if chatter_count == 0 else f"unstable with {chatter_count} chatter occurrences."
    
    return (f"Site: {site} is {stability_status}. Total stable time in 'In Operation': {total_stable_operation_time_str}.\n"
            f"Data window: between {start_time} and {end_time}, total duration: {total_data_window_duration_str}.\n"
            f"Percentage of time in operation: {operation_percentage:.2f}%.")

# Example usage
print(is_data_stable('chatter_example_data.csv', 'Site_001', print_unstable_periods=True))

