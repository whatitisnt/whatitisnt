function slider4() {
  let splides = $(".slider4");
  for (let i = 0, splideLength = splides.length; i < splideLength; i++) {
    new Splide(splides[i], {
      // Desktop on down
      perPage: 3,
      perMove: 1,
      focus: "center", // 0 = left and 'center' = center
      type: "loop", // 'loop' or 'slide'
      gap: "5em", // space between slides
      arrows: false, // 'slider' or false
      pagination: "slider", // 'slider' or false
      speed: 600, // transition speed in miliseconds
      dragAngleThreshold: 30, // default is 30
      autoWidth: true, // for cards with differing widths
      rewind: false, // go back to beginning when reach end
      rewindSpeed: 400,
      autoplay: true,
      interval: 3000,
      pauseOnHover: true,
      drag: true,
      waitForTransition: true,
      updateOnMove: false,
      preloadPages: 3,
      slideFocus: false,
      cloneStatus: false,
      trimSpace: false, // true removes empty space from end of list
      classes: {
        pagination: "splide__pagination is--topslider",
        page: "splide__pagination__page is--topslider"
      },
      breakpoints: {
        991: {
          // Tablet
          gap: "0em" // space between slides
        },
        767: {
          // Mobile Landscape
        },
        479: {
          // Mobile Portrait
        }
      }
    }).mount();
  }
}
slider4();
