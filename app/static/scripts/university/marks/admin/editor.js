/**
 * Created by m on 12.07.15.
 */
var LessonsCollection = Backbone.Collection.extend({
    model: Lesson
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

        $.ajax({
            url: this.urls.save_marks,
            data: JSON.stringify(changed.toJSON()),
            method: "POST",
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });

        changed.forEach(function (mark) {
            mark.reset();
        });

        loadToContent(window.location);
    }
});

var MarksCollectionSaveButton = Backbone.View.extend({
    events: {
        "click": "save"
    },

    save: function () {
        this.collection.save();
    },

    render: function () {
        return this;
    }
});


function EditorController(options) {
    var lessons = new LessonsCollection([], options);
    var students = new StudentsCollection([], options);
    var marks = new MarksCollection([], options);

    var lessonEditor = new LessonEditorView({
        el: "#lesson-editor"
    });


    new MarksCollectionSaveButton({
        collection: marks,
        el: ".btn-save-marks"
    });

    new StudentsCollectionView({
        collection: students,
        el: ".s-table"
    });

    function bind() {
        // bind lessons
        $(".m-table .t-header .mark").each(function (idx, item) {
            var data = $(item).data();
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
            lessons.add(lesson);
        });

        // bind students
        $(".s-table .t-content .t-row").each(function (idx, item) {
            var data = $(item).data();
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
            console.log(student);
            new StudentView({
                model: student,
                el: item
            });
            students.add(student);
        });

        // bind marks
        $(".m-table .t-content .t-cell.mark").each(function (idx, item) {
            var data = $(item).data();
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
                    el: item,
                });
                lesson.get("marks").add(mark);
                marks.add(mark);
            }
        });

    }

    bind();
}

