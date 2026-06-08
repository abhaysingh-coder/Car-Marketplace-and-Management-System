/* ==========================================
   AutoDrive - Main JavaScript
========================================== */

(() => {
    "use strict";

    const $ = (selector, parent = document) =>
        parent.querySelector(selector);

    const $$ = (selector, parent = document) =>
        [...parent.querySelectorAll(selector)];

    /* ==========================
       Mobile Navigation
    ========================== */

    window.toggleMenu = function () {
        const navLinks = $("#navLinks");

        if (navLinks) {
            navLinks.classList.toggle("active");
        }
    };

    function closeMenuOnLinkClick() {
        const navLinks = $("#navLinks");

        if (!navLinks) return;

        $$("#navLinks a").forEach(link => {
            link.addEventListener("click", () => {
                navLinks.classList.remove("active");
            });
        });
    }

    /* ==========================
       Active Navigation Link
    ========================== */

    function setActiveNavLink() {

        const currentPath =
            window.location.pathname.toLowerCase();

        $$("#navLinks a").forEach(link => {

            const linkPath =
                new URL(link.href, window.location.origin)
                    .pathname
                    .toLowerCase();

            if (linkPath === currentPath) {
                link.classList.add("active");
            }
        });
    }

    /* ==========================
       Hero Slider
    ========================== */

    function initHeroSlider() {

        const slides = $$(".slide");

        if (!slides.length) return;

        let index = 0;

        function showSlide(nextIndex) {

            slides[index].classList.remove("active");

            index =
                (nextIndex + slides.length) %
                slides.length;

            slides[index].classList.add("active");
        }

        slides.forEach(slide =>
            slide.classList.remove("active")
        );

        slides[0].classList.add("active");

        window.nextSlide = () => {
            showSlide(index + 1);
        };

        window.prevSlide = () => {
            showSlide(index - 1);
        };

        setInterval(() => {
            showSlide(index + 1);
        }, 5000);
    }

    /* ==========================
       Bootstrap Carousels
    ========================== */

    function initCarousels() {

        const carousels = [
            "#sellHeroCarousel",
            "#sellCarousel",
            "#serviceCarousel"
        ];

        carousels.forEach(id => {

            const element =
                document.querySelector(id);

            if (
                element &&
                typeof bootstrap !== "undefined"
            ) {
                new bootstrap.Carousel(element, {
                    interval: 3000,
                    ride: "carousel",
                    pause: "hover",
                    wrap: true
                });
            }
        });
    }

    /* ==========================
       Reveal Animation
    ========================== */

    function initRevealAnimation() {

        const revealItems =
            document.querySelectorAll(".reveal");

        if (!revealItems.length) return;

        const observer =
            new IntersectionObserver(
                entries => {

                    entries.forEach(entry => {

                        if (
                            entry.isIntersecting
                        ) {

                            entry.target.classList.add(
                                "active"
                            );

                            observer.unobserve(
                                entry.target
                            );
                        }
                    });
                },
                {
                    threshold: 0.15
                }
            );

        revealItems.forEach(item => {
            observer.observe(item);
        });
    }

    /* ==========================
       Back To Top Button
    ========================== */

    function initBackToTop() {

        const button =
            document.createElement("button");

        button.className = "top-btn";

        button.innerHTML =
            '<i class="fa-solid fa-arrow-up"></i>';

        document.body.appendChild(button);

        window.addEventListener(
            "scroll",
            () => {

                if (
                    window.scrollY > 400
                ) {
                    button.classList.add(
                        "show"
                    );
                } else {
                    button.classList.remove(
                        "show"
                    );
                }
            }
        );

        button.addEventListener(
            "click",
            () => {

                window.scrollTo({
                    top: 0,
                    behavior: "smooth"
                });
            }
        );
    }

    /* ==========================
       Animated Counter
    ========================== */

    function initCounters() {

        const counters =
            document.querySelectorAll(
                ".stat-box h2, .why-grid h3"
            );

        if (!counters.length) return;

        const animateCounter =
            counter => {

                const text =
                    counter.textContent.trim();

                const target =
                    parseInt(
                        text.replace(/\D/g, "")
                    );

                if (!target) return;

                const suffix =
                    text.replace(/[0-9]/g, "");

                let current = 0;

                const step =
                    Math.ceil(target / 80);

                function update() {

                    current += step;

                    if (
                        current >= target
                    ) {

                        counter.textContent =
                            text;

                        return;
                    }

                    counter.textContent =
                        current + suffix;

                    requestAnimationFrame(
                        update
                    );
                }

                update();
            };

        const observer =
            new IntersectionObserver(
                entries => {

                    entries.forEach(entry => {

                        if (
                            entry.isIntersecting
                        ) {

                            animateCounter(
                                entry.target
                            );

                            observer.unobserve(
                                entry.target
                            );
                        }
                    });
                },
                {
                    threshold: 0.4
                }
            );

        counters.forEach(counter => {
            observer.observe(counter);
        });
    }

    /* ==========================
       Service Page Gallery
    ========================== */

    function initServiceGallery() {

        const thumbs =
            document.querySelectorAll(
                ".thumb"
            );

        const mainImage =
            document.getElementById(
                "mainServiceImage"
            );

        const serviceTitle =
            document.getElementById(
                "serviceTitle"
            );

        const serviceText =
            document.getElementById(
                "serviceText"
            );

        if (
            !thumbs.length ||
            !mainImage
        ) {
            return;
        }

        thumbs.forEach(thumb => {

            thumb.addEventListener(
                "click",
                () => {

                    thumbs.forEach(item =>
                        item.classList.remove(
                            "active"
                        )
                    );

                    thumb.classList.add(
                        "active"
                    );

                    mainImage.style.opacity =
                        "0";

                    setTimeout(() => {

                        mainImage.src =
                            thumb.dataset.image;

                        if (
                            serviceTitle
                        ) {
                            serviceTitle.textContent =
                                thumb.dataset.title;
                        }

                        if (
                            serviceText
                        ) {
                            serviceText.textContent =
                                thumb.dataset.text;
                        }

                        mainImage.style.opacity =
                            "1";

                    }, 250);
                }
            );
        });
    }

    /* ==========================
       Prevent Double Submit
    ========================== */

    function preventDoubleSubmit() {

        document
            .querySelectorAll(
                'form[method="post"], form[method="POST"]'
            )
            .forEach(form => {

                form.addEventListener(
                    "submit",
                    () => {

                        const btn =
                            form.querySelector(
                                'button[type="submit"]'
                            );

                        if (!btn) return;

                        btn.disabled = true;

                        btn.innerHTML =
                            '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
                    }
                );
            });
    }

    /* ==========================
       History Tabs
    ========================== */

    window.openHistoryTab =
        function (event, tabName) {

            document
                .querySelectorAll(
                    ".history-tab-content"
                )
                .forEach(tab => {
                    tab.classList.remove(
                        "active"
                    );
                });

            document
                .querySelectorAll(
                    ".history-tab-btn"
                )
                .forEach(btn => {
                    btn.classList.remove(
                        "active"
                    );
                });

            const selected =
                document.getElementById(
                    tabName
                );

            if (selected) {
                selected.classList.add(
                    "active"
                );
            }

            if (
                event &&
                event.currentTarget
            ) {
                event.currentTarget.classList.add(
                    "active"
                );
            }
        };

    /* ==========================
       Initialize
    ========================== */

    document.addEventListener(
        "DOMContentLoaded",
        () => {

            closeMenuOnLinkClick();
            setActiveNavLink();

            initHeroSlider();
            initCarousels();

            initRevealAnimation();
            initBackToTop();
            initCounters();

            initServiceGallery();
            preventDoubleSubmit();
        }
    );

})();

document.addEventListener("DOMContentLoaded", function () {
    const sellHero = document.querySelector("#sellHeroCarousel");

    if (sellHero && typeof bootstrap !== "undefined") {
        new bootstrap.Carousel(sellHero, {
            interval: 3000,
            ride: "carousel",
            pause: "hover",
            wrap: true
        });
    }

    const items = document.querySelectorAll(".sell-reveal");

    function revealSellingItems() {
        items.forEach(function (item) {
            if (item.getBoundingClientRect().top < window.innerHeight - 100) {
                item.classList.add("active");
            }
        });
    }

    window.addEventListener("scroll", revealSellingItems);
    revealSellingItems();
});

function openHistoryTab(event, tabName) {
    document.querySelectorAll(".history-tab-content").forEach(tab => {
        tab.classList.remove("active");
    });

    document.querySelectorAll(".history-tab-btn").forEach(btn => {
        btn.classList.remove("active");
    });

    document.getElementById(tabName).classList.add("active");
    event.currentTarget.classList.add("active");
}

function openTab(tabName, event) {
    let contents = document.querySelectorAll('.tab-content');
    let buttons = document.querySelectorAll('.tab-btn');

    contents.forEach(content => {
        content.classList.remove('active');
    });

    buttons.forEach(button => {
        button.classList.remove('active');
    });

    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}