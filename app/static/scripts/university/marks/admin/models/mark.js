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


// copypaste from python version
var MARK_BASE = 0;
var MARK_SPECIAL = 1000;

var MARK_BLACK_HOLE = MARK_BASE - (MARK_SPECIAL + 1);
var MARK_ABSENT = MARK_BASE - 2;
var MARK_EMPTY = MARK_BASE;
var MARK_NORMAL = MARK_BASE + 1;
var MARK_GOOD = MARK_BASE + 2;
var MARK_EXCELLENT = MARK_BASE + 3;
var MARK_AWESOME = MARK_BASE + 4;
var MARK_FANTASTIC = MARK_BASE + 5;
var MARK_INCREDIBLE = MARK_BASE + 6;
var MARK_SHINING = MARK_BASE + (MARK_SPECIAL + 1);
var MARK_MERCY = MARK_BASE + (MARK_SPECIAL + 2);
var MARK_KEEP = MARK_BASE + (MARK_SPECIAL + 3);

mark_styles = {};
mark_styles[MARK_BLACK_HOLE] = 'black-hole';
mark_styles[MARK_ABSENT] = 'absent';
mark_styles[MARK_EMPTY] = 'empty';
mark_styles[MARK_NORMAL] = 'normal';
mark_styles[MARK_GOOD] = 'good';
mark_styles[MARK_EXCELLENT] = 'excellent';
mark_styles[MARK_AWESOME] = 'awesome';
mark_styles[MARK_FANTASTIC] = 'fantastic';
mark_styles[MARK_INCREDIBLE] = 'incredible';
mark_styles[MARK_SHINING] = 'shining';
mark_styles[MARK_MERCY] = 'mercy';

var MarkView = Backbone.View.extend({
    initialize: function () {
        _.bindAll(this, "render");
        this.model.on('change', this.render);
        this.model.get("lesson").on("change:style", this.render);
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
            mark_styles[this.model.get("value")],
            this.model.is_changed() ? "modified" : ""
        ].join(" "));
        return this;
    },

    markSelectorItemChoose: function (selected_item) {
        var new_value = $(selected_item).data("value");
        this.new_style = $(selected_item).data("class");
        this.model.set('value', new_value);
        $mark_selector.fadeOut("fast");
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

        var items = $mark_selector.fadeIn("fast").offset({
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

        $(document).on("mouseover.markSelector", function (e) {
            console.log(e);
            var x = e.pageX;
            var y = e.pageY;
            var radius = width + 10;

            var xdiff = (x - (last_offset.left + 28 / 2));
            var ydiff = (y - (last_offset.top + 36 / 2));

            console.log(last_offset, e.clientX, e.clientY);


            if (Math.sqrt(xdiff * xdiff + ydiff * ydiff) > radius) {
                $(document).off("mouseover.markSelector");
                $mark_selector.fadeOut("fast");
            }
        });

        $mark_selector.find(".mark").removeClass("lect exam test current");
        $mark_selector.find(".mark").toggleClass(this.model.get("lesson").get("style"), true);
    }
});

