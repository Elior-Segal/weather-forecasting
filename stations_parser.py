import re
from typing import List, Dict
import pandas as pd


# The site doesn't allow automated downloads:
# file at https://www.bom.gov.au/climate/data/lists_by_element/stations.txt

def parse_value(x: str):
    x = x.strip()
    if x in ("", "..", "....."):
        return None
    try:
        return float(x) if "." in x else int(x)
    except ValueError:
        return x


def parse_bom_file(path: str) -> List[Dict]:
    records = []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find header + separator
    header_idx = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith("Site  Dist"):
            header_idx = i
            break

    if header_idx is None:
        raise ValueError("Header not found")

    header = lines[header_idx].rstrip("\n")
    separator = lines[header_idx + 1].rstrip("\n")

    # Column spans are defined by runs of dashes
    spans = [(m.start(), m.end()) for m in re.finditer(r"-+", separator)]

    # Column names aligned to those spans
    columns = [
        header[start:end].strip().lower().replace(" ", "_")
        for start, end in spans
    ]

    # Data starts after separator
    for line in lines[header_idx + 2:]:
        if not line.strip():
            continue

        row = {}
        for (start, end), col in zip(spans, columns):
            row[col] = parse_value(line[start:end])

        records.append(row)

    return records


data = parse_bom_file("stations.txt")
df = pd.DataFrame(data)
df = df[df["site"].notna() & df["start"].notna() & df["start"].apply(lambda x: isinstance(x, int))]
df['site_norm'] = df.site_name.apply(
    lambda s: s.replace('NORTH TASMAN SEA (', '').replace('EAST', '').replace('WEST', '').replace(' ',
                                                                                                  '') if isinstance(s,
                                                                                                                    str) else s)
df = df[df["site_norm"].apply(lambda x: isinstance(x, str))]
