-- https://www.interviewquery.com/questions/closest-sat-scores

-- Create a column with the difference in scores across students (cross join)
-- Cross joing where id is different
-- ORDER BY score_diff ASC, studentA, studentB

SELECT s1.student as one_student, s2.student as other_student,
        ABS(s1.score - s2.score) as score_diff
FROM scores as s1
INNER JOIN scores as s2
    ON s1.id != s2.id AND s1.id > s2.id
ORDER BY score_diff ASC, one_student ASC
LIMIT 1