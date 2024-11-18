// Define the navbar HTML as a string
const headHTML = `
<meta charset="utf-8">
<title>MPS</title>
<meta content="width=device-width, initial-scale=1.0" name="viewport">
<meta content="" name="keywords">
<meta content="" name="description">

<!-- Google Web Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600;700&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet"> 

<!-- Icon Font Stylesheet -->
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.4/css/all.css"/>
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css" rel="stylesheet">

<!-- Libraries Stylesheet -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
<link href="lib/animate/animate.min.css" rel="stylesheet">
<link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">
<link href="lib/lightbox/css/lightbox.min.css" rel="stylesheet">


<!-- Customized Bootstrap Stylesheet -->
<link href="css/bootstrap.min.css" rel="stylesheet">

<!-- Template Stylesheet -->
<link href="css/style.css" rel="stylesheet">
`;
























// Define the topbar HTML as a string
const topbarHTML = `
<div class="container px-0">
    <div class="row gx-0 align-items-center" style="height: 45px;">
        <div class="col-lg-8 text-center text-lg-start mb-lg-0">
            <div class="d-flex flex-wrap">
                <a href="#" class="text-muted me-4"><i class="fas fa-phone-alt text-primary me-2"></i>+234 706 685 9293</a>
                <a href="#" class="text-muted me-0"><i class="fas fa-envelope text-primary me-2"></i>masudjiya@gmail.com</a>
            </div>
        </div>
        <div class="col-lg-4 text-center text-lg-end">
            <div class="d-flex align-items-center justify-content-end">
                <a href="#" class="btn btn-primary btn-square rounded-circle nav-fill me-3"><i class="fab fa-facebook-f text-white"></i></a>
                <a href="#" class="btn btn-primary btn-square rounded-circle nav-fill me-3"><i class="fab fa-twitter text-white"></i></a>
                <a href="#" class="btn btn-primary btn-square rounded-circle nav-fill me-3"><i class="fab fa-instagram text-white"></i></a>
                <a href="#" class="btn btn-primary btn-square rounded-circle nav-fill me-0"><i class="fab fa-linkedin-in text-white"></i></a>
            </div>
        </div>
    </div>
</div>
`;



















// Define the navbar HTML as a string
const navbarHTML = `
<div class="position-absolute bg-dark" style="left: 0; top: 0; width: 100%; height: 100%;">
</div>
<div class="container px-0">
    <nav class="navbar navbar-expand-lg navbar-dark bg-white py-3 px-4">
        <a href="index.html" class="navbar-brand p-0">
            <h1 class="text-primary m-0"><i class="fas fa-donate me-3"></i>MPS</h1>
            <!-- <img src="img/logo.png" alt="Logo"> -->
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="fa fa-bars"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <div class="navbar-nav ms-auto py-0">
                <a href="index.html" class="nav-item nav-link active">Home</a>
                <a href="about.html" class="nav-item nav-link">About</a>
                <a href="service.html" class="nav-item nav-link">Services</a>
                <a href="404.html" class="nav-item nav-link">Projects</a>
                <div class="nav-item dropdown">
                    <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">News</a>
                    <div class="dropdown-menu m-0">
                        <a href="blog.html" class="dropdown-item">Our Blog</a>
                        <a href="team.html" class="dropdown-item">Our Team</a>
                        <a href="testimonial.html" class="dropdown-item">Testimonial</a>
                        <a href="faqs.html" class="dropdown-item">FAQs</a>
                    </div>
                </div>
                <a href="contact.html" class="nav-item nav-link">Contact</a>
            </div>
            <div class="d-flex align-items-center flex-nowrap pt-xl-0">
                <button class="btn btn-primary btn-md-square mx-2" data-bs-toggle="modal" data-bs-target="#searchModal"><i class="fas fa-search"></i></button>
                <a href="../login/login.html" class="btn btn-primary rounded-pill text-white py-2 px-4 ms-2 flex-wrap flex-sm-shrink-0">Get Sarted</a>
            </div>
        </div>
    </nav>
</div>
`;



















// Define the footer HTML as a string
const footerHTML = `
<div class="container py-5">
    <div class="row g-5">
        <div class="col-md-6 col-lg-6 col-xl-3">
            <div class="footer-item d-flex flex-column">
                <div class="footer-item">
                    <h4 class="text-white mb-4">Newsletter</h4>
                    <p class="mb-3">Subscribe for our monthly newsletter and empower yoourself with financial knowledge.</p>
                    <div class="position-relative mx-auto rounded-pill">
                        <input class="form-control rounded-pill w-100 py-3 ps-4 pe-5" type="text" placeholder="Enter your email">
                        <button type="button" class="btn btn-primary rounded-pill position-absolute top-0 end-0 py-2 mt-2 me-2">SignUp</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-6 col-xl-3">
            <div class="footer-item d-flex flex-column">
                <h4 class="text-white mb-4">Explore</h4>
                <a href="#"><i class="fas fa-angle-right me-2"></i> Home</a>
                <a href="#"><i class="fas fa-angle-right me-2"></i> Services</a>
                <a href="#"><i class="fas fa-angle-right me-2"></i> About Us</a>
                <a href="#"><i class="fas fa-angle-right me-2"></i> Latest Projects</a>
                <a href="#"><i class="fas fa-angle-right me-2"></i> testimonial</a>
                <a href="#"><i class="fas fa-angle-right me-2"></i> Our Team</a>
                <a href="#"><i class="fas fa-angle-right me-2"></i> Contact Us</a>
            </div>
        </div>
        <div class="col-md-6 col-lg-6 col-xl-3">
            <div class="footer-item d-flex flex-column">
                <h4 class="text-white mb-4">Contact Info</h4>
                <a href=""><i class="fa fa-map-marker-alt me-2"></i> 123 Street, Kuje, Abuja</a>
                <a href=""><i class="fas fa-envelope me-2"></i> info@mps.com</a>
                <a href=""><i class="fas fa-phone me-2"></i> +234 706 685 9293</a>
                <div class="d-flex align-items-center">
                    <a class="btn btn-light btn-md-square me-2" href=""><i class="fab fa-facebook-f"></i></a>
                    <a class="btn btn-light btn-md-square me-2" href=""><i class="fab fa-twitter"></i></a>
                    <a class="btn btn-light btn-md-square me-2" href=""><i class="fab fa-instagram"></i></a>
                    <a class="btn btn-light btn-md-square me-0" href=""><i class="fab fa-linkedin-in"></i></a>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-6 col-xl-3">
            <div class="footer-item-post d-flex flex-column">
                <h4 class="text-white mb-4">Popular Post</h4>
                <div class="d-flex flex-column mb-3">
                    <p class="text-uppercase text-primary mb-2">Investment</p>
                    <a href="#" class="text-body">Revisiting Your Investment & Distribution Goals</a>
                </div>
                <div class="d-flex flex-column mb-3">
                    <p class="text-uppercase text-primary mb-2">Business</p>
                    <a href="#" class="text-body">Dimensional Fund Advisors Interview with Director</a>
                </div>
                <div class="footer-btn text-start">
                    <a href="blog.html" class="btn btn-light rounded-pill px-4">View All Post <i class="fa fa-arrow-right ms-1"></i></a>
                </div>
            </div>
        </div>
    </div>
</div>
`;











// Define the copyright HTML as a string
const copyrightHTML = `
<div class="container">
    <div class="row g-4 align-items-center">
        <div class="col-md-6 text-center text-md-start mb-md-0">
            <span class="text-body"><a href="https://mps.com" class="border-bottom text-primary"><i class="fas fa-copyright text-light me-2"></i>www.mps.com</a>, All right reserved.</span>
        </div>
        <div class="col-md-6 text-center text-md-end text-body">
            Designed By <a class="border-bottom text-primary" href="https://abudigitalinc.wordpress.com">ABUQATAADA DIGITAL INC.</a>
        </div>
    </div>
</div>
`;














// Inject components into the DOM
document.addEventListener("DOMContentLoaded", () => {
  // Inject the head
  const headContainer = document.getElementById("head");
  if (headContainer) headContainer.innerHTML = headHTML;

  // Inject the topbar
  const topbarContainer = document.getElementById("topbar");
  if (topbarContainer) topbarContainer.innerHTML = topbarHTML;

  // Inject the navbar
  const navbarContainer = document.getElementById("navbar");
  if (navbarContainer) navbarContainer.innerHTML = navbarHTML;

  // Inject the footer
  const footerContainer = document.getElementById("footer");
  if (footerContainer) footerContainer.innerHTML = footerHTML;

  // Inject the copyright
  const copyrightContainer = document.getElementById("copyright");
  if (copyrightContainer) copyrightContainer.innerHTML = copyrightHTML;
});

























































(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(window).width() > 992) {
            if ($(this).scrollTop() > 45) {
                $('.sticky-top .container').addClass('shadow-sm').css('max-width', '100%');
            } else {
                $('.sticky-top .container').removeClass('shadow-sm').css('max-width', $('.topbar .container').width());
            }
        } else {
            $('.sticky-top .container').addClass('shadow-sm').css('max-width', '100%');
        }
    });


    // Hero Header carousel
    $(".header-carousel").owlCarousel({
        items: 1,
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: false,
        loop: true,
        margin: 0,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ]
    });



    // Project carousel
    $(".project-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : false,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:2
            },
            1200:{
                items:2
            }
        }
    });

    // testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : false,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:2
            },
            1200:{
                items:2
            }
        }
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 5,
        time: 2000
    });


    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


})(jQuery);

