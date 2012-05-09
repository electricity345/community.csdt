function mycarousel_initCallback(carousel) {
  /*$('.slider-next').bind('click', function() {
    carousel.next();
    return false;
  });

  $('.slider-prev').bind('click', function() {
    carousel.prev();
    return false;
  });*/
    
  $('.slider-nav a').bind('click', function() {
    carousel.scroll(jQuery.jcarousel.intval(jQuery(this).text()));
    return false;
  });
};

function mycarousel_itemFirstInCallback(carousel, item, idx, state) {
  $('.slider-nav ul li a').removeClass('active');
  $('.slider-nav ul li a').eq(idx-1).addClass('active');	
};

$(function(){
  $('.slider').jcarousel({
    auto: 0,
    wrap: "last",
    scroll: 1,
    visible: 1,
    initCallback: mycarousel_initCallback,
    itemFirstInCallback: mycarousel_itemFirstInCallback,
    buttonNextHTML: null,
    buttonPrevHTML: null
  });
  
  //Gallery Hover Effect
  $('.gallery-content ul li').hover(function(){
    $(this).find('.image-hover').show();
  }, function(){
    $(this).find('.image-hover').hide();
  });
});
