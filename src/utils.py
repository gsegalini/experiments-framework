import os
import pandas as pd
from tqdm import tqdm
import numpy as np
class PerformanceManager:

    def __init__(self, filename):
        self.table = {}
        self.reset()
        self.filename = filename

    def reset(self):
        self.current_row = {}

    def log_metric(self, name, value):
        self.current_row[name] = value

    def commit_row(self, verbose=False):
        for key in self.table:
            if key not in self.current_row: self.current_row[key] = None
        for key in self.current_row:
            if key not in self.table:
                self.table[key] = []
            self.table[key].append(self.current_row[key])
        if verbose:
            tqdm.write(f"Logged metrics: {self.current_row}")
        self.reset()

    def save(self, append=False):
        df = self.to_pd()
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if append:
            if os.path.exists(self.filename):
                # 1. Read the existing data
                old_df = pd.read_csv(self.filename)
                # 2. Combine old and new (pandas automatically handles the column mismatch)
                combined_df = pd.concat([old_df, df], ignore_index=True)
                # 3. Write back to the same file                
                combined_df.to_csv(self.filename, index=False)
            else:
                # File doesn't exist, just write the new df
                df.to_csv(self.filename, index=False)
            self.table = {}
        else:
            df.to_csv(self.filename, index=False)

    def __repr__(self) -> str:
        # show avg of each column
        repr_str = "Performance Summary:\n"
        for key in self.table:
            # if column is numeric, show average
            col = self.table[key]
            if all(isinstance(x, (int, float, np.number)) or x is None for x in col):
                avg = np.nanmean([x for x in col if x is not None])
                repr_str += f"{key}: {avg:.1f}\n"
            else:
                repr_str += f"{key}: {col}\n"
        return repr_str
    
    def commit_and_save(self, verbose=False):
        self.commit_row(verbose=verbose)
        self.save(append=True)

    def to_pd(self):
        return pd.DataFrame(self.table)
