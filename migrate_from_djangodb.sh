#!/usr/bin/env bash
source='tealeaf'
destiny='tealeaf-flask'

pg_dump -U postgres -t students_student ${source} | psql -U postgres -d ${destiny}
pg_dump -U postgres -t students_group ${source} | psql -U postgres -d ${destiny}
pg_dump -U postgres -t students_discipline ${source} | psql -U postgres -d ${destiny}
pg_dump -U postgres -t students_studentlab ${source} | psql -U postgres -d ${destiny}
pg_dump -U postgres -t students_mark ${source} | psql -U postgres -d ${destiny}
pg_dump -U postgres -t students_lesson ${source} | psql -U postgres -d ${destiny}
pg_dump -U postgres -t students_studenttask ${source} | psql -U postgres -d ${destiny}

psql -U postgres ${destiny} <<SQL
INSERT INTO groups(id, title, year, captain_id)
SELECT id, title, year, captain_id
FROM students_group;
SQL

psql -U postgres ${destiny} <<SQL
INSERT INTO students (id, name, second_name, group_id, sex)
SELECT id, name, second_name, group_id, sex
FROM students_student;
SQL

psql -U postgres ${destiny} <<SQL
INSERT INTO disciplines (id, title, year, visible)
SELECT id, title, year, visible
FROM students_discipline;
SQL

psql -U postgres ${destiny} <<SQL
INSERT INTO labs (id, title, description, discipline_id, visible, regular)
SELECT id, title, description, discipline_id, visible, regular
FROM students_studentlab;
SQL

psql -U postgres ${destiny} <<SQL
INSERT INTO lessons (id, description, date, lesson_type, discipline_id, group_id, score_ignore)
SELECT id, description, date, lesson_type, discipline_id, group_id, score_ignore
FROM students_lesson;
SQL

psql -U postgres ${destiny} <<SQL
INSERT INTO marks (id, value, lesson_id, student_id)
SELECT id, mark, lesson_id, student_id
FROM students_mark;
SQL

psql -U postgres ${destiny} <<SQL
INSERT INTO tasks (id, complexity, description, "order", lab_id)
SELECT id, complexity, description, "order", lab_id
FROM students_studenttask;
SQL

psql -U postgres ${destiny} <<SQL
DROP TABLE students_group CASCADE;
DROP TABLE students_student CASCADE;
DROP TABLE students_discipline CASCADE;
DROP TABLE students_mark CASCADE;
DROP TABLE students_studentlab CASCADE;
DROP TABLE students_lesson CASCADE;
DROP TABLE students_studenttask CASCADE;
SQL