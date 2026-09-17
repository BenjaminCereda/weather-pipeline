-- 4. For each city and day, how many hours have a precipitation probability above 50%?

select
    c.city_name,
    h.day_time,
    sum(
        case
            when h.precipitation_probability > 50 then 1
            else 0
        end
        ) as num_hour
from hourly_forecast h

join (
    select 
        city_id, 
        max(fetch_id) as last_fetch 
    from forecast_fetches
    group by city_id
) as last
    on h.city_id = last.city_id
    and h.fetch_id = last.last_fetch

join cities c
    on h.city_id = c.city_id

group by
    c.city_name,
    h.day_time
