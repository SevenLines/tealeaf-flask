/**
 * Created by m on 29.06.15.
 */
/***
 * эта функция подключает управление формой отображения оценки баллы / проценты
 */
$(function () {
    var scoringItems = [
        {cls: 'percents', title: "в процентах"},
        {cls: 'points', title: "в баллах"}
    ];

    function getVisibleScoreIndex() {
        var lastScoringIndex = parseInt($.cookie("score"));
        if (isNaN(lastScoringIndex) || lastScoringIndex == undefined) {
            lastScoringIndex = 0;
        }
        return lastScoringIndex % scoringItems.length
    }

    $(document).on("click", ".btn-students-score", function () {
        var lastVisibleScore = getVisibleScoreIndex();
        lastVisibleScore = (lastVisibleScore + 1) % scoringItems.length;
        $.cookie("score", lastVisibleScore, {expires: 100, path: '/'});
        setVisibleScore();
    });

    function setVisibleScore() {
        var lastVisibleScore = getVisibleScoreIndex();
        var scores = $(".s-table .t-content .t-cell .info .score");
        scoringItems.forEach(function (item, index) {
            scores.find("." + item.cls).css({
                display: lastVisibleScore == index ? "block" : "none"
            });
        });
        $(".btn-students-score .btn-text").html(scoringItems[lastVisibleScore].title);
    }

    function setScore() {
        var $scores = $(".s-table .info .score");
        $scores.find(".points").each(function (item) {
            var value = $(this).data("value");
            $(this).html(value);
        });
        $scores.find(".percents").each(function (item) {
            var value = $(this).data("value") + "%";
            $(this).html(value);
        });
    }

    $(document).on("load:groups:complete", setScore);
    $(document).on("load:groups:complete", setVisibleScore);
});