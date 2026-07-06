-- Before Index
EXPLAIN ANALYZE
SELECT *
FROM tasks
WHERE title ILIKE '%Performance%';


-- Create Index
CREATE INDEX idx_tasks_title
ON tasks(title);


-- After Index
EXPLAIN ANALYZE
SELECT *
FROM tasks
WHERE title ILIKE '%Performance%';