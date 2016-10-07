/**
 * Created by m on 09.09.16.
 */
function ViewController() {
    var state = $.cookie("visibleState") != "true";

    function toggleVisible() {
        state = !state;

        $('.t-row').filter(function () {
            return $(this).data('percents') < 25;
        }).toggle(state);

        var el = $(".btn-hide-nulls");
        el.find("span").toggleClass("fa-eye", state);
        el.find("span").toggleClass("fa-eye-slash", !state);

        $.cookie("visibleState", state, {expires: 100, path: '/'});
    }

    $(".btn-hide-nulls").on("click", toggleVisible);
    toggleVisible();
}