/**
 * Created by m on 29.06.15.
 */
$(function () {
    function addTooltips() {
        $('[data-toggle="tooltip"]').tooltip();
    }

    $(document).on("load:groups:complete", addTooltips);
});