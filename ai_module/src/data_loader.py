import logging
from pathlib import Path
from typing import Dict, Optional, Tuple

import pandas as pd

from ai_module.src.config import (
    DATASET_CSV_PATH,
    LABEL_LEGITIMATE,
    LABEL_MAP,
    LABEL_SCAM,
    PARENT_DATA_TSV,
    RAW_TSV_PATH,
    STRING_TO_LABEL_MAP,
)
from ai_module.src.preprocessing import normalize_text

logger = logging.getLogger(__name__)


def locate_raw_dataset() -> Path:
    candidates = [RAW_TSV_PATH, PARENT_DATA_TSV]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        f"Raw SMS dataset not found in any expected location:\n"
        f" - {RAW_TSV_PATH}\n"
        f" - {PARENT_DATA_TSV}\n"
        f"Please ensure 'sms_spam_collection.tsv' is present."
    )


def load_raw_dataset(tsv_path: Optional[Path] = None) -> pd.DataFrame:
    path = tsv_path if tsv_path is not None else locate_raw_dataset()
    logger.info(f"Loading raw dataset from {path}")

    df = pd.read_csv(
        path,
        sep="\t",
        names=["raw_label", "message"],
        quoting=3,
        encoding="utf-8",
        dtype={"raw_label": str, "message": str},
        on_bad_lines="skip",
    )
    return df


def prepare_dataset(
    tsv_path: Optional[Path] = None,
    drop_duplicates: bool = True,
    save_output: bool = True,
) -> pd.DataFrame:
    raw_df = load_raw_dataset(tsv_path)
    initial_count = len(raw_df)
    logger.info(f"Initial raw record count: {initial_count}")

    df = raw_df.dropna(subset=["raw_label", "message"]).copy()

    df["message"] = df["message"].apply(normalize_text)
    df["raw_label"] = df["raw_label"].astype(str).str.strip().str.lower()

    df = df[df["message"].str.len() > 0]

    valid_labels = set(STRING_TO_LABEL_MAP.keys())
    unknown_labels = df[~df["raw_label"].isin(valid_labels)]
    if not unknown_labels.empty:
        logger.warning(f"Dropping {len(unknown_labels)} rows with unrecognized labels.")
        df = df[df["raw_label"].isin(valid_labels)]

    df["label"] = df["raw_label"].map(STRING_TO_LABEL_MAP).astype(int)
    df["label_name"] = df["label"].map(LABEL_MAP)

    df = df[["message", "label", "label_name"]].reset_index(drop=True)

    dup_count = df.duplicated(subset=["message"]).sum()
    logger.info(f"Duplicate messages identified: {dup_count} ({dup_count/len(df):.2%})")

    if drop_duplicates:
        df = df.drop_duplicates(subset=["message"]).reset_index(drop=True)
        logger.info(f"Deduplicated dataset records: {len(df)}")
    else:
        logger.info(f"Retaining duplicates. Total records: {len(df)}")

    if save_output:
        DATASET_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(DATASET_CSV_PATH, index=False, encoding="utf-8")
        logger.info(f"Saved prepared dataset to {DATASET_CSV_PATH}")

    return df


def load_prepared_dataset(csv_path: Optional[Path] = None) -> pd.DataFrame:
    path = csv_path if csv_path is not None else DATASET_CSV_PATH

    if not path.exists():
        logger.info(f"Prepared dataset not found at {path}. Preparing from raw TSV...")
        return prepare_dataset(save_output=True)

    df = pd.read_csv(
        path,
        dtype={"message": str, "label": int, "label_name": str},
        encoding="utf-8",
    )
    df["message"] = df["message"].fillna("").astype(str)
    return df


def inspect_dataset_summary(df: pd.DataFrame) -> Dict[str, object]:
    total = len(df)
    counts = df["label"].value_counts().to_dict()
    named_counts = {LABEL_MAP.get(k, str(k)): v for k, v in counts.items()}
    proportions = {name: round((count / total) * 100, 2) for name, count in named_counts.items()}

    lengths = df["message"].str.len()

    stats = {
        "total_records": total,
        "class_counts": named_counts,
        "class_proportions_percent": proportions,
        "min_char_length": int(lengths.min()),
        "max_char_length": int(lengths.max()),
        "mean_char_length": round(float(lengths.mean()), 2),
        "median_char_length": round(float(lengths.median()), 2),
    }
    return stats


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    df_prepared = prepare_dataset()
    summary = inspect_dataset_summary(df_prepared)
    print("\nDataset Preparation Completed Successfully:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
