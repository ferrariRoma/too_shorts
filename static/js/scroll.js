$(window).scroll(function () {
    let scroll = $(window).scrollTop();
    if (scroll > 400) {
        $("nav").addClass("fixed");
    } else {
        $("nav").removeClass("fixed");
    }
});