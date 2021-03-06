#!/usr/bin/env bash
source='tealeaf'
destiny='tealeaf-flask'
user=mk

pg_dump -U ${user} -t students_student ${source} | psql -U ${user} -d ${destiny}
pg_dump -U ${user} -t students_group ${source} | psql -U ${user} -d ${destiny}
pg_dump -U ${user} -t students_discipline ${source} | psql -U ${user} -d ${destiny}
pg_dump -U ${user} -t students_studentlab ${source} | psql -U ${user} -d ${destiny}
pg_dump -U ${user} -t students_mark ${source} | psql -U ${user} -d ${destiny}
pg_dump -U ${user} -t students_lesson ${source} | psql -U ${user} -d ${destiny}
pg_dump -U ${user} -t students_studenttask ${source} | psql -U ${user} -d ${destiny}
pg_dump -U ${user} -t students_studenttaskresult ${source} | psql -U ${user} -d ${destiny}

psql -U ${user} ${destiny} <<SQL
INSERT INTO groups(id, title, year, captain_id)
SELECT id, title, year, captain_id
FROM students_group;
SQL

psql -U ${user} ${destiny} <<SQL
INSERT INTO students (id, name, second_name, group_id, sex)
SELECT id, name, second_name, group_id, sex
FROM students_student;
SQL

psql -U ${user} ${destiny} <<SQL
INSERT INTO disciplines (id, title, year, visible)
SELECT id, title, year, visible
FROM students_discipline;
SQL

psql -U ${user} ${destiny} <<SQL
INSERT INTO labs (id, title, description, discipline_id, visible, regular)
SELECT id, title, description, discipline_id, visible, regular
FROM students_studentlab;
SQL

psql -U ${user} ${destiny} <<SQL
INSERT INTO lessons (id, description, date, lesson_type, discipline_id, group_id, score_ignore)
SELECT id, description, date, lesson_type, discipline_id, group_id, score_ignore
FROM students_lesson;
SQL

psql -U ${user} ${destiny} <<SQL
INSERT INTO marks (id, value, lesson_id, student_id)
SELECT id, mark, lesson_id, student_id
FROM students_mark;
SQL

psql -U ${user} ${destiny} <<SQL
INSERT INTO tasks (id, complexity, description, "order", lab_id)
SELECT id, complexity, description, "order", lab_id
FROM students_studenttask;
SQL

psql -U ${user} ${destiny} <<SQL
INSERT INTO taskresults (id, created_at, updated_at, done, task_id, student_id)
SELECT id, date_create, date_update, done, task_id, student_id
FROM students_studenttaskresult;
SQL


psql -U ${user} ${destiny} <<SQL
DROP TABLE students_group CASCADE;
DROP TABLE students_student CASCADE;
DROP TABLE students_discipline CASCADE;
DROP TABLE students_mark CASCADE;
DROP TABLE students_studentlab CASCADE;
DROP TABLE students_lesson CASCADE;
DROP TABLE students_studenttask CASCADE;
DROP TABLE students_studenttaskresult CASCADE;
SQL

psql -U ${user} ${destiny} << SQL
SELECT setval('articles_id_seq', (SELECT MAX(id) FROM articles));
SELECT setval('disciplines_id_seq', (SELECT MAX(id) FROM disciplines));
SELECT setval('groups_id_seq', (SELECT MAX(id) FROM groups));
SELECT setval('labs_id_seq', (SELECT MAX(id) FROM labs));
SELECT setval('lessons_id_seq', (SELECT MAX(id) FROM lessons));
SELECT setval('marks_id_seq', (SELECT MAX(id) FROM marks));
SELECT setval('roles_id_seq', (SELECT MAX(id) FROM roles));
SELECT setval('students_id_seq', (SELECT MAX(id) FROM students));
SELECT setval('tasks_id_seq', (SELECT MAX(id) FROM tasks));
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('taskresults_id_seq', (SELECT MAX(id) FROM taskresults));
SQL