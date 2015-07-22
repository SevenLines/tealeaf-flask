/**
 * Created by m on 22.07.15.
 */
function MarksHoverController() {
    $("#marks-editor").on({
        mouseenter: function () {
            var index = $(this).index();
            $(this).addClass("hover");
            $(".m-table>tbody, .s-table>tbody").each(function (i, item) {
                $($(item).find(">.t-row")[index]).addClass("hover");
            });
        },
        mouseleave: function () {
            $(this).removeClass("hover");
            var index = $(this).index();
            $(".m-table>tbody, .s-table>tbody").each(function (i, item) {
                $($(item).find(">.t-row")[index]).removeClass("hover");
            });
        }
    }, ".m-table>tbody>.t-row,.s-table>tbody>.t-row");
}
