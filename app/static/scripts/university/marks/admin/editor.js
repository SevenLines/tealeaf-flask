/**
 * Created by m on 12.07.15.
 */
var LessonsCollection = Backbone.Collection.extend({
    model: Lesson
});

var LabsCollection = Backbone.Collection.extend({
    model: Lab
});

var LabItemsCollection = Backbone.Collection.extend({
    model: LabItem
});


var TasksCollection = Backbone.Collection.extend({
    model: Task
});


var StudentsCollection = Backbone.Collection.extend({
    model: Student,

    save: function () {
        var changed = new StudentsCollection(this.filter(function (item) {
            return item.is_changed();
        }));

        var requests = changed.forEach(function (item) {
            item.save();
        });
        $.when.apply($, requests).then(function () {
            loadToContent(window.location);
        })
    }
});

var StudentsCollectionView = Backbone.View.extend({
    events: {
        "click .btn-update": "save"
    },

    save: function () {
        this.collection.save();
    }
});

var MarksCollection = Backbone.Collection.extend({
    initialize: function (models, options) {
        //Backbone.Collection.apply(this, arguments);
        if (options) {
            this.urls = options.urls;
        }
    },

    model: Mark,

    save: function () {
        var changed = new MarksCollection(this.filter(function (item) {
            return item.is_changed();
        }));

        if (changed.length) {
            $.ajax({
                url: this.urls.save_marks,
                data: JSON.stringify(changed.toJSON()),
                method: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json"
            }).done(function () {
                changed.forEach(function (mark) {
                    mark.reset();
                });
            });
        }
    }
});

var TasksResultsCollection = Backbone.Collection.extend({
    initialize: function (models, options) {
        if (options) {
            this.urls = options.urls;
        }
    },

    model: TaskResult,
    save: function () {
        var changed = new TasksResultsCollection(this.filter(function (item) {
            return item.is_changed();
        }));
        if (changed.length) {
            $.ajax({
                url: this.urls.save_tasks_results,
                data: JSON.stringify(changed.toJSON()),
                method: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json"
            }).done(function () {
                changed.forEach(function (mark) {
                    mark.reset();
                });
            });
        }
    }
});


function EditorController(options) {
    var lessons = new LessonsCollection([], options);
    var students = new StudentsCollection([], options);
    var marks = new MarksCollection([], options);
    var tasks_results = new TasksResultsCollection([], options);
    var labs = new LabsCollection([], options);
    var tasks = new TasksCollection([], options);
    var labsItems = new LabItemsCollection([], options);

    var lessonEditor = new LessonEditorView({
        el: "#lesson-editor"
    });

    $(".btn-save-marks").click(function () {
        var marks_ajax = marks.save();
        var tasks_ajax = tasks_results.save();

        $.when(tasks_ajax, marks_ajax).done(function (data, textStatus, jqXHR) {
            console.log("cool");
            loadToContent(window.location);
        })
    });

    new StudentsCollectionView({
        collection: students,
        el: ".s-table"
    });

    function bind_selectors(selector, callback, collection) {
        if (callback == null)
            return;
        $(selector).each(function (idx, item) {
            var data = $(item).data();
            var out = callback(data, item);
            if (collection && out) {
                collection.add(out);
            }
        })
    }

    function bind() {
        // bind lessons
        bind_selectors(".m-table .t-header .mark", function (data, item) {
            var lesson = new Lesson({
                id: data.id,
                date: data.date,
                group_id: data.group_id,
                discipline_id: data.discipline_id,
                style: data.style,
                description: data.description || "",
                lesson_type: data.lessonType || 1,
                score_ignore: data.scoreIgnore == "True",
                "update-lesson": data.updateLesson,
                "delete-lesson": data.deleteLesson,
                "create-lesson": data.createLesson
            });

            new LessonView({
                model: lesson,
                el: item
            }, {
                lessonEditor: lessonEditor
            });

            return lesson;
        }, lessons);

        // bind labs
        bind_selectors(".l-table .t-header", function (data, item) {
            return new Lab({
                id: data.id,
            });
        }, labs);

        // bind labs
        bind_selectors(".m-labs .m-lab", function (data, item) {
            var labItem =  new LabItem({
                id: data.id,
                title: data.title,
                description: data.description,
                discipline_id: data.discipline_id,
                visible: data.visible,
                regular: data.regular,
                order: data.order
            });

            new LabItemView({
                model: labItem,
                el: item
            }, {

            });

            return labItem
        }, labsItems);

        // bind tasks
        bind_selectors(".l-table .t-header .t-cell-task", function (data, item) {
            return new Task({
                id: data.id,
                lab: labs.get(data.lab)
            });
        }, tasks);


        // bind students
        bind_selectors(".s-table .t-content .t-row", function (data, item) {
            var student = new Student({
                id: data.id,
                name: data.name.toString(),
                second_name: data.secondName.toString(),
                group_id: data.group_id,
                sex: data.sex != "undefined" ? data.sex : 1,
                urlUpdate: data.urlUpdate,
                urlRemove: data.urlRemove,
                urlCreate: data.urlCreate
            });
            new StudentView({
                model: student,
                el: item
            });
            return student
        }, students);

        // bind marks
        bind_selectors(".m-table .t-content .t-cell.mark", function (data, item) {
            if (data.lesson && data.student) {
                var lesson = lessons.get(data.lesson);
                var student = students.get(data.student);
                var mark = new Mark({
                    student: student,
                    lesson: lesson,
                    lesson_type: data.lessonType,
                    value: data.value
                });
                new MarkView({
                    model: mark,
                    el: item
                });
                lesson.get("marks").add(mark);
                return mark;
            }
        }, marks);

        // bind tasks results
        bind_selectors(".l-table .t-content .t-cell.mark", function (data, item) {
            var taskResult = new TaskResult({
                task: tasks.get(data.task),
                student: students.get(data.student),
                done: data.done
            });

            new TaskResultView({
                model: taskResult,
                el: item
            });

            return taskResult;
        }, tasks_results);


    }

    bind();
}

