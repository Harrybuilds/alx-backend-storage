-- 3-glam_rock.sql

-- Select bands with 'Glam rock' as their main style and calculate lifespan based on formed and split dates
-- If the band hasn't split, we assume they are still active as of 2022 (i.e., split is NULL)
SELECT band_name,
       CASE
           WHEN split IS NULL THEN (2022 - formed)
           ELSE (split - formed)
       END AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
