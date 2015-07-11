/**
 * Created by m on 12.07.15.
 */
var Mark = Backbone.Model.extend({
    constructor: function () {
        Backbone.Model.apply(this, arguments);
        this.old_value = this.get("value");
    },

    is_changed: function () {
        return this.get("value") != this.old_value;
    },

    reset: function () {
        this.old_value = this.get("value");
        this.trigger('change', this);
    },

    toJSON: function () {
        return {
            'student_id': this.get("student").id,
            'lesson_id': this.get("lesson").id,
            'value': this.get("value")
        }
    }
});

var last_offset = {
    left: -1,
    top: -1
};


var MarkView = Backbone.View.extend({
    initialize: function () {
        _.bindAll(this, "render");
        this.model.bind('change', this.render);
    },

    events: {
        "click": "showMarkSelector"
    },

    render: function () {
        this.$el.attr("class", null);
        this.$el.addClass([
            "t-cell",
            "mark",
            this.model.get("lesson").get("style"),
            this.new_style,
            this.model.is_changed() ? "modified" : ""
        ].join(" "));
        return this;
    },

    markSelectorItemChoose: function (selected_item) {
        var new_value = $(selected_item).data("value");
        this.new_style = $(selected_item).data("class");
        this.model.set('value', new_value);
        $mark_selector.hide();
    },

    showMarkSelector: function () {
        var that = this;


        $mark_selector = $("#mark-selector");
        $mark_selector.find("li").unbind("click");
        $mark_selector.find("li").one("click", function () {
            that.markSelectorItemChoose(this);
        });


        that.class_list = [];
        $mark_selector.find("li").each(function (idx, item) {
            that.class_list.push($(item).data("class"));
        });

        var offset = that.$el.offset();
        var width = that.el.clientWidth * 1.1;
        var height = that.el.clientHeight;

        var item_width = 28;
        var ul_width = $mark_selector.find("ul").first().width();

        var items = $mark_selector.show().offset({
            left: offset.left - ul_width / 2 + width / 2,
            top: offset.top - ul_width / 2 + height / 2
        }).find("li");

        last_offset.left = offset.left + (width - item_width) / 2;
        last_offset.top = offset.top + (height - item_width) / 2;

        if (items.size()) {
            var radius = 35;
            var angle = 2 * Math.PI / (items.size());
            items.each(function (i, item) {
                var item_value = $(item).data("value");
                if (item_value != that.model.get('value')) {
                    $(item).offset({
                        left: last_offset.left + radius * Math.cos(i * angle),
                        top: last_offset.top + radius * Math.sin(i * angle)
                    });
                } else {
                    $(item).offset({
                        left: last_offset.left,
                        top: last_offset.top
                    });
                }
            });
        }

        $mark_selector.find(".mark").removeClass("lect exam test current");
        $mark_selector.find(".mark").toggleClass(this.model.get("lesson").get("style"), true);
    }
});

$("#mark-selector")
