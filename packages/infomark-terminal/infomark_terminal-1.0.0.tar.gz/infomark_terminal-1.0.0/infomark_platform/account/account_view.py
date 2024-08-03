import pandas as pd

from infomark_terminal.helper_funcs import print_rich_table
from infomark_terminal.rich_config import console


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """

    """
    df["updated_date"] = pd.to_datetime(df["updated_date"])
    df["updated_date"] = df["updated_date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.replace(to_replace=[None], value="-", inplace=True)
    to_rename = {
        "name": "Name",
        "description": "Description",
        "version": "Version",
        "updated_date": "Last Update",
    }
    df = df.rename(columns=to_rename)
    df = df[["Name", "Description", "Version", "Last Update"]]
    return df

def display_personal_routines(df: pd.DataFrame, page: int, pages: int):
    """

    """
    try:
        title = f"Personal routines - page {page}"
        if pages:
            title += f" of {pages}"
            df = clean_df(df)

            print_rich_table(
                df=df,
                title=title,
                headers=list(df.columns),
                show_header=True,
                index_name="#",
            )
    except Exception:
        console.print("Failed to display personal routines.")

def display_default_routines(df: pd.DataFrame):
    """
    """
    try:
        df = df.rename(columns={"date_updated": "updated_date"})
        df = clean_df(df)
        print_rich_table(
            df=df,
            title="Default routines",
            headers=["Name", "Description", "Version", "Last update"],
            show_index=True,
            index_name="#",
        )
    except Exception:
        console.print("Failed to display default routines.")
