mmsi_draught_avg = """
SELECT
    ROUND(avg(twAvg(dt.draught))::numeric, 2) AS draught_avg
FROM public.fact_trajectory AS ft
    INNER JOIN public.dim_trajectory AS dt ON ft.start_date_id = dt.date_id and ft.trajectory_sub_id = dt.trajectory_sub_id
    INNER JOIN public.dim_ship AS ds ON ft.ship_id = ds.ship_id
WHERE ds.mmsi = {{mmsi}};
"""

mmsi_draught_min = """
SELECT
    min(minValue(dt.draught))
FROM public.fact_trajectory AS ft
    INNER JOIN public.dim_trajectory AS dt ON ft.start_date_id = dt.date_id and ft.trajectory_sub_id = dt.trajectory_sub_id
    INNER JOIN public.dim_ship AS ds ON ft.ship_id = ds.ship_id
WHERE ds.mmsi = {{mmsi}};

"""

mmsi_draught_max = """
SELECT
    max(maxValue(dt.draught))
FROM public.fact_trajectory AS ft
    INNER JOIN public.dim_trajectory AS dt ON ft.start_date_id = dt.date_id and ft.trajectory_sub_id = dt.trajectory_sub_id
    INNER JOIN public.dim_ship AS ds ON ft.ship_id = ds.ship_id
WHERE ds.mmsi = {{mmsi}};
"""

mmsi_draught_mean = """
SELECT median 
FROM depth.mv_ship_mean_draught 
WHERE mmsi = {{mmsi}};
"""

mmsi_draught_histogram = """
SELECT
    draught,
    count(*)
FROM depth.fact_depth_50m AS fd50m
    INNER JOIN public.dim_ship AS ds ON fd50m.ship_id = ds.ship_id
WHERE ds.mmsi = {{mmsi}}
group by draught
ORDER BY draught DESC NULLS LAST;
"""

