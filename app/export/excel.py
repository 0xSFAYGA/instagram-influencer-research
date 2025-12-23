import pandas as pd
from pathlib import Path
from typing import List, Mapping


def write_excel(path: Path, rows: List[Mapping]) -> Path:
    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
        sheet = writer.book.active
        sheet.freeze_panes = "A2"
    return path

