import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlalchemy
from gandai import constants
from gandai.db import connect_with_connector

db = connect_with_connector()


def leaderboard() -> pd.DataFrame:

    def analyst_stage_search_count_trailing_days():
        stmt = """
            SELECT
                s.label as search,
                e.type,
                a.name as analyst,
                SUM(CASE WHEN e.created >= EXTRACT(EPOCH FROM NOW()) - 7 * 86400 THEN 1 ELSE 0 END) AS last_7_days,
                SUM(CASE WHEN e.created >= EXTRACT(EPOCH FROM NOW()) - 14 * 86400 THEN 1 ELSE 0 END) AS last_14_days,
                SUM(CASE WHEN e.created >= EXTRACT(EPOCH FROM NOW()) - 30 * 86400 THEN 1 ELSE 0 END) AS last_30_days,
                SUM(CASE WHEN e.created >= EXTRACT(EPOCH FROM NOW()) - 90 * 86400 THEN 1 ELSE 0 END) AS last_90_days,
                SUM(CASE WHEN e.created >= EXTRACT(EPOCH FROM NOW()) - 180 * 86400 THEN 1 ELSE 0 END) AS last_180_days,
                SUM(CASE WHEN e.created >= EXTRACT(EPOCH FROM NOW()) - 365 * 86400 THEN 1 ELSE 0 END) AS last_365_days
            FROM
                event e
            LEFT JOIN
                actor a ON a.key = e.actor_key
            LEFT JOIN
                search s ON s.uid = e.search_uid
            WHERE
                e.type in ('validate', 'reject','advance','send','buyer','update','criteria')
            GROUP BY
                s.label, e.search_uid, analyst, e.type
            ORDER BY
                last_30_days DESC
            ;
            """
        with db.connect() as conn:
            result = conn.execute(sqlalchemy.text(stmt))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            df = df[df["last_90_days"] > 0]

        df["stage"] = df["type"].map(constants.STAGE_MAP)
        df["stage"] = df["stage"].fillna("update")
        df = df.drop(columns=["type"])

        return df

    def analyst_stage_search_count_by_date():

        stmt = """
            SELECT
                a.name as analyst,
                TO_CHAR(TO_TIMESTAMP(e.created), 'YYYY-MM-DD') as date,
                s.label as search,
                e.type,
                COUNT(*) as event_count
            FROM
                event e
            LEFT JOIN
                actor a ON a.key = e.actor_key
            LEFT JOIN
                search s ON s.uid = e.search_uid
            WHERE
                e.type in ('validate', 'reject', 'advance', 'send','buyer','update','criteria')
                AND TO_TIMESTAMP(e.created) >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY
                a.name,
                s.label,
                e.type,
                TO_CHAR(TO_TIMESTAMP(e.created), 'YYYY-MM-DD')
            ;
            """
        with db.connect() as conn:
            conn.execute(sqlalchemy.text("SET TIME ZONE 'America/Chicago'"))
            result = conn.execute(sqlalchemy.text(stmt))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

        df["search"] = df["search"].fillna("No Search")
        df["stage"] = df["type"].map(constants.STAGE_MAP)

        df = df.reset_index()
        df_pivot = df.pivot_table(
            index=["analyst", "stage", "search"],
            columns="date",
            values="event_count",
            fill_value=0,
        ).reset_index()
        return df_pivot

    def analyst_stage_search_count_by_week():
        stmt = """
            SELECT
                a.name as analyst,
                TO_CHAR(TO_TIMESTAMP(e.created), 'IYYY-IW') as week, -- ISO week
                s.label as search,
                e.type,
                COUNT(*) as event_count
            FROM
                event e
            LEFT JOIN
                actor a ON a.key = e.actor_key
            LEFT JOIN
                search s ON s.uid = e.search_uid
            WHERE
                e.type in ('validate', 'reject', 'advance', 'send','buyer','update','criteria')
                AND TO_TIMESTAMP(e.created) >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY
                a.name,
                s.label,
                e.type,
                TO_CHAR(TO_TIMESTAMP(e.created), 'IYYY-IW')
            ;
            """
        with db.connect() as conn:
            conn.execute(sqlalchemy.text("SET TIME ZONE 'America/Chicago'"))
            result = conn.execute(sqlalchemy.text(stmt))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

        df["search"] = df["search"].fillna("No Search")
        df["stage"] = df["type"].map(constants.STAGE_MAP)

        df = df.reset_index()
        df_pivot = df.pivot_table(
            index=["analyst", "stage", "search"],
            columns="week",
            values="event_count",
            fill_value=0,
        ).reset_index()

        df_pivot = df_pivot.rename(columns={df_pivot.columns[-2]: "last_week"})
        df_pivot = df_pivot.rename(columns={df_pivot.columns[-1]: "this_week"})
        df_pivot = df_pivot[["analyst", "stage", "search", "last_week", "this_week"]]
        return df_pivot

    df_trailing = analyst_stage_search_count_trailing_days()
    df_by_date = analyst_stage_search_count_by_date()
    df_by_week = analyst_stage_search_count_by_week()

    df = df_trailing.merge(df_by_date, on=["analyst", "stage", "search"], how="left")
    df = df.merge(df_by_week, on=["analyst", "stage", "search"], how="left")
    df = df.fillna(0)

    df = df.reset_index()
    df["analyst"] = df["analyst"].apply(lambda x: x.split(" ")[0])
    print(df)
    return df
