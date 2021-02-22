-- https://www.interviewquery.com/questions/random-sql-sample

-- This brute force approach will break for big tables
-- SELECT *
-- FROM big_table
-- ORDER BY RAND()
-- LIMIT 10

SELECT t1.id, t1.name
FROM big_table as t1
INNER JOIN 
(
SELECT CEIL(RAND() * 
    (SELECT MAX(id) FROM big_table)) as ID
) as t2
ON t1.id >= t2.id
ORDER BY t1.id ASC
LIMIT 6;