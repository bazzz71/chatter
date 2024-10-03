import pandas as pd

def is_data_stable(data: str, site: str, print_unstable_periods: bool = False) -> str:
    # Load the data into a DataFrame
    df = pd.read_csv(data)
    
    # Convert the Time column to datetime
    df['DateTime'] = pd.to_datetime(df['Time'], format='%d/%m/%Y %H:%M:%S')
    
    # Sort data by Site and DateTime
    df = df.sort_values(by=['Site', 'DateTime'])
    
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

    # Count the occurrences of chatter for the specified site
    chatter_count = df[(df['Site'] == site) & (df['is_chatter'])].shape[0]

    # Print the unstable periods if requested
    if print_unstable_periods and chatter_count > 0:
        # Extract the periods of instability
        unstable_periods = df[(df['Site'] == site) & (df['is_chatter'])]
        print(f"Unstable periods for {site}:")
        for _, row in unstable_periods.iterrows():
            print(f"Time: {row['DateTime']}, Previous State: {row['prev_state']}, Current State: {row['State']}")

    # Determine stability based on chatter occurrences
    if chatter_count > 0:
        return f"Site: {site} is unstable with {chatter_count} chatter occurrences."
    else:
        return f"Site: {site} is stable."

# Example usage
unstable_result = is_data_stable('chatter_data.txt', 'Chatter_Site')
stable_result = is_data_stable('stable_data.txt', 'Stable_Site', print_unstable_periods=True)

print(unstable_result)  # Example output for Chatter_Site
print(stable_result)     # Example output for Stable_Site
