/**
 * Created by m on 29.06.15.
 */
(function () {

    var last_offset = {
        left: 0,
        top: 0
    };

    var $mark_selector;
    var current_target;
    var marks_selector = ".m-table .t-content .t-cell.mark";

    function saveMarks() {
        var data_to_save = [];
        $(marks_selector+".modified").each(function (index, item) {
            value = $(item).data("value");
            student = $(item).data("student");
            lesson = $(item).data("lesson");
            data_to_save.push({
                student: student,
                lesson: lesson,
                value: value
            })
        });

        if (data_to_save.length) {
            $.post(COMMON_URLS.marks_save_batch, {
                marks: data_to_save
            }).done(function () {
                loadToContent(location, "<h2>Успешно сохранено!<br>Обновляю кеш...</h2>");
            })
        }
    }

    function markSelectorItemChoose() {
        var $item = $(this);
        var new_value = $item.data("value");
        var old_value = $(current_target).data("old-value");

        if (current_target) {
            $mark_selector.find("li").each(function (index, item) {
                $(current_target).removeClass($(item).data("class"));
            });
            $(current_target).data("value", new_value);
            $(current_target).addClass($item.data("class"));

            if (new_value != old_value) {
                $(current_target).addClass("modified");
            } else {
                $(current_target).removeClass("modified");
            }
        }
        $mark_selector.hide();
    }

    function showMarkSelector() {
        current_target = this;
        $mark_selector = $("#mark-selector");

        var target_value = $(this).data("value");
        var lesson_type_cls = $(this).data("lesson-type");
        var offset = $(current_target).offset();
        var width = current_target.clientWidth * 1.1;
        var height = current_target.clientHeight;

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
                if (item_value != target_value) {
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
        $mark_selector.find(".mark").toggleClass(lesson_type_cls, true);
    }

    $(document).on("click", marks_selector, showMarkSelector);
    $(document).on("click", "#mark-selector li", markSelectorItemChoose);
    $(document).on("click", "#marks-editor .admin-line .btn-save-marks", saveMarks);

})();