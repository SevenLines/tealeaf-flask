/**
 * Created by m on 12.07.15.
 */
var Student = Backbone.Model.extend({
    constructor: function (model, options) {
        Backbone.Model.apply(this, arguments);
        this.reset();
    },

    is_changed: function () {
        if (!this.get('id'))
            return false;
        return this.old_name != this.get("name") ||
            this.old_second_name != this.get("second_name") ||
            this.old_sex != this.get("sex") ||
            this.old_photo != this.get("photo") ||
            this.get("remove_photo");
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
            'group_id': this.get("group_id"),
            'photo': this.get("photo"),
            'remove_photo': this.get("remove_photo")
        }
    },

    save: function () {
        var that = this;
        var formData = new FormData(this.get("photo_form"));
        var json = this.toJSON();
        for (var key in json) {
            if (typeof json[key] != "undefined") {
                formData.append(key, json[key]);
            }
        }
        if (this.get("id")) {
            $.ajax({
                url: this.get("urlUpdate"),
                method: "POST",
                data: formData,
                cache: false,
                contentType: false,
                processData: false
            }).done(function () {
                that.reset();
            })
        } else {
            $.ajax({
                url: this.get("urlCreate"),
                method: "POST",
                data: formData,
                cache: false,
                contentType: false,
                processData: false
            }).done(function () {
                loadToContent(window.location)
            })
        }
    },

    remove: function () {
        $.ajax({
            url: this.get("urlRemove"),
            method: "POST",
        }).done(function () {
            loadToContent(window.location)
        })
    },

    reset: function () {
        this.old_name = this.get("name");
        this.old_second_name = this.get("second_name");
        this.old_sex = this.get("sex");
        this.old_photo = null;
        this.trigger('change', this);
    }
});


var StudentView = Backbone.View.extend({
    initialize: function () {
        _.bindAll(this, "render");
        this.model.on('change', this.render);
    },

    events: {
        "click": "toggleOpen",
        "click .btn-remove": "remove",
        "click .btn-add": "save",
        "click .btn-image-select": "select_image",
        "click .btn-image-remove": "toggle_remove_image",
        "input input": "changed",
        "change input": "changed",
        "click .btn-male": "set_male",
        "click .btn-female": "set_female"
    },

    select_image: function (e) {
        var self = this;
        if (typeof this.file_input == "undefined") {
            // create image selector
            this.form = $("<form><input type='file' name='photo'></form>");
            this.file_input = this.form.find("input");

            this.file_input.on('change', function () {
                var file = this.files[0];
                var fileReader = new FileReader();
                fileReader.onload = function (e) {
                    self.$el.find(".img-photo").get(0).src = e.target.result;
                };
                fileReader.readAsDataURL(file);
                self.model.set("photo", $(this).val());
                self.model.set("photo_form", self.form[0]);
                self.model.set("remove_photo", undefined);
            });
        }
        this.file_input.click();

    },

    toggle_remove_image: function () {
        if (typeof  this.file_input != "undefined") {
            $(this.form).remove();
        }
        if (!this.model.get("remove_photo")) {
            this.last_photo = this.$el.find(".img-photo").attr("src");
            this.$el.find(".img-photo").attr("src", null);
            this.model.set("remove_photo", true);
        } else {
            this.$el.find(".img-photo").attr("src", this.last_photo);
            this.model.set("remove_photo", false);
        }
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

    toggleOpen: function () {
        this.$el.addClass("open");
        var that = this;
        $(document).on("mouseover.studentEditor", function (e) {
            that.onMouseOver(e);
        });
    },

    save: function () {
        this.model.save();
    },

    onMouseOver: function (e) {
        if (!this.$el.hasClass("open")) {
            return;
        }

        var student_menu = this.$el.find(".student-menu")[0];
        var offset = 0;
        var bound = student_menu.getBoundingClientRect();

        var x = e.clientX;
        var y = e.clientY;

        if (bound.left - x > offset
            || bound.top - y > offset
            || x - (bound.left + bound.width) > offset
            || y - (bound.top + bound.height) > offset) {
            this.$el.removeClass("open");
            $(document).off("mouseover.studentEditor");
        }
    },

    remove: function (e) {
        e.preventDefault();
        student = this.model.get("sex") == 0 ? "студентки" : "студента"
        if (confirm([
                "Подтвердите удаление",
                student,
                this.model.get("second_name"),
                this.model.get("name")].join(" "))) {
            this.model.remove();
        }
    },

    render: function (e) {
        this.$el.find(".info .name-second-name").html(this.model.get("second_name"));
        this.$el.find(".info .name-name").html(this.model.get("name"));
        if (this.model.get("name")) {
            this.$el.find(".info .name-n").html(this.model.get("name").substr(0, 1));
        }

        this.$el.toggleClass("modified", this.model.is_changed());


        this.$el.find(".btn-male").toggleClass("btn-primary", this.model.get("sex") == 1);
        this.$el.find(".btn-male").toggleClass("btn-default", this.model.get("sex") != 1);

        this.$el.find(".btn-female").toggleClass("btn-primary", this.model.get("sex") == 0);
        this.$el.find(".btn-female").toggleClass("btn-default", this.model.get("sex") != 0);
    }
});