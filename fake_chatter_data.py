# import pandas as pd
# import random
# from datetime import datetime, timedelta

# def generate_chatter_data(start_date, end_date):
#     data = []
#     current_date = start_date
#     id_counter = 1  # Initialize ID counter

#     while current_date <= end_date:
#         if current_date.month not in [6, 7, 8, 9]:  # Assuming wet months
#             num_changes = random.randint(5, 15)  
#             current_state = random.choice(['In Operation', 'Off'])
#             last_change_time = None  # Track last change time
            
#             for _ in range(num_changes):
#                 # Randomly determine a change time within the same day
#                 change_time = current_date + timedelta(seconds=random.randint(0, 30))
                
#                 # Toggle the state
#                 new_state = 'Off' if current_state == 'In Operation' else 'In Operation'
                
#                 # Assess if this change is chatter
#                 is_chatter = False
#                 if last_change_time and (change_time - last_change_time).total_seconds() <= 30:
#                     is_chatter = True

#                 # Append the data with chatter assessment
#                 data.append([id_counter, 'Chatter_Site', change_time.strftime('%d/%m/%Y %H:%M:%S'), 
#                               new_state, 'Good', 'Current Data', None, None, 'Sensor', is_chatter])
                
#                 # Update current state and last change time
#                 current_state = new_state
#                 last_change_time = change_time
#                 id_counter += 1  # Increment the ID counter
#         current_date += timedelta(days=1)

#     return data

# def generate_stable_data(start_date, end_date):
#     data = []
#     current_date = start_date
#     id_counter = 1  # Initialize ID counter

#     while current_date <= end_date:
#         if current_date.month in [6, 7, 8, 9]:  # Dry months
#             num_changes = random.randint(3, 8)  # Fewer changes
#         else:  # Wet months
#             num_changes = random.randint(10, 15)  # More changes

#         current_state = random.choice(['In Operation', 'Off'])  # Initial state
#         for _ in range(num_changes):
#             change_time = current_date + timedelta(seconds=random.randint(0, 86399))  # Any time of the day
#             current_state = 'Off' if current_state == 'In Operation' else 'In Operation'  # Toggle state
#             data.append([id_counter, 'Stable_Site', change_time.strftime('%d/%m/%Y %H:%M:%S'), current_state, 'Good', 'Current Data', None, None, 'Sensor', True])
#             id_counter += 1  # Increment the ID counter
#         current_date += timedelta(days=1)

#     return data

# # Define the date range
# start_date = datetime(2023, 10, 3)
# end_date = datetime(2024, 10, 3)

# # Generate data for chatter site and stable site
# chatter_data = generate_chatter_data(start_date, end_date)
# stable_data = generate_stable_data(start_date, end_date)

# # Create DataFrames
# chatter_df = pd.DataFrame(chatter_data, columns=['ID', 'Site', 'Time', 'State', 'Quality', 'Reason', 'Status', 'Suppression', 'Type', 'is_chatter'])
# stable_df = pd.DataFrame(stable_data, columns=['ID', 'Site', 'Time', 'State', 'Quality', 'Reason', 'Status', 'Suppression', 'Type', 'real_point'])

# # Save to CSV files
# chatter_df.to_csv('chatter_data.txt', index=False, sep=',')
# stable_df.to_csv('stable_data.txt', index=False, sep=',')

# print("Extrapolated data for chatter site saved to 'chatter_data.txt'")
# print("Extrapolated data for stable site saved to 'stable_data.txt'")


import pandas as pd
import random
from datetime import datetime, timedelta

def generate_chatter_data(start_date, end_date):
    data = []
    current_date = start_date
    id_counter = 1  # Initialize ID counter

    while current_date <= end_date:
        if current_date.month not in [6, 7, 8, 9]:  # Assuming wet months
            num_changes = random.randint(5, 15)  
            current_state = random.choice(['In Operation', 'Off'])
            last_change_time = None  # Track last change time
            
            for _ in range(num_changes):
                # Randomly determine a change time within the same day
                change_time = current_date + timedelta(seconds=random.randint(0, 30))
                
                # Toggle the state
                new_state = 'Off' if current_state == 'In Operation' else 'In Operation'
                
                # Assess if this change is chatter
                is_chatter = False
                if last_change_time and (change_time - last_change_time).total_seconds() <= 30:
                    is_chatter = True

                # Append the data with chatter assessment
                data.append([id_counter, 'Chatter_Site', change_time.strftime('%d/%m/%Y %H:%M:%S'), 
                              new_state, 'Good', 'Current Data', None, None, 'Sensor', is_chatter])
                
                # Update current state and last change time
                current_state = new_state
                last_change_time = change_time
                id_counter += 1  # Increment the ID counter
        current_date += timedelta(days=1)

    return data

def generate_stable_data(start_date, end_date):
    data = []
    current_date = start_date
    id_counter = 1  # Initialize ID counter

    while current_date <= end_date:
        if current_date.month in [6, 7, 8, 9]:  # Dry months
            num_changes = random.randint(3, 8)  # Fewer changes
        else:  # Wet months
            num_changes = random.randint(10, 15)  # More changes

        current_state = random.choice(['In Operation', 'Off'])  # Initial state
        last_change_time = None  # Track last change time
        
        for _ in range(num_changes):
            # Generate a change time that is at least 30 seconds apart from the last change
            if last_change_time is None:
                change_time = current_date + timedelta(seconds=random.randint(0, 86399))  # Any time of the day
            else:
                # Ensure the new change time is at least 30 seconds after the last change
                change_time = last_change_time + timedelta(seconds=90 + random.randint(10, 90))
            
            current_state = 'Off' if current_state == 'In Operation' else 'In Operation'  # Toggle state
            
            data.append([id_counter, 'Stable_Site', change_time.strftime('%d/%m/%Y %H:%M:%S'), current_state, 'Good', 'Current Data', None, None, 'Sensor', True])
            last_change_time = change_time  # Update last change time
            id_counter += 1  # Increment the ID counter
        
        current_date += timedelta(days=1)

    return data

# Define the date range
start_date = datetime(2023, 10, 3)
end_date = datetime(2024, 10, 3)

# Generate data for chatter site and stable site
chatter_data = generate_chatter_data(start_date, end_date)
stable_data = generate_stable_data(start_date, end_date)

# Create DataFrames
chatter_df = pd.DataFrame(chatter_data, columns=['ID', 'Site', 'Time', 'State', 'Quality', 'Reason', 'Status', 'Suppression', 'Type', 'is_chatter'])
stable_df = pd.DataFrame(stable_data, columns=['ID', 'Site', 'Time', 'State', 'Quality', 'Reason', 'Status', 'Suppression', 'Type', 'real_point'])

# Save to CSV files
chatter_df.to_csv('chatter_data.txt', index=False, sep=',')
stable_df.to_csv('stable_data.txt', index=False, sep=',')

print("Extrapolated data for chatter site saved to 'chatter_data.txt'")
print("Extrapolated data for stable site saved to 'stable_data.txt'")
