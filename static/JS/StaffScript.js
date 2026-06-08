const menuBtn = document.getElementById("menuBtn");
const staffSidebar = document.getElementById("staffSidebar");

if (menuBtn && staffSidebar) {
    menuBtn.addEventListener("click", () => {
        staffSidebar.classList.toggle("active");
    });
}

document.addEventListener("click", (event) => {
    if (!staffSidebar || !menuBtn) return;

    const clickedInsideSidebar = staffSidebar.contains(event.target);
    const clickedMenuButton = menuBtn.contains(event.target);

    if (!clickedInsideSidebar && !clickedMenuButton && window.innerWidth <= 900) {
        staffSidebar.classList.remove("active");
    }
});

const currentPath = window.location.pathname;
const sidebarLinks = document.querySelectorAll(".sidebar-nav a");

sidebarLinks.forEach(link => {
    if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
    }
});

function openTab(event, tabId){
    const contents = document.querySelectorAll(".tab-content");
    const buttons = document.querySelectorAll(".tab-btn");

    contents.forEach(content => {
        content.classList.remove("active");
    });

    buttons.forEach(button => {
        button.classList.remove("active");
    });

    document.getElementById(tabId).classList.add("active");
    event.currentTarget.classList.add("active");
}