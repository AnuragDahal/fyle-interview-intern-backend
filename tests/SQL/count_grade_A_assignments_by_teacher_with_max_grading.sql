-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT teacher_id, COUNT(*) as grade_A_count
FROM assignments
WHERE grade = 'A' AND teacher_id = (
    SELECT teacher_id
    FROM (
        SELECT teacher_id, COUNT(*) as assignment_count
        FROM assignments
        GROUP BY teacher_id
        ORDER BY assignment_count DESC
        LIMIT 1
    ) as subquery
)
GROUP BY teacher_id;