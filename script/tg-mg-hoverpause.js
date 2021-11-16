$('.mg-link-wrapper').on('mouseenter', function() {
  $('.tg__profilelink, .story__headshot-tg-img').css('animation-play-state', 'paused');
});

$('.mg-link-wrapper').on('mouseleave', function() {
  $('.tg__profilelink, .story__headshot-tg-img').css('animation-play-state', 'running');
});

$('.tg-link-wrapper').on('mouseenter', function() {
  $('.mg__profilelink, .story__headshot-mg-img').css('animation-play-state', 'paused');
});

$('.tg-link-wrapper').on('mouseleave', function() {
  $('.mg__profilelink, .story__headshot-mg-img').css('animation-play-state', 'running');
});