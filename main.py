import pandas as pd
from scipy.spatial.transform import Rotation as R
import numpy as np

pd.options.display.float_format = "{:,.2f}".format
pd.set_option('display.max_columns', None)

columns = ['Date', 'id', 'Matrix']
data = pd.read_csv(r'C:\Users\phili\PycharmProjects\Kw_Data_eval\data.csv', header=None, names=columns)

df = pd.DataFrame(data)

# Split Matrix values into separate columns
split_columns = df['Matrix'].str.split(" ", expand=True)
num_columns = len(split_columns.columns)

# Define column names for split columns
column_names = [f'tvecx', 'tvecy', 'tvecz', 'rvecx', 'rvecy', 'rvecz', 'null']

# Assign column names to split columns dataframe
split_columns.columns = column_names

# Concatenate split columns to the original dataframe
df = pd.concat([df, split_columns], axis=1)

# Convert columns to float
df['rvecx'] = pd.to_numeric(df['rvecx']).astype('float64')
df['rvecy'] = pd.to_numeric(df['rvecy']).astype('float64')
df['rvecz'] = pd.to_numeric(df['rvecz']).astype('float64')

# Function to create Euler angles for each element
def create_euler_angles(row):
    rvecx = row['rvecx']
    rvecy = row['rvecy']
    rvecz = row['rvecz']
    r = R.from_rotvec(np.pi/2 * np.array([rvecx, rvecy, rvecz]))
    return r.as_euler('zxy', degrees=True)  # Convert Rotation object to Euler angles with 'zxy' sequence

# Apply the function to create Euler angles for each element
df['euler_angles'] = df.apply(create_euler_angles, axis=1)

# Print the DataFrame with Euler angles
print(df['euler_angles'])
