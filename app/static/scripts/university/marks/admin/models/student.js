/**
 * Created by m on 12.07.15.
 */
var Student = Backbone.Model.extend({
    constructor: function (model, options) {
        Backbone.Model.apply(this, arguments);
        this.reset();
    },

    is_changed: function () {
        return this.old_name != this.get("name") ||
            this.old_second_name != this.get("second_name") ||
            this.old_sex != this.get("sex");
    },

    defaults: function () {
        return {
            marks: new MarksCollection()
        }
    },

    toJSON: function () {
        return {
            'name': this.get("name"),
            'second_name': this.get("second_name"),
            'sex': this.get("sex"),
            'group_id': this.get("group_id")
        }
    },

    save: function (url) {
        var that = this;
        return $.ajax({
            url: this.get("urlUpdate"),
            method: "POST",
            data: that.toJSON()
        }).done(function () {
            that.reset();
        })
    },

    reset: function () {
        this.old_name = this.get("name");
        this.old_second_name = this.get("second_name");
        this.old_sex = this.get("sex");
        this.trigger('change', this);
    }
});


var StudentView = Backbone.View.extend({
    initialize: function () {
        _.bindAll(this, "render");
        this.model.on('change', this.render);
    },

    events: {
        //"click .btn-update": "save",
        "click .btn-remove": "remove",
        "input input": "changed",
        "change input": "changed",
        "click .btn-male": "set_male",
        "click .btn-female": "set_female"
    },

    changed: function (e) {
        this.model.set(e.target.name, e.target.value);
    },

    set_male: function (e) {
        this.model.set("sex", 1)
    },

    set_female: function (e) {
        this.model.set("sex", 0)
    },

    //save: function (e) {
    //    e.preventDefault();
    //    this.model.save($(e.target).data("href"))
    //},

    remove: function (e) {
        e.preventDefault();
        this.model.remove($(e.target).data("href"))
    },

    render: function (e) {
        this.$el.find(".info .name-second-name").html(this.model.get("second_name"));
        this.$el.find(".info .name-name").html(this.model.get("name"));
        this.$el.find(".info .name-n").html(this.model.get("name").substr(0, 1));

        this.$el.toggleClass("modified", this.model.is_changed());


        this.$el.find(".btn-male").toggleClass("btn-primary", this.model.get("sex") == 1);
        this.$el.find(".btn-male").toggleClass("btn-default", this.model.get("sex") != 1);

        this.$el.find(".btn-female").toggleClass("btn-primary", this.model.get("sex") == 0);
        this.$el.find(".btn-female").toggleClass("btn-default", this.model.get("sex") != 0);
    }
});