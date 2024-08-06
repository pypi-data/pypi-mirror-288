-- Goal:
    -- Change the draught values of type B ships to 0.1.
-- Reason:
    -- Normally, we exclude ships with draught NULL from queries, case a Type A ship should always have a draught value.
    -- However, in the case of Type B ships, only 0.03% of the ships have a draught value, and the rest have NULL.
    -- So we decided to change the draught values of Type B ships to 0.0, such that we can include them in the queries
    -- where we count them when determining the number of ships in an area.

UPDATE depth.fact_depth_50m AS fd50m
SET draught = 0.1
FROM public.dim_ship AS ds
    INNER JOIN public.dim_ship_type AS dst ON ds.ship_type_id = dst.ship_type_id
WHERE fd50m.ship_id = ds.ship_id
    AND dst.mobile_type = 'Class B'
    AND fd50m.draught IS NULL
    AND fd50m.date_id BETWEEN {{from_date}} AND {{to_date}};
