from typing import Any, Dict, List, Tuple
import pandas as pd
from core.cleaner import clean_numeric


def create_daily_summary(combined_df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Aggregate combined dataframe by Day, sum numeric columns, and recalculate rates."""
    # 1. Product count per day
    prod_count = combined_df.groupby("Day")["ID"].count().reset_index()
    prod_count.rename(columns={"ID": "Total Products"}, inplace=True)

    # 2. Prepare cleaned metrics for summing
    agg_df = pd.DataFrame()
    agg_df["Day"] = combined_df["Day"]

    for col in combined_df.columns:
        if col in ["Day", "ID", "Product"] or "rate" in col.lower():
            continue
        agg_df[col] = combined_df[col].apply(clean_numeric)

    daily_summary = agg_df.groupby("Day", as_index=False).sum()
    daily_summary = pd.merge(prod_count, daily_summary, on="Day")

    # 3. Recalculate CTR and Conversion Rates from summed metrics
    if "Video impressions" in daily_summary and "Page views from video" in daily_summary:
        daily_summary["Video click-through rate"] = daily_summary.apply(
            lambda r: (r["Page views from video"] / r["Video impressions"]) if r["Video impressions"] > 0 else 0.0,
            axis=1,
        )

    if "Unique page views from video" in daily_summary and "Video unique product customers" in daily_summary:
        daily_summary["Video conversion rate"] = daily_summary.apply(
            lambda r: (r["Video unique product customers"] / r["Unique page views from video"])
            if r["Unique page views from video"] > 0
            else 0.0,
            axis=1,
        )

    if "Product card impressions" in daily_summary and "Page views from product card" in daily_summary:
        daily_summary["Product card click-through rate"] = daily_summary.apply(
            lambda r: (r["Page views from product card"] / r["Product card impressions"])
            if r["Product card impressions"] > 0
            else 0.0,
            axis=1,
        )

    if "Unique page views from product card" in daily_summary and "Product card unique customers" in daily_summary:
        daily_summary["Product card conversion rate"] = daily_summary.apply(
            lambda r: (r["Product card unique customers"] / r["Unique page views from product card"])
            if r["Unique page views from product card"] > 0
            else 0.0,
            axis=1,
        )

    # Sort descending by Day
    daily_summary["Sort_Date"] = pd.to_datetime(daily_summary["Day"], errors="coerce")
    daily_summary = daily_summary.sort_values(by="Sort_Date", ascending=False).drop(columns=["Sort_Date"])

    # Reorder columns: Day, Total Products, followed by original metrics in sequence
    ordered_cols = ["Day", "Total Products"] + [c for c in combined_df.columns if c not in ["Day", "ID", "Product"]]
    final_cols = [c for c in ordered_cols if c in daily_summary.columns]
    daily_summary = daily_summary[final_cols]

    return daily_summary, final_cols


def calculate_total_summary(daily_summary: pd.DataFrame, final_cols: List[str]) -> Dict[str, Any]:
    """Calculate aggregated total values and overall rates for the summary row."""
    tot_dict: Dict[str, Any] = {"Day": "Total"}

    for c in final_cols:
        if c == "Day" or "rate" in c.lower():
            continue
        tot_dict[c] = daily_summary[c].sum()

    # Recalculate total rates from overall totals
    if "Video impressions" in tot_dict and "Page views from video" in tot_dict:
        tot_dict["Video click-through rate"] = (
            (tot_dict["Page views from video"] / tot_dict["Video impressions"])
            if tot_dict["Video impressions"] > 0
            else 0.0
        )

    if "Unique page views from video" in tot_dict and "Video unique product customers" in tot_dict:
        tot_dict["Video conversion rate"] = (
            (tot_dict["Video unique product customers"] / tot_dict["Unique page views from video"])
            if tot_dict["Unique page views from video"] > 0
            else 0.0
        )

    if "Product card impressions" in tot_dict and "Page views from product card" in tot_dict:
        tot_dict["Product card click-through rate"] = (
            (tot_dict["Page views from product card"] / tot_dict["Product card impressions"])
            if tot_dict["Product card impressions"] > 0
            else 0.0
        )

    if "Unique page views from product card" in tot_dict and "Product card unique customers" in tot_dict:
        tot_dict["Product card conversion rate"] = (
            (tot_dict["Product card unique customers"] / tot_dict["Unique page views from product card"])
            if tot_dict["Unique page views from product card"] > 0
            else 0.0
        )

    return tot_dict
