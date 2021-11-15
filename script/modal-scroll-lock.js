$('[scroll=enable]').click(function() {
	unLockScroll();
});

$('[scroll=disable]').click(function() {
	lockScroll();
});


let scrollPosition = [];
let marginB;
let marginR;
const $html = $('html');
const $body = $('body');

function lockScroll(){
  setTimeout(function () {
    let initWidth = $body.outerWidth();
    let initHeight = $body.outerHeight();
    scrollPosition = [
        self.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft,
        self.pageYOffset || document.documentElement.scrollTop  || document.body.scrollTop
    ];
    $html.css('overflow', 'hidden');
    window.scrollTo(scrollPosition[0], scrollPosition[1]);

    marginR = $body.outerWidth()-initWidth;
    marginB = $body.outerHeight()-initHeight;
    $body.css({'margin-right': marginR,'margin-bottom': marginB});
  }, 10);
}

function unLockScroll(){
  setTimeout(function () {
    $html.css('overflow', 'initial');
    window.scrollTo(scrollPosition[0], scrollPosition[1]);
    $body.css({'margin-right': 0, 'margin-bottom': 0});
  }, 10);
}