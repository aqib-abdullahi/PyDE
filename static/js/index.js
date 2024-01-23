const closeDropDown = document.getElementById("menuButton2")
const dropDownButton = document.querySelector(".menu-button")
const dropContent = document.querySelector(".ul-link")
const aboutSection = document.querySelector(".about");

dropDownButton.addEventListener("click", function() {
    console.log("clicked")
    dropContent.classList.add('show')
})

closeDropDown.addEventListener("click", function() {
    console.log("clicked")
    dropContent.classList.remove('show')
})

document.addEventListener("DOMContentLoaded", function() {
    const nav = document.querySelector(".nav")
    let aboutSectionOffset = aboutSection.offsetTop;

    document.getElementById('aboutlink').addEventListener('click', function(e) {
        function scrollToAboutSection() {
            window.scrollTo({
                top: aboutSectionOffset - nav.offsetHeight,
                behavior: "smooth"
            });
        }
        scrollToAboutSection();
    });

    document.getElementById('aboutlink2').addEventListener('click', function(e) {
        if (dropContent.classList.contains('show')) {
            dropContent.classList.remove('show')
            let aboutSectionOffset = aboutSection.offsetTop;

            function scrollToAboutSection() {
                window.scrollTo({
                    top: aboutSectionOffset - nav.offsetHeight,
                    behavior: "smooth"
                });
            }
            scrollToAboutSection();
        }
    });
});