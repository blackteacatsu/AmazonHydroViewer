from pathlib import Path
import json
import urllib.request
import xarray
import pandas as pd

app_dir = Path(__file__).parent
tips = pd.read_csv(app_dir / "tips.csv")

