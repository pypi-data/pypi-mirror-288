-- Goal:
    -- Change the confidence values of outliers to 0.0.
-- Reason:
    -- There has been a single case where a ship managed to have a draught value of 25.5 meters with a confidence
    -- value of 1.0. This should not be possible, so until the cause can be determined, we have decided to set the
    -- confidence value of outliers to 0.0.

UPDATE depth.fact_depth_50m AS fd50m
SET confidence_depth_01 = 0.0
FROM public.dim_ship AS ds
WHERE ds.ship_id = fd50m.ship_id
AND ds.mmsi = {{outlier}}
AND draught BETWEEN {{min_draugh}} and {{max_draught}};