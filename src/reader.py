import io
import numpy as np
import pandas as pd

class FormCSV:
  def __init__(self, filename):
    self.filename = filename
    self.parse()

  @staticmethod
  def time_to_seconds(time_str: str) -> float | np.nan:
    """
    Convert time string in format 'mm:ss' to seconds.
    """
    # Handles cases where time_str might be NaN or not a string
    if pd.isna(time_str) or not isinstance(time_str, str):
        return np.nan
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes = float(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    return np.nan

  def parse(self):
    with open(self.filename) as f:
      lines = f.readlines()

    # The first two lines correspond to the description
    description_csv = ''.join(lines[:2])
    description_io = io.StringIO(description_csv)
    self.description_df = pd.read_csv(description_io)

    # There is a blank line then the remaining lines are the swim data
    swim_csv = ''.join(lines[3:])
    swim_io = io.StringIO(swim_csv)
    self.swim_df = pd.read_csv(swim_io)

    # Convert 'Cumul Time' and 'Move Time' to seconds
    self.swim_df['Cumul Time (s)'] = self.swim_df['Cumul Time'].apply(self.time_to_seconds)
    self.swim_df['Move Time (s)'] = self.swim_df['Move Time'].apply(self.time_to_seconds)
