document.querySelector('.hamburger').addEventListener('click', function () {
    this.classList.toggle('active');
    const navMenu = document.querySelector('.nav ul');
    navMenu.classList.toggle('show');
    
    // If menu is closing, close all open submenus
    if (!navMenu.classList.contains('show')) {
        document.querySelectorAll('.nav ul li').forEach(item => item.classList.remove('show'));
    }
});

// Handle submenu toggling
document.querySelectorAll('.nav ul li a').forEach(link => {
    link.addEventListener('click', function (e) {
        const submenu = this.nextElementSibling;

        // Check if there is a submenu
        if (submenu && submenu.classList.contains('submenu')) {
            e.preventDefault(); // Prevent default link behavior

            const parentLi = this.parentElement;
            const isSubmenuOpen = parentLi.classList.contains('show');

            // Toggle the current submenu
            if (isSubmenuOpen) {
                parentLi.classList.remove('show');
            } else {
                // Close all submenus
                document.querySelectorAll('.nav ul li').forEach(item => item.classList.remove('show'));

                // Open the current submenu
                parentLi.classList.add('show');
            }
        }
    });
});
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    header.classList.toggle('scrolled', window.scrollY > 50);
});
