select * 
from (
    select
        d.city_id,
        max(d.day_time) as last_day,
        min(d.day_time) as first_day,
        max(to_char(d.day_time::timestamp, 'J')::INTEGER) -
        min(to_char(d.day_time::timestamp, 'J')::INTEGER) as date_range
    from daily_forecast d

    join (
        select 
            city_id, 
            max(fetch_id) as last_fetch 
        from forecast_fetches
        group by city_id
    ) as last
        on d.city_id = last.city_id
        and d.fetch_id = last.last_fetch
    group by
    d.city_id
)
where 
    date_range != 6
-- having
--     date_range != 6


