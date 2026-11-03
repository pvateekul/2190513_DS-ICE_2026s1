import pandas as pd
from fastmcp import FastMCP

df = pd.DataFrame(
    {
        "province": [
            "Chiang Mai",
            "Chiang Mai",
            "Bangkok",
            "Bangkok",
            "Phuket",
            "Phuket",
        ],
        "year": [2023, 2024, 2023, 2024, 2023, 2024],
        "rainfall": [1100, 1250, 1400, 1550, 2400, 2200],
        "crop_yield": [3.1, 3.4, 2.8, 3.0, 2.5, 2.7],
    }
)


mcp = FastMCP("Data Science Assistant")


@mcp.tool
def get_summary() -> dict:
    """Return the dataset's shape, columns, and descriptive statistics."""
    return {
        "rows": len(df),
        "columns": df.columns.tolist(),
        "statistics": df.describe().round(2).to_dict(),
    }


@mcp.tool
def get_top_provinces(
    column: str,
    n: int = 5,
) -> list[dict]:
    """Return the top provinces by a numeric column's average."""
    allowed_columns = {"rainfall", "crop_yield"}

    if column not in allowed_columns:
        raise ValueError("Unsupported column")

    if not 1 <= n <= 20:
        raise ValueError("n must be between 1 and 20")

    return (
        df.groupby("province")[column]
        .mean()
        .sort_values(ascending=False)
        .head(n)
        .round(2)
        .rename("average")
        .reset_index()
        .to_dict(orient="records")
    )


@mcp.tool
def filter_data(
    province: str,
) -> list[dict]:
    """Return all records for a specific province."""
    result = df[df["province"].str.lower() == province.lower()]
    return result.to_dict(orient="records")


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
