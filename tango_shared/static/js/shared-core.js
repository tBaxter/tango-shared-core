
// initialize slidwshows and top assets.
if ($('.slideshow').length > 0) {
  var $thumbnails = $('.rs-thumb-wrap a');

  $('.slideshow').refineSlide({
      transition : 'cubeH',
      thumbMargin: 0,
      useArrows: true,
      transitionDuration: 500,
  });

  $thumbnails.css('height', $thumbnails.eq(0).outerWidth() * 0.65);

  // set up thumbnail previewer
  if ($thumbnails.outerWidth() < 80) {
      var $previewer = $('<span class="rs-thumb-viewer"></span>');
      $('.rs-thumb-wrap').prepend($previewer);
      
      $thumbnails.hover(function() {
        $previewer.css('left', (this.offsetLeft + this.offsetWidth/2)).toggle();
    });
  }

  // set up swipe functions
  $('.rs-wrap').hammer().on("swipeleft", function() {
      $('.rs-arrows .rs-prev').click();
  });
  $('.rs-slider').hammer().on("swiperight", function() {
      $('.rs-arrows .rs-next').click();
  });
  // initialize fullscreen toggler
  $('.embiggen-toggle').click(function() {
      $('.rs-wrap').toggleClass('rs-fullscreen');
      $thumbnails.css('height', 50);
  });
}