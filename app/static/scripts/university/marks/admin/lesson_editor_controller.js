/**
 * Created by m on 06.07.15.
 */
function LessonEditorController() {
    var lastLessonItem = null;
    var self = this;


    var block = false;
    $(document).on("mouseover", ".m-table .t-header .mark", function () {
        if (block)
            return;
        block = true;

        var $lessonEditor = $("#lesson-editor");
        $lessonEditor.addClass("lesson-editor-visible");
        $lessonEditor.fadeIn("fast");

        try {
            if (this == lastLessonItem) {
                return;
            }

            lastLessonItem = this;

            var lessonEditorWidth = $lessonEditor.width();

            var $cell = $(this).parents("td");

            var cellOffset = $cell.offset();

            $lessonEditor.offset({
                left: cellOffset.left - lessonEditorWidth / 2,
                top: cellOffset.top + $cell.height()
            });

            self.setEditor(this);
        } finally {
            block = false;
        }
    });

    self.setEditor = function (cell_item) {
        var $cell_item = $(cell_item);
        var lessonEditorForm = $("#lesson-editor")[0];
        $(lessonEditorForm).removeClass("test exam lect laba");
        $(lessonEditorForm).addClass($cell_item.data('style'));
        lessonEditorForm.date.value = $cell_item.data("date");
        lessonEditorForm.description.value = $cell_item.data("description");
        lessonEditorForm.lesson_type.value = $cell_item.data("lesson-type");
        lessonEditorForm.score_ignore.checked = $cell_item.data("score-ignore") == "True";

        var $dateSelector = $($("#lesson-editor")[0].date);
        if (!$dateSelector.data("DateTimePicker")) {
            $dateSelector.datetimepicker({
                inline: true,
                format: "YYYY-MM-DD"
            });
        }
        $dateSelector.data("DateTimePicker").date(lessonEditorForm.date.value);
    };

    $(document).on("mouseover", function (e) {
        var $lessonEditor = $("#lesson-editor");
        if (!$lessonEditor.hasClass("lesson-editor-visible")) {
            return;
        }

        var offset = 2;
        var bound = $lessonEditor[0].getBoundingClientRect();

        var x = e.clientX;
        var y = e.clientY;

        if (bound.left - x > offset
            || bound.top - y > 20 * offset
            || x - (bound.left + bound.width) > offset
            || y - (bound.top + bound.height) > offset) {
            $lessonEditor.removeClass("lesson-editor-visible");
            $lessonEditor.fadeOut("fast");

            var $dateSelector = $($("#lesson-editor")[0].date);
            //$dateSelector.datetimepicker('hide');
        }
    });


};

