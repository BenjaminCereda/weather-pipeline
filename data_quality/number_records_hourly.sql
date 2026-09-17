select
    d.city_id,
    count(*) as row_count
from hourly_forecast d

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
having
    count(*) != 168

