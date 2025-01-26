(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(() => {
            $('#spinner').length > 0 && $('#spinner').removeClass('show');
        }, 1);
    };
    spinner();

    // Initiate the wowjs
    new WOW().init();

    // Sticky Navbar
    $(window).scroll(function () {
        $(this).scrollTop() > 45
            ? $('.navbar').addClass('sticky-top shadow-sm')
            : $('.navbar').removeClass('sticky-top shadow-sm');
    });

    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const showClass = "show";

    $(window).on("load resize", function () {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
                function () {
                    $(this).addClass(showClass)
                        .find(".dropdown-toggle").attr("aria-expanded", "true")
                        .end().find(".dropdown-menu").addClass(showClass);
                },
                function () {
                    $(this).removeClass(showClass)
                        .find(".dropdown-toggle").attr("aria-expanded", "false")
                        .end().find(".dropdown-menu").removeClass(showClass);
                }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });

    // Back to top button
    $(window).scroll(function () {
        $(this).scrollTop() > 300
            ? $('.back-to-top').fadeIn('slow')
            : $('.back-to-top').fadeOut('slow');
    });
    $('.back-to-top').click(() => $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo'));

    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({ delay: 10, time: 2000 });

    // Modal Video
    $(document).ready(function () {
        let $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });

        $('#videoModal').on('shown.bs.modal', () => {
            $("#video").attr('src', `${$videoSrc}?autoplay=1&modestbranding=1&showinfo=0`);
        }).on('hide.bs.modal', () => {
            $("#video").attr('src', $videoSrc);
        });
    });

    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav: false,
        responsive: {
            0: { items: 1 },
            768: { items: 2 },
            992: { items: 3 }
        }
    });
})(jQuery);

// Toggle cart visibility
function toggleCart() {
    document.getElementById('shoppingCart')?.classList.toggle('active');
}

function createCartItem({ name, price, quantity }) {
    const cartItem = document.createElement('div');
    cartItem.classList.add('cart-item');
    cartItem.setAttribute('data-name', name);

    const nameElement = document.createElement('p');
    nameElement.textContent = name;

    const priceElement = document.createElement('p');
    priceElement.textContent = price;

    const quantityContainer = document.createElement('div');
    quantityContainer.classList.add('quantity');

    const decrementButton = document.createElement('button');
    decrementButton.textContent = '-';
    decrementButton.addEventListener('click', () => updateQuantity(decrementButton, -1));

    const quantityElement = document.createElement('span');
    quantityElement.textContent = quantity;

    const incrementButton = document.createElement('button');
    incrementButton.textContent = '+';
    incrementButton.addEventListener('click', () => updateQuantity(incrementButton, 1));

    quantityContainer.append(decrementButton, quantityElement, incrementButton);
    cartItem.append(nameElement, priceElement, quantityContainer);

    return cartItem;
}


document.addEventListener('DOMContentLoaded', function () {
    // Attach event listeners to "Add to Cart" buttons
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function () {
            const itemName = this.getAttribute('data-name');
            const itemPrice = this.getAttribute('data-price');
            addToCart(itemName, parseFloat(itemPrice));
        });
    });

    loadCart();
});

function addToCart(name, price) {
    const cartItems = document.getElementById('cartItems');
    const existingItem = document.querySelector(`.cart-item[data-name="${name}"]`);

    if (existingItem) {
        const quantityElement = existingItem.querySelector('.quantity span');
        quantityElement.textContent = parseInt(quantityElement.textContent) + 1;
    } else {
        const cartItem = createCartItem({ name, price, quantity: 1 });
        cartItems.appendChild(cartItem);
    }
    saveCart();
}


// Update item quantity
function updateQuantity(button, amount) {
    const quantityElement = button.parentElement.querySelector('span');
    let currentQuantity = parseInt(quantityElement.textContent);
    currentQuantity += amount;

    if (currentQuantity < 1) {
        button.closest('.cart-item').remove();
    } else {
        quantityElement.textContent = currentQuantity;
    }
    saveCart();
}

document.addEventListener('DOMContentLoaded', function () {
    loadCart();

    document.querySelector('.cart-items').addEventListener('click', function (event) {
        if (event.target.matches('.decrement-button')) {
            updateQuantity(event.target, -1);
        } else if (event.target.matches('.increment-button')) {
            updateQuantity(event.target, 1);
        }
    });
});

// Save cart state to local storage
function saveCart() {
    const cartItems = Array.from(document.querySelectorAll('.cart-item')).map(item => ({
        name: item.getAttribute('data-name'),
        price: parseFloat(item.querySelector('p:nth-child(2)').textContent),
        quantity: parseInt(item.querySelector('.quantity span').textContent)
    }));

    localStorage.setItem('cart', JSON.stringify(cartItems));
}

// Load cart state from local storage
function loadCart() {
    const cartData = JSON.parse(localStorage.getItem('cart')) || [];
    const cartItems = document.getElementById('cartItems');
    cartItems.innerHTML = '';

    cartData.forEach(item => cartItems.appendChild(createCartItem(item)));
}

// Pass cart data to checkout
function proceedToCheckout() {
    const cartData = JSON.parse(localStorage.getItem('cart')) || [];
    if (!cartData.length) return alert("Your cart is empty!");

    fetch('/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cartData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Checkout successful!");
            window.location.href = '/menu';
        } else {
            alert("Checkout failed!");
        }
    })
    .catch(error => console.error('Error during checkout:', error));
}


// Attach event to checkout button
document.querySelector('.checkout-btn')?.addEventListener('click', proceedToCheckout);

// Load the cart on page load
document.addEventListener('DOMContentLoaded', loadCart);
