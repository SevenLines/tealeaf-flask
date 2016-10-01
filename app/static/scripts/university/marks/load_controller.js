/**
 * Created by m on 22.07.15.
 */
function LoadController() {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });


    $(function () {
        $(document).trigger("load:groups:complete");
        $(document).trigger("load:complete");

        window.loadToContent = function (url, info, target, callback) {
            var $loadingScreen = $("#loading-screen");
            if (!info) {
            }
            $loadingScreen.find(".info").html(info);

            $("#content").fadeOut({
                duration: "fast",
                complete: function () {
                    $loadingScreen.fadeIn({
                        duration: "fast",
                        complete: function () {
                            $.pjax({
                                url: url,
                                container: '#content-wrapper',
                                timeout: 10000,
                                target: target
                            })
                        }
                    })
                }
            });
            return false;
        };

        $(document).on("click", "a.load-to-content", function () {
            loadToContent(this.href, null, this);
            return false;
        });


        $(document).on("pjax:success", function (e, data, status, xhr, options) {
            var target = e.relatedTarget;

            $(".menu").find(".groups>li, .main>li").removeClass("active");

            if (target) {
                $(target).parents("li").addClass("active");
            }

            $("#loading-screen").fadeOut();
            $("#content").fadeIn();

            $(document).trigger("load:groups:complete");
            $(document).trigger("load:complete");

        });

        $(document).on("pjax:popstate", function (e) {
            if (e.state && e.state.url) {
                var $menu = $(".menu");
                var url = e.state.url.replace(window.location.origin, "");
                var a_tag = $menu.find(".groups>li, .main>li")
                    .find("a[href='" + url + "']");
                $menu.find(".groups>li, .main>li").removeClass("active");
                $(a_tag).parents("li").addClass("active");
            }
        })
    });
}
