/**
 * Created by m on 12.07.15.
 */
var Lesson = Backbone.Model.extend({
    defaults: function () {
        return {
            marks: new MarksCollection()
        }
    }
});

var LessonEditorView = Backbone.View.extend({

    events: {
        "change input": "changed",
        "change select": "changed",
        "input textarea": "changed"
    },

    constructor: function (model, options) {
        Backbone.View.apply(this, arguments);
        this.lastLessonView = null;

        $(this.el.date).datetimepicker({
            inline: true,
            format: "YYYY-MM-DD"
        });

        var that = this;

        this.styles = {
            1: "",
            2: "test",
            3: "lect",
            4: "laba",
            5: "exam"
        }
    },

    onMouseOver: function (e) {
        if (!this.$el.hasClass("lesson-editor-visible")) {
            return;
        }

        var offset = 2;
        var bound = this.$el[0].getBoundingClientRect();

        var x = e.clientX;
        var y = e.clientY;

        if (bound.left - x > offset
            || bound.top - y > 20 * offset
            || x - (bound.left + bound.width) > offset
            || y - (bound.top + bound.height) > offset) {
            this.$el.removeClass("lesson-editor-visible");
            this.$el.fadeOut("fast");
            $(document).off("mouseover.lessonEditor");
        }
    },

    changed: function () {
        console.log(this);
        this.lastLessonView.model.set({
            "description": this.el.description.value,
            "lesson_type": this.el.lesson_type.value,
            "style": this.styles[this.el.lesson_type.value],
            "score_ignore": this.el.description.checked,
            "date": this.el.date.value
        });
    },

    render: function () {
        if (this.lastLessonView) {
            this.el.description.value = this.lastLessonView.model.get("description");
            this.el.lesson_type.value = this.lastLessonView.model.get("lesson_type");
            this.el.score_ignore.checked = this.lastLessonView.model.get("score_ignore");

            this.el.date.value = this.lastLessonView.model.get("date");
            $(this.el.date).data("DateTimePicker").date(this.lastLessonView.model.get("date"));
        }
        return this;
    },

    show: function (lesson_view) {
        this.$el.addClass("lesson-editor-visible");

        var that = this;
        $(document).on("mouseover.lessonEditor", function (e) {
            that.onMouseOver(e);
        });

        this.$el.fadeIn("fast");

        if (lesson_view == this.lastLessonView) {
            return;
        }

        this.lastLessonView = lesson_view;

        var lessonEditorWidth = this.$el.width();

        var $cell = lesson_view.$el.parents("td");

        var cellOffset = $cell.offset();

        this.$el.offset({
            left: cellOffset.left - lessonEditorWidth / 2,
            top: cellOffset.top + $cell.height()
        });

        this.render();
    }
});


var LessonView = Backbone.View.extend({
    constructor: function (model, options) {
        Backbone.View.apply(this, arguments);
        this.lessonEditor = options.lessonEditor;
        _.bindAll(this, "render");
        this.model.bind('change', this.render);
    },

    events: {
        "click": "openEditor"
    },

    render: function () {
        this.$el.removeClass();
        this.$el.addClass([
            "mark t-cell t-cell-head",
            this.model.get("style")
        ].join(" "));

        //this.model.get("marks").forEach(function (mark) {
        //    mark.render();
        //})
    },

    openEditor: function () {
        this.lessonEditor.show(this);
    }
});