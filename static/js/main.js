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
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
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


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    
})(jQuery);// Function to toggle cart visibility
function toggleCart() {
    const cart = document.getElementById('shoppingCart');
    cart.classList.toggle('active');
}

// Function to add items to the cart
function addToCart(name, price) {
    const cartItems = document.getElementById('cartItems');
    
    // Check if the item already exists in the cart
    const existingItem = document.querySelector(`.cart-item[data-name="${name}"]`);
    if (existingItem) {
        const quantityElement = existingItem.querySelector('.quantity span');
        const newQuantity = parseInt(quantityElement.textContent) + 1;
        quantityElement.textContent = newQuantity;
    } else {
        // Create a new cart item element
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.setAttribute('data-name', name);
        cartItem.innerHTML = `
            <p>${name}</p>
            <p>${price}</p>
            <div class="quantity">
                <button onclick="updateQuantity(this, -1)">-</button>
                <span>1</span>
                <button onclick="updateQuantity(this, 1)">+</button>
            </div>
        `;
        cartItems.appendChild(cartItem);
    }
    saveCart();
}

// Function to update item quantity
function updateQuantity(button, amount) {
    const quantityElement = button.parentElement.querySelector('span');
    let currentQuantity = parseInt(quantityElement.textContent);
    currentQuantity += amount;
    if (currentQuantity < 1) {
        // Remove the cart item if quantity is 0
        const cartItem = button.closest('.cart-item');
        cartItem.remove();
    } else {
        quantityElement.textContent = currentQuantity;
    }
    saveCart();
}

// Function to save cart state to local storage
function saveCart() {
    const cartItems = document.querySelectorAll('.cart-item');
    const cartData = [];

    cartItems.forEach(item => {
        const name = item.getAttribute('data-name');
        const price = item.querySelector('p:nth-child(2)').textContent;
        const quantity = item.querySelector('.quantity span').textContent;
        cartData.push({ name, price, quantity });
    });

    localStorage.setItem('cart', JSON.stringify(cartData));
}

// Function to load cart state from local storage
function loadCart() {
    const cartData = JSON.parse(localStorage.getItem('cart'));
    if (cartData) {
        const cartItems = document.getElementById('cartItems');
        cartItems.innerHTML = ''; // Clear existing items

        cartData.forEach(item => {
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.setAttribute('data-name', item.name);
            cartItem.innerHTML = `
                <p>${item.name}</p>
                <p>${item.price}</p>
                <div class="quantity">
                    <button onclick="updateQuantity(this, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button onclick="updateQuantity(this, 1)">+</button>
                </div>
            `;
            cartItems.appendChild(cartItem);
        });
    }
}

// Event listener for add-to-cart buttons
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        const name = this.getAttribute('data-name');
        const price = this.getAttribute('data-price');
        addToCart(name, price);
    });
});

// Load cart when the page loads
window.onload = loadCart;
