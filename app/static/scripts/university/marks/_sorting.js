/**
 * Created by m on 29.06.15.
 */
/***
 * эта функция подключает сортировку оценок студентов по имени / цвете,
 */
$(function () {
    function sortFunctionByPoints(item1, item2) {
        var value1 = $(item1).data("points");
        var value2 = $(item2).data("points");
        return value1 < value2 ? 1 : -1;
    }

    sortFunctionByPoints.title = "По цвету";

    function sortFunctionByName(item1, item2) {
        var value1 = $(item1).data("name");
        var value2 = $(item2).data("name");
        return value1 > value2 ? 1 : -1;
    }

    sortFunctionByName.title = "По имени";

    var sortingFunction = [
        sortFunctionByPoints,
        sortFunctionByName
    ];


    function getSortingIndex() {
        var lastSortingIndex = parseInt($.cookie("sorting"));
        if (isNaN(lastSortingIndex) || lastSortingIndex == undefined) {
            lastSortingIndex = 0;
        }
        return lastSortingIndex % sortingFunction.length
    }


    function sort() {
        if (sortingFunction.length == 0) {
            return;
        }

        var lastSortingIndex = getSortingIndex();

        var sortFunction = sortingFunction[lastSortingIndex];

        var $students = $(".s-table .t-content");
        var $marks = $(".m-table .t-content");

        $students.find(".t-row").sort(sortFunction).appendTo($students);
        $marks.find(".t-row").sort(sortFunction).appendTo($marks);

        $(".btn-students-sorting .btn-text").html(sortingFunction[lastSortingIndex].title);
    }

    $(document).on("click", ".btn-students-sorting", function () {
        var lastSortingIndex = getSortingIndex();
        lastSortingIndex = (lastSortingIndex + 1) % sortingFunction.length;
        $.cookie("sorting", lastSortingIndex, {expires: 100, path: '/'});
        sort();
    });

    $(document).on("load:groups:complete", sort);
});