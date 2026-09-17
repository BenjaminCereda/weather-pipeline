-- 3. Which cities have the largest temperature swing within a single day?

select
    c.city_name,
    h.day_time,
    max(h.temperature_2m) - min(h.temperature_2m) as temp_diff,
    min(h.temperature_2m) as min_temp,
    max(h.temperature_2m) as max_temp
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

order by temp_diff desc