-- 1. Which cities will have the highest temperature tomorrow?
select 
    c.city_name,
    h.day_time, 
    h.hour_time, 
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

where day_time = date('now', '+1 days')

group by 
    c.city_name
order by max_temp desc