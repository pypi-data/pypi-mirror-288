import pandas as pd
import plotly.express as px
import sqlalchemy
from gandai import constants
from gandai.query import db


def hours_per_analyst_per_day() -> px.scatter:
    stmt = """
    SELECT
        split_part(a.name, ' ', 1) as analyst,
        TO_CHAR(TO_TIMESTAMP(e.created), 'YYYY-MM-DD') as date,
        TO_CHAR(TO_TIMESTAMP(e.created), 'YYYY-MM-DD HH24:MI') as time 
    FROM
        event e
    LEFT JOIN
        actor a ON a.key = e.actor_key
    WHERE 
        TO_TIMESTAMP(e.created) >= CURRENT_DATE - INTERVAL '7 days'
        and a.type = 'research'
    ORDER BY
        e.created DESC
    ;
    """
    with db.connect() as conn:
        conn.execute(sqlalchemy.text("SET TIME ZONE 'America/Chicago'"))
        result = conn.execute(sqlalchemy.text(stmt))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    df['window'] = df['time'].apply(lambda x: f'{x[0:-1]}0')

    df_grouped = df.groupby(['date', 'analyst']).agg(
        windows=("window","nunique")
    ).reset_index()
    df_grouped['minutes'] = df_grouped['windows'] * 10
    df_grouped['hours'] = df_grouped['minutes'] / 60
    df_grouped['hours'] = df_grouped['hours'].round(1)
    df_grouped['text'] = df_grouped['hours'].astype(str) + " hrs"
    df_grouped = df_grouped.sort_values(by=["analyst"])
    fig = px.scatter(
        df_grouped,
        x="date",
        y="analyst",
        size="hours",
        color="analyst",
        # title="Hours per day per analyst",
        height=600,
        template="plotly_dark",
        text="text",
    )
    fig.update_traces(textposition="top center", textfont=dict(color="darkgray", size=10))
    return fig


def draw_events_by_analyst_by_date_by_stage() -> px.scatter:
    stmt = """
        SELECT
            a.name as analyst,
            TO_CHAR(TO_TIMESTAMP(e.created), 'YYYY-MM-DD') as date,
            e.type,
            COUNT(*) as event_count
        FROM
            event e
        LEFT JOIN
            actor a ON a.key = e.actor_key
        LEFT JOIN
            search s ON s.uid = e.search_uid
        WHERE
            e.type in ('validate', 'reject', 'advance', 'send')
            AND TO_TIMESTAMP(e.created) >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY
            a.name,
            e.type,
            TO_CHAR(TO_TIMESTAMP(e.created), 'YYYY-MM-DD')
        ORDER BY
            e.type,
            date,
            a.name
        ;
        """
    with db.connect() as conn:
        conn.execute(sqlalchemy.text("SET TIME ZONE 'America/Chicago'"))
        result = conn.execute(sqlalchemy.text(stmt))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    df["analyst"] = df["analyst"].apply(lambda x: x.split(" ")[0])
    df["stage"] = df["type"].map(constants.STAGE_MAP)
    type_order = ["reject", "advance", "validate", "send"]
    df["type"] = pd.Categorical(df["type"], categories=type_order, ordered=True)
    df = df.sort_values(by=["analyst"])
    fig = px.scatter(
        df,
        x="date",
        y="analyst",
        facet_col="stage",
        size="event_count",
        # title="Events by Analyst, by Date, by Stage | Last 7 Days",
        height=600,
        text="event_count",
        color="analyst",
        template="plotly_dark",
    )
    fig.update_traces(
        textposition="top center", textfont=dict(color="darkgray", size=10)
    )
    return fig
