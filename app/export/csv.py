import pandas as pd
from pathlib import Path
from typing import List, Mapping


def write_csv(path: Path, rows: List[Mapping]) -> Path:
    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path

