/* Official and not clone */
// double click on the heart icon
$(".fa-heart").dblclick(function() {
    $(".notification-bubble").show(400);
});

$(document).on("scroll", function() {
    if ($(document).scrollTop() > 50) {
        $(".navigation").addClass("shrink");
    } else {
        $(".navigation").removeClass("shrink");
    }
});
/* Official and not clone */