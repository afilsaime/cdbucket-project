<!-- ================================================== -->
<!-- =============== START STARTER JS ================ -->
<!-- ================================================== -->
  
jQuery(document).ready(function(){
  
  "use strict";

  // FitVides Option
  jQuery("html").fitVids({ customSelector: "iframe"});

  // LightBox Options
  jQuery(".attachment").find('a > img:not(.attachment-thumbnail)').parent().attr('rel','gallery').fancybox({
    fitToView: true,
    autoSize :  true,
    margin : 30,
    autoScale : true,
    width : '100%',
    height : '100%',
    showNavArrows: true,
    showCloseButton: true,
    helpers : {
      media : {}
    }
  });

  jQuery(".lightbox").attr('rel','gallery').fancybox({
    fitToView: true,
    autoSize :  true,
    margin : 30,
    autoScale : true,
    width : '100%',
    height : '100%',
    showNavArrows: true,
    showCloseButton: true,
    helpers : {
      media : {}
    }
  });
  
  // "single-post-content" is the class of blog-single content container
  jQuery(".single-post-content").find('a > img').parent().attr('rel','gallery').fancybox({
    fitToView: true,
    autoSize :  true,
    margin : 30,
    autoScale : true,
    width : '100%',
    height : '100%',
    showNavArrows: true,
    showCloseButton: true,
    helpers : {
      media : {}
    }
  });

  //Activate the "star" plugin from StarHomePage
  jQuery(".star").each(function() {
      postars(jQuery('.cover').get(0)).init();
  });

  //Start Home-Video-Player
  jQuery(function(){
    jQuery(".player").YTPlayer();
  });

  //Page Loader

  jQuery('.page-loader').delay(800).fadeOut('slow');

  //Page Loader Ends

  //Start RyalSlider
  function royalSliderAva() {

    jQuery('#ava-slider').each(function(){

      var wH = jQuery(window).height();

      jQuery(this).parent().css('height',wH);
      
      jQuery(this).css('height',wH);

      jQuery(this).royalSlider({
        arrowsNav: true,
        loop: false,
        keyboardNavEnabled: true,
        controlsInside: false,
        fadeinLoadedSlide: true,
        imageScaleMode: 'fill',
        arrowsNavAutoHide: false,
        autoScaleSlider: false,
        controlNavigation: false,
        thumbsFitInViewport: false,
        navigateByClick: true,
        startSlideId: 0,
        autoPlay: false,
        transitionType:'move',
        globalCaption: false,
        slidesSpacing: 0,
        deeplinking: {
        enabled: true,
        change: false,

        },
      });
    });
  };

  function afterRSInit() {

    jQuery('.rsContent .rsImg').each(function(){

      var thisSrc = jQuery(this).attr('src');

      jQuery(this).hide();

    });

    jQuery(window).scroll(function(){

      var actualScroll = jQuery(window).scrollTop() * 0.5;

      jQuery('.rsContent').css({
        'background-position': '50% ' + actualScroll + 'px'
      });

      console.log(actualScroll);

    });

  }

  afterRSInit();

  royalSliderAva();

  jQuery(window).resize(function(){

    afterRSInit();

    royalSliderAva();

  });
  /***********************************************************************************************/
  /* MENU */
  /***********************************************************************************************/
  jQuery('.open-menu').on('click', function(){

    jQuery(this).toggleClass('active');

    jQuery('.menu-fixed-container').toggleClass('open');

  });

  jQuery('.x-filter').on('click',function(){

    jQuery('.open-menu').toggleClass('active');

    jQuery('.menu-fixed-container').toggleClass('open');

  });

  jQuery('.menu-fixed-container > nav > ul > li > a').on('click',function(){

        jQuery(this).parent().siblings().toggleClass('no-hovered');
        jQuery(this).parent().toggleClass('click');
        jQuery(this).parent().siblings().removeClass('click'); 
    });

  jQuery('.menu-fixed-container > nav > ul > li > .sub-menu').parent().addClass('hover-sub-menu');

  jQuery('.menu-fixed-container > nav > ul > li  > .sub-menu').on('click',function(){

      jQuery(this).parent().toggleClass('hovered-sub-menu ');

  });

  jQuery('.menu-fixed-container nav ul li .sub-menu').parent().find('> a').on('click', function(e){

    e.preventDefault();

  });
/***********************************************************************************************/
/* END MENU */
/***********************************************************************************************/

/***********************************************************************************************/
  /* COUNTER */
  /***********************************************************************************************/
  if ( jQuery( '.sm-countdown' ).length > 0 ) {
  
      jQuery( '.sm-countdown' ).each( function() {
        var jQuerythis = jQuery( this );
        jQuerythis.ccountdown( jQuerythis.data( 'date' ) );
      } );
      jQuery( '.sm-countdown.sm-style1 .element' ).knob({
        draw : function () {
          var a = this.angle(this.cv)  // Angle
            , sa = this.startAngle     // Start angle
            , ea = sa + a        // End angle
            , r = true
            , delta_deg = 6
            , delta_rad = delta_deg / 180 * Math.PI;
  
          this.g.lineWidth = this.lineWidth;
  
          this.g.strokeStyle = r ? this.o.fgColor : this.fgColor ;
          var sa_deg = parseInt(sa / Math.PI * 180, 10) % 360;
          var ea_deg = parseInt(ea / Math.PI * 180, 10) % 360;
          var idx =0 ;
          if (ea_deg < sa_deg) ea_deg += 360;
          var ea_deg_round = Math.round(ea_deg / delta_deg) * delta_deg;
          for (var ta_deg = sa_deg; ta_deg <= ea_deg_round; ta_deg += delta_deg) {
            this.g.beginPath();
            var ta_rad = ta_deg / 180 * Math.PI;
            this.g.arc(this.xy, this.xy, this.radius, -( ta_rad - delta_rad / 4 ), -( ta_rad + delta_rad / 4 ), true); 
            this.g.stroke();
          }
          var rs_deg = ea_deg_round + delta_deg;
          for (var ta_deg = rs_deg; ta_deg < sa_deg + 360; ta_deg += delta_deg) {
            this.g.beginPath();
            var ta_rad = ta_deg / 180 * Math.PI;
            this.g.strokeStyle = this.o.bgColor;
            this.g.arc(this.xy, this.xy, this.radius, -( ta_rad - delta_rad / 4) , -( ta_rad + delta_rad / 4 ), true); 
            this.g.stroke();
          }
          return false;
        }
      } );
    }
  /***********************************************************************************************/
  /* END COUNTER */
  /***********************************************************************************************/

  /***********************************************************************************************/
  /* HIDE FUCTIONS */
  /***********************************************************************************************/
  jQuery(window).scroll(function(){
    if(jQuery(document).scrollTop() > 200){
      jQuery('.mb_YTPBar').css({'display': 'none'});

    }
    else{
        jQuery('.mb_YTPBar').css({'display': 'block'});
      }
  });
  /***********************************************************************************************/
  /* END HIDE FUNCTIONS */
  /***********************************************************************************************/

/***********************************************************************************************/
  /* GO TO TOP BUTTON */
  /***********************************************************************************************/
  // Go to top button
      jQuery(window).load(function(){
         jQuery(window).scroll(function(){

            if(jQuery(document).scrollTop() > 300)
            {    
                jQuery('.goTop').css({bottom:"50px"});
            }
            else
            {  
               jQuery('.goTop').css({bottom:"-80px"});
            }
        }); 
        jQuery('#overlay').fadeOut();
      });
       
    jQuery('.goTop').on("click",function(){
        jQuery('html, body').animate({scrollTop:0}, 'slow');
        return false;
    }); 
  // End button top
  /***********************************************************************************************/
  /* END GO TO TOP BUTTON */
  /***********************************************************************************************/

  /***********************************************************************************************/
    /* JPLAYER */
    /***********************************************************************************************/
    //Toggle Playlist
    // jQuery('.jplayerButton').on('click', function(){

    //   jQuery(this).toggleClass('active');

    //   jQuery('.playlist-toggle').toggleClass('open');

    // });

    jQuery('.jplayerButton').on('click', function(){

      jQuery(this).toggleClass('active');

      jQuery('.playlist-wrapper').toggleClass('open');

    });

    // Open Close Player on scroll
    jQuery(".homeNormal").addClass("close-down");
    jQuery(window).on("scroll", function () {
    //      if (jQuery(this).scrollTop() > -1) {
    //          jQuery(".homeNormal").addClass("close-down");
    //          jQuery("#h-player").addClass("rotate");
    //      }
    //      else {
    //          jQuery(".homeNormal").removeClass("close-down");
    //          jQuery("#h-player").removeClass("rotate");
    //      }
    });
    jQuery(window).on("scroll", function () {
        if (jQuery(this).scrollTop() > 5500) {
            jQuery(".homeCustom").addClass("close-down");
            jQuery("#h-player").addClass("rotate");
        }
        else {
            jQuery(".homeCustom").removeClass("close-down");
            jQuery("#h-player").removeClass("rotate");
        }
    });
    // Open Close Player Button
    jQuery('#h-player').on('click', function() {
        jQuery(this).toggleClass("rotate")
        jQuery(".jplayer-home").toggleClass("close-down");
    });

    jQuery(window).on("scroll", function () {
        if (jQuery(this).scrollTop() > 5) {
            jQuery(".buttonBar").addClass("close-video");
        }
        else {
            jQuery(".buttonBar").removeClass("close-video");
        }
    });


    /***********************************************************************************************/
    /* END JPLAYER */
    /***********************************************************************************************/

  /***********************************************************************************************/
  /* START ISOTOPE */
  /***********************************************************************************************/
  function isotope() {

    var container = jQuery('.aqura-filter-content ul');

    container.imagesLoaded(function() {

     container.isotope();

    });

    container.isotope();

    var jQueryoptionSets = jQuery('.categories ul'),

    jQueryoptionLinks = jQueryoptionSets.find('a');

    jQueryoptionLinks.on("click", function(){

     var jQuerythis = jQuery(this);

     if ( jQuerythis.hasClass('selected') ) {

      return false;

     }
     var jQueryoptionSet = jQuerythis.parents('.categories ul');

     jQueryoptionSet.find('.selected').removeClass('selected');

     jQuerythis.addClass('selected');

     var options = {},

      key = jQueryoptionSet.attr('data-option-key'),

      value = jQuerythis.attr('data-option-value');

     value = value === 'false' ? false : value;

     options[ key ] = value;

     if ( key === 'layoutMode' && typeof changeLayoutMode === 'function' ) {

      changeLayoutMode( jQuerythis, options )

     } else {

      container.isotope( options );

     }

     return false;

    });

   };

   isotope();

   jQuery(window).resize(function(){

    isotope();

   });
  /***********************************************************************************************/
  /* END ISOTOPE */
  /***********************************************************************************************/

  /***********************************************************************************************/
  /* START CAROUSEL */
  /***********************************************************************************************/
  jQuery(".owl-carousel").owlCarousel({
    items:1,
    nav:true,
    navText: ['<i class="fa fa-chevron-left"></i>','<i class="fa fa-chevron-right"></i>']
    
  });
  /***********************************************************************************************/
  /* END CAROUSEL */
  /***********************************************************************************************/

  
  /***********************************************************************************************/
  /* INSTAGRAM */
  /***********************************************************************************************/
  var feedSidebar = new Instafeed({
        //get: 'tagged',
        //tagName: 'NichifyPerspectives', // place your tage here
        get: 'user',
        userId: 2143300160,
        sortBy: 'most-liked',
        clientId: 'b65a53a5cc0540769b7cf79ea333348c', // place the client id here
        template: '<li><a href="{{link}}" target="_blank"><img class="img-responsive" src="{{image}}" /></a></li>',
        target: 'instagram-sidebar-widget',
        limit: 6,
        resolution: 'low_resolution',
    });
    if (jQuery('#instagram-sidebar-widget').length>0) {
        feedSidebar.run();
    }
    /***********************************************************************************************/
    /* END INSTAGRAM */
    /***********************************************************************************************/
});
<!-- ================================================== -->
<!-- =============== END STARTER JS ================ -->
<!-- ================================================== -->
