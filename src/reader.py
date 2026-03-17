import pandas as pd

class FormCSV:
  def __init__(self, filename):
    self.filename = filename
    self.parse()

  def parse(self):
    # Read the first two lines as the description (header + 1 row of data)
    self.description_df = pd.read_csv(self.filename, nrows=1)

    # Skip the description and the blank line (first 3 lines) to read swim data
    self.swim_df = pd.read_csv(self.filename, skiprows=3)

    # Convert 'Cumul Time' and 'Move Time' to seconds
    for col in ['Cumul Time', 'Move Time']:
        if col in self.swim_df.columns:
            # Prepend '00:' to convert 'mm:ss' to 'hh:mm:ss' for pandas to_timedelta
            time_strings = '00:' + self.swim_df[col].astype(str)
            self.swim_df[f'{col} (s)'] = pd.to_timedelta(time_strings, errors='coerce').dt.total_seconds()
