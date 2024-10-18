-- 2-fans.sql

-- First, we assume the metal_bands table has been created with the required data

-- Fetch and sum the number of fans for each country (origin)
-- Then rank the countries by total number of fans (non-unique)
SELECT origin, SUM(nb_fans) AS total_fans
FROM metal_bands
GROUP BY origin
ORDER BY total_fans DESC;
