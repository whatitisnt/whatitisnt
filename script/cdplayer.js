$("#listenbutton").click(function () {
  $("#cdstart").click();
});

$("#listenbuttonmob").click(function () {
  $("#cdstart").click();
});

$(".cdplayer-lyricswrapper").click(function () {
  $(".splide__pagination__page").eq(0).click();
});

$(".track1").on("click", function () {
  if ($("#trackname1").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track1")[0].pause();
    $(".track1").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track1")[0].play();
    $(".track1").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab1").click();
    $("#lyricstab1mob").click();
  }
});

$(".track2").on("click", function () {
  if ($("#trackname2").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track2")[0].pause();
    $(".track2").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track2")[0].play();
    $(".track2").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab2").click();
    $("#lyricstab2mob").click();
  }
});

$(".track3").on("click", function () {
  if ($("#trackname3").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track3")[0].pause();
    $(".track3").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track3")[0].play();
    $(".track3").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab3").click();
    $("#lyricstab3mob").click();
  }
});

$(".track4").on("click", function () {
  if ($("#trackname4").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track4")[0].pause();
    $(".track4").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track4")[0].play();
    $(".track4").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab4").click();
    $("#lyricstab4mob").click();
  }
});

$(".track5").on("click", function () {
  if ($("#trackname5").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track5")[0].pause();
    $(".track5").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track5")[0].play();
    $(".track5").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab5").click();
    $("#lyricstab5mob").click();
  }
});

$(".track6").on("click", function () {
  if ($("#trackname6").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track6")[0].pause();
    $(".track6").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track6")[0].play();
    $(".track6").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab6").click();
    $("#lyricstab6mob").click();
  }
});

$(".track7").on("click", function () {
  if ($("#trackname7").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track7")[0].pause();
    $(".track7").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track7")[0].play();
    $(".track7").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab7").click();
    $("#lyricstab7mob").click();
  }
});

$(".track8").on("click", function () {
  if ($("#trackname8").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track8")[0].pause();
    $(".track8").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track8")[0].play();
    $(".track8").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab8").click();
    $("#lyricstab8mob").click();
  }
});

$(".track9").on("click", function () {
  if ($("#trackname9").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track9")[0].pause();
    $(".track9").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track9")[0].play();
    $(".track9").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab9").click();
    $("#lyricstab9mob").click();
  }
});

$(".track10").on("click", function () {
  if ($("#trackname10").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track10")[0].pause();
    $(".track10").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track10")[0].play();
    $(".track10").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab10").click();
    $("#lyricstab10mob").click();
  }
});

$(".track11").on("click", function () {
  if ($("#trackname11").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track11")[0].pause();
    $(".track11").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track11")[0].play();
    $(".track11").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab11").click();
    $("#lyricstab11mob").click();
  }
});

$(".track12").on("click", function () {
  if ($("#trackname12").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track12")[0].pause();
    $(".track12").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track12")[0].play();
    $(".track12").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab12").click();
    $("#lyricstab12mob").click();
  }
});

$(".track13").on("click", function () {
  if ($("#trackname13").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track13")[0].pause();
    $(".track13").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track13")[0].play();
    $(".track13").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab13").click();
    $("#lyricstab13mob").click();
  }
});

$(".track14").on("click", function () {
  if ($("#trackname14").hasClass("playing")) {
    $(".playing").removeClass("playing");
    $("audio#track14")[0].pause();
    $(".track14").find(".track-name").addClass("paused");
    $(".disc-img").css("animation-play-state", "paused");
  } else {
    $(".playing").removeClass("playing");
    $(".paused").removeClass("paused");
    $("audio#track14")[0].play();
    $(".track14").find(".track-name").addClass("playing");
    $(".disc-img").css("animation-play-state", "running");
    $("#lyricstab14").click();
    $("#lyricstab14mob").click();
  }
});

$("audio#track1").on("ended", function () {
  console.log("track1 ended");
  $(".track2.is--pc").click();
});

$("audio#track2").on("ended", function () {
  console.log("track2 ended");
  $(".track3.is--pc").click();
});

$("audio#track3").on("ended", function () {
  console.log("track3 ended");
  $(".track4.is--pc").click();
});

$("audio#track4").on("ended", function () {
  console.log("track4 ended");
  $(".track5.is--pc").click();
});

$("audio#track5").on("ended", function () {
  console.log("track5 ended");
  $(".track6.is--pc").click();
});

$("audio#track6").on("ended", function () {
  console.log("track6 ended");
  $(".track7.is--pc").click();
});

$("audio#track7").on("ended", function () {
  console.log("track7 ended");
  $(".track8.is--pc").click();
});

$("audio#track8").on("ended", function () {
  console.log("track8 ended");
  $(".track9.is--pc").click();
});

$("audio#track9").on("ended", function () {
  console.log("track9 ended");
  $(".track10.is--pc").click();
});

$("audio#track10").on("ended", function () {
  console.log("track10 ended");
  $(".track11.is--pc").click();
});

$("audio#track11").on("ended", function () {
  console.log("track11 ended");
  $(".track12.is--pc").click();
});

$("audio#track12").on("ended", function () {
  console.log("track12 ended");
  $(".track13.is--pc").click();
});

$("audio#track13").on("ended", function () {
  console.log("track13 ended");
  $(".track14.is--pc").click();
});

$("audio#track14").on("ended", function () {
  console.log("track14 ended");
  $(".track1.is--pc").click();
});
