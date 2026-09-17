-- 2. For each city and day, what are the minimum, maximum, and average temperatures?

select 
    c.city_name,
    h.day_time, 
    min(h.temperature_2m) as min_temp,
    max(h.temperature_2m) as max_temp,
    avg(h.temperature_2m) as avg_temp

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
    c.city_id,
    h.day_time