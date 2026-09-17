--- 7. Which cities have the most volatile forecasts across multiple fetches?

select 
    city_name,
    avg(change) as avg_change
from (
    select 
        *,
        abs(temperature_2m - previous_temp) as change
    from (
        select
            c.city_name,
            d.day_time,
            d.temperature_2m,
            LAG(d.temperature_2m) OVER (
                PARTITION BY c.city_name, d.day_time
                ORDER BY f.fetch_id
                ) AS previous_temp

        from forecast_fetches f

        join daily_forecast d
            on f.fetch_id = d.fetch_id

        join cities c
            on d.city_id = c.city_id

        order by f.fetch_id
    )
)
group by
    city_name