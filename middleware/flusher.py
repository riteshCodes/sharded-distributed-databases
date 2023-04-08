import os
import glob
from pathlib import Path

from main import MWare

m_ware = MWare()
m_ware.flush_all()
print('All data are flushed from the databases')
print(m_ware.key_space_inf())

# Set the directory where log files are stored
log_dir = Path('logs')

# Check if the directory exists
if os.path.isdir(log_dir):
    # Find and delete all log files in the specified directory
    log_files = glob.glob(os.path.join(log_dir, "*.log"))

    for log_file in log_files:
        try:
            os.remove(log_file)
            print(f"Deleted: {log_file}")
        except OSError as e:
            print(f"Error deleting {log_file}: {e}")

    print(f"All log files have been deleted from {log_dir}.")
else:
    print(f"Error: Directory {log_dir} does not exist.")
