
/* =========================================================
   EVENTHUB
   MAIN JAVASCRIPT
========================================================= */


/* =========================================================
   THEME
========================================================= */

function toggleTheme() {

    document.body.classList.toggle("light-mode");

    const isLight =
        document.body.classList.contains("light-mode");

    localStorage.setItem(
        "eventhub-theme",
        isLight ? "light" : "dark"
    );

    updateThemeIcon();
}


/* =========================================================
   UPDATE THEME ICON
========================================================= */

function updateThemeIcon() {

    const icon =
        document.getElementById("themeIcon");

    if (!icon) {
        return;
    }

    const isLight =
        document.body.classList.contains("light-mode");

    icon.textContent =
        isLight ? "☾" : "☀";
}


/* =========================================================
   LOAD SAVED THEME
========================================================= */

function loadTheme() {

    const savedTheme =
        localStorage.getItem("eventhub-theme");

    if (savedTheme === "light") {

        document.body.classList.add(
            "light-mode"
        );

    } else {

        document.body.classList.remove(
            "light-mode"
        );
    }

    updateThemeIcon();
}


/* =========================================================
   MOBILE MENU
========================================================= */

function toggleMobileMenu() {

    const nav =
        document.getElementById("navLinks");

    const button =
        document.getElementById(
            "mobileMenuButton"
        );

    if (!nav) {
        return;
    }

    nav.classList.toggle("open");

    if (button) {

        const isOpen =
            nav.classList.contains("open");

        button.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );
    }
}


/* =========================================================
   CLOSE MOBILE MENU
========================================================= */

function closeMobileMenu() {

    const nav =
        document.getElementById("navLinks");

    const button =
        document.getElementById(
            "mobileMenuButton"
        );

    if (!nav) {
        return;
    }

    nav.classList.remove("open");

    if (button) {

        button.setAttribute(
            "aria-expanded",
            "false"
        );
    }
}


/* =========================================================
   ACTIVE NAVIGATION
========================================================= */

function setActiveNavigation() {

    const currentPath =
        window.location.pathname;

    const links =
        document.querySelectorAll(
            ".nav-links a"
        );

    links.forEach(function (link) {

        const href =
            link.getAttribute("href");

        if (!href) {
            return;
        }

        link.classList.remove("active");

        try {

            const url =
                new URL(
                    href,
                    window.location.origin
                );

            const linkPath =
                url.pathname;

            if (
                linkPath === "/" &&
                currentPath === "/"
            ) {

                link.classList.add("active");

            } else if (
                linkPath !== "/" &&
                currentPath.startsWith(
                    linkPath
                )
            ) {

                link.classList.add("active");
            }

        } catch (error) {

            console.warn(
                "Navigation error:",
                error
            );
        }

    });
}


/* =========================================================
   CLOSE MENU WHEN CLICKING OUTSIDE
========================================================= */

document.addEventListener(
    "click",
    function (event) {

        const nav =
            document.getElementById(
                "navLinks"
            );

        const button =
            document.getElementById(
                "mobileMenuButton"
            );

        if (!nav || !button) {
            return;
        }

        if (
            nav.classList.contains("open") &&
            !nav.contains(event.target) &&
            !button.contains(event.target)
        ) {

            closeMobileMenu();
        }
    }
);


/* =========================================================
   CLOSE MENU AFTER LINK CLICK
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const links =
            document.querySelectorAll(
                ".nav-links a"
            );

        links.forEach(function (link) {

            link.addEventListener(
                "click",
                closeMobileMenu
            );

        });

    }
);


/* =========================================================
   ESCAPE KEY
========================================================= */

document.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Escape") {

            closeMobileMenu();
        }

    }
);


/* =========================================================
   CLOSE MOBILE MENU ON RESIZE
========================================================= */

window.addEventListener(
    "resize",
    function () {

        if (window.innerWidth > 850) {

            closeMobileMenu();
        }

    }
);


/* =========================================================
   REGISTRATION MESSAGE
========================================================= */

function showRegistrationMessage() {

    alert(
        "تم اختيار الحجز بنجاح ✨\n\n" +
        "سيتم تطوير نظام الحجز في الخطوة القادمة."
    );
}


/* =========================================================
   PRODUCT MESSAGE
========================================================= */

function showProductMessage() {

    alert(
        "تم اختيار المنتج ✨\n\n" +
        "سيتم تطوير نظام الطلب والدفع في الخطوة القادمة."
    );
}


/* =========================================================
   SMOOTH SCROLL
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const anchors =
            document.querySelectorAll(
                'a[href^="#"]'
            );

        anchors.forEach(function (anchor) {

            anchor.addEventListener(
                "click",
                function (event) {

                    const targetId =
                        this.getAttribute("href");

                    if (
                        !targetId ||
                        targetId === "#"
                    ) {
                        return;
                    }

                    const target =
                        document.querySelector(
                            targetId
                        );

                    if (!target) {
                        return;
                    }

                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }
            );

        });

    }
);


/* =========================================================
   PAGE LOAD
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadTheme();

        setActiveNavigation();

    }
);

