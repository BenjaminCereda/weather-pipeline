-- 5. Which city has the best weather for outdoor activities over the next 3 days?

select
    c.city_name,
    sum(
        case
            when h.precipitation_probability <= 30
            and h.temperature_2m <= 26
            and h.temperature_2m >= 18 then 1
            else 0
        end
        ) as score
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

where
    h.day_time >= date('now')
    and h.day_time < date('now', '+3 days')

group by
    c.city_name

order by score desc