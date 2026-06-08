const menuBtn = document.getElementById("menuBtn");
const adminSidebar = document.getElementById("adminSidebar");

if (menuBtn && adminSidebar) {
    menuBtn.addEventListener("click", () => {
        adminSidebar.classList.toggle("active");
    });
}

document.addEventListener("click", (event) => {
    if (!adminSidebar || !menuBtn) return;

    const clickedInsideSidebar = adminSidebar.contains(event.target);
    const clickedMenuButton = menuBtn.contains(event.target);

    if (!clickedInsideSidebar && !clickedMenuButton && window.innerWidth <= 900) {
        adminSidebar.classList.remove("active");
    }
});

const currentPath = window.location.pathname;
const sidebarLinks = document.querySelectorAll(".sidebar-nav a");

sidebarLinks.forEach(link => {
    if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
    }
})
const menuBtn = document.getElementById("menuBtn");
const adminSidebar = document.getElementById("adminSidebar");

if (menuBtn && adminSidebar) {
    menuBtn.addEventListener("click", () => {
        adminSidebar.classList.toggle("active");
    });
}

document.addEventListener("click", (event) => {
    if (!adminSidebar || !menuBtn) return;

    const clickedInsideSidebar = adminSidebar.contains(event.target);
    const clickedMenuButton = menuBtn.contains(event.target);

    if (!clickedInsideSidebar && !clickedMenuButton && window.innerWidth <= 900) {
        adminSidebar.classList.remove("active");
    }
});

const currentPath = window.location.pathname;
const sidebarLinks = document.querySelectorAll(".sidebar-nav a");

sidebarLinks.forEach(link => {
    if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
    }
});

const menuBtn = document.getElementById("menuBtn");
const adminSidebar = document.getElementById("adminSidebar");

if (menuBtn && adminSidebar) {
    menuBtn.addEventListener("click", () => {
        adminSidebar.classList.toggle("active");
    });
}

document.addEventListener("click", (event) => {
    if (!adminSidebar || !menuBtn) return;

    const clickedInsideSidebar = adminSidebar.contains(event.target);
    const clickedMenuButton = menuBtn.contains(event.target);

    if (!clickedInsideSidebar && !clickedMenuButton && window.innerWidth <= 900) {
        adminSidebar.classList.remove("active");
    }
});

const currentPath = window.location.pathname;
const sidebarLinks = document.querySelectorAll(".sidebar-nav a");

sidebarLinks.forEach(link => {
    if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
    }
});