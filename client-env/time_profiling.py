import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Store latency data in a Pandas DataFrame
data = {'keys': ['1', '10', '100', '1000', '10000'],
        'latency': [50, 40, 60, 70, 80]}
df = pd.DataFrame(data)
print(df)
# df.set_index('keys', inplace=True)  # Set timestamp column as index

# Plot configurations
fig, axs = plt.subplots()
plt.plot(df.index, df['latency'])
plt.xlabel('Number of key-value pairs (Throughput)')
plt.ylabel('Latency (ms)')
plt.title('Total Latency: ')
plt.grid(True)
plt.show()

