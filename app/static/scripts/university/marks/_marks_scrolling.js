/**
 * Created by m on 29.06.15.
 */
/***
 * эта функция подключает скроллинг таблицы оценок мышью
 */
function ScrollController() {
    var containerMoved = false;
    (function () {

        var lastX = -1;
        var leftButtonDown = false;
        var funcScroll = function (e) {
            var left = e.clientX;
            if (leftButtonDown) {
                if (lastX != -1 && Math.abs(lastX - left) > 2) {
                    this.scrollLeft += lastX - left;
                    $.cookie("lastScroll", this.scrollLeft);
                    var containerMoved = true;
                }
            }
            lastX = left;
        };
        $(document).on({
            mousedown: function (e) {
                if (e.which === 1) {
                    leftButtonDown = true;
                    return false;
                }
            },
            touchmove: funcScroll,
            mousemove: funcScroll
        }, ".m-table-container");

        $(document).mouseup(function (e) {
            if (leftButtonDown) {
                leftButtonDown = false;
                setTimeout(function () {
                    self.containerMoved = false;
                }, 60);
            }
        });
    })();
};
