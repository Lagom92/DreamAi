/*!
 * Start Bootstrap - Grayscale v6.0.3 (https://startbootstrap.com/theme/grayscale)
 * Copyright 2013-2020 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
 */
(function ($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
    if (
      location.pathname.replace(/^\//, "") ==
        this.pathname.replace(/^\//, "") &&
      location.hostname == this.hostname
    ) {
      var target = $(this.hash);
      target = target.length ? target : $("[name=" + this.hash.slice(1) + "]");
      if (target.length) {
        $("html, body").animate(
          {
            scrollTop: target.offset().top - 70,
          },
          1000,
          "easeInOutExpo"
        );
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $(".js-scroll-trigger").click(function () {
    $(".navbar-collapse").collapse("hide");
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $("body").scrollspy({
    target: "#mainNav",
    offset: 100,
  });

  // Collapse Navbar
  var navbarCollapse = function () {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  
  $(function () {
    $(".openModal").click(function () {
      setTimeout(function () {
        var h = $(".modal-body .first-content p").height();
        $(".modal-body").css("height", h + 80 + "px");
        $(".modal-body .first-content p").css("height", h + "px");
      }, 250);
    });
    $(".first-button").on("click", function () {
      $(".first-content").animate({ width: "toggle" }, function () {
        $(".second-content").animate({ width: "toggle" });
        var h = $(".modal-body .second-content p").height();
        $(".modal-body").css("height", h + 80 + "px");
        $(".modal-body .second-content p").css("height", h + "px");
      });
    });
    $(".second-button").on("click", function () {
      $(".second-content").animate({ width: "toggle" }, function () {
        $(".third-content").animate({ width: "toggle" });
        var h = $(".modal-body .third-content div").height();
        $(".modal-body").css("height", h + 80 + "px");
        $(".modal-body .third-content p").css("height", h + "px");
      });
    });
  });

  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict

// audio record js
