/**
 * Created by m on 29.06.15.
 */
/***
 * эта функция раскрашивает строки студентов в соответствующие цвета
 */
function ColorController() {
    function setColors() {
        var $rows = $(".s-table .t-content .t-row ");
        $rows.each(function (item) {
            var percents = $(this).data("percents");
            var $info = $(this).find(".info");
            $info.css({
                "background-color": tinycolor.mix(tinycolor("#FFE6DD"), tinycolor("#DBFF6D"), percents)
            });
            if (percents >= 100) {
                $info.addClass("god");
            } else {
                $info.removeClass("god");
            }
        });
    }

    $(document).on("load:groups:complete", setColors);
};