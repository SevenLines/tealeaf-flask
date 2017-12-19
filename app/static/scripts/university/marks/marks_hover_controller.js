/**
 * Created by m on 22.07.15.
 */
function MarksHoverController() {
    $("#marks-editor").on({
        mouseenter: function () {
            var index = $(this).index();
            $(this).addClass("hover");
            $(".m-table>tbody, .s-table>tbody, .l-table>tbody").each(function (i, item) {
                $($(item).find(">.t-row")[index]).addClass("hover");
            });
        },
        mouseleave: function () {
            $(this).removeClass("hover");
            var index = $(this).index();
            $(".m-table>tbody, .s-table>tbody, .l-table>tbody").each(function (i, item) {
                $($(item).find(">.t-row")[index]).removeClass("hover");
            });
        }
    }, ".m-table>tbody>.t-row,.s-table>tbody>.t-row,.l-table>tbody>.t-row");


    var previous_targets = [];
    $(".l-table .t-content td").not("").mouseover(function (e) {
        var target = $(e.currentTarget);

        var new_targets = [];
        var tr = target.parents("tr.t-row");
        var top = tr.prev().find("td").get(target.index());
        var bottom = tr.next().find("td").get(target.index());
        if (top) {
            new_targets.push($(top));
        }
        if (bottom) {
            new_targets.push($(bottom));
        }
        if (target.prev()) {
            new_targets.push(target.prev());
        }
        if (target.next()) {
            new_targets.push(target.next());
        }
        new_targets.push(target);

        previous_targets.filter(function (item) {
            return new_targets.indexOf(item) === -1
        }).forEach(function (item) {
            setTimeout(function () {
                item.removeClass("hover-hide");
            }, 1000)
        });

        new_targets.forEach(function (item) {
            item.addClass("hover-hide");
        });

        previous_targets = new_targets;
    });

}
