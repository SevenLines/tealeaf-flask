/**
 * Created by m on 20.07.15.
 */
var TaskResult = Backbone.Model.extend({
    constructor: function () {
        Backbone.Model.apply(this, arguments);
        this.done = this.get("done");
    },

    is_changed: function () {
        return this.get("done") != this.done;
    },

    reset: function () {
        this.done = this.get("done");
        this.trigger('change', this);
    },

    toJSON: function () {
        return {
            'student_id': this.get("student").id,
            'task_id': this.get("task").id,
            'done': this.get("done")
        }
    },

    toggle: function () {
        this.set("done", !this.get("done"));
    }
});

var TaskResultView = Backbone.View.extend({
    initialize: function () {
        _.bindAll(this, "render");
        this.model.on('change', this.render);
    },

    events: {
        "click": "toggle"
    },

    toggle: function () {
        console.log("cool");
        this.model.toggle();
    },

    render: function () {
        this.$el.toggleClass("done", this.model.get("done"));
        this.$el.toggleClass("modified", this.model.is_changed());
    }
});