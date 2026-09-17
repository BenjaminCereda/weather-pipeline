--  6. How has the forecast for the same city and date changed between different API fetches?

select 
    *,
    latest_temp - previous_temp as change
from (
    select
        c.city_name,
        d.day_time,
        MAX(
            CASE
                WHEN fetch_rank = 1 THEN temperature_2m
            END
        ) AS latest_temp, 
        MAX(
        CASE
            WHEN fetch_rank = 2 THEN temperature_2m
        END
        ) AS previous_temp
    from (
        select
            city_id,
            fetch_id,
            ROW_NUMBER() over (
                PARTITION by city_id
                order by fetch_id DESC
            ) AS fetch_rank
        from forecast_fetches
        ) f
    join daily_forecast d
        on d.fetch_id = f.fetch_id
    join cities c
        on d.city_id = c.city_id
    where fetch_rank < 3
    group by
        c.city_name,
        d.day_time
)