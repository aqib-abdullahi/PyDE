const treeRootElements = document.querySelectorAll("ul.treeRoot li span");

treeRootElements.forEach(function(element) {
    element.addEventListener("click", function() {
        if (this.parentElement.classList.contains("hasSubMenu")) {
            const ul = this.parentElement.querySelector("ul");
            if (ul.classList.contains("activeSubMenu")) {
                ul.classList.remove("activeSubMenu");
            } else {
                ul.classList.add("activeSubMenu");
            }
        }

    });

    const isFile = element.parentElement.classList.contains("file");
    const iconClass = isFile ? "fa-regular fa-file" : "fa-regular fa-folder-open";
    const iconClasses = iconClass.split(' ');
    const iconElement = document.createElement("i");
    iconClasses.forEach(cls => {
        iconElement.classList.add(cls);
    });
    element.parentNode.insertBefore(iconElement, element);
    // element.parentNode.appendChild(iconElement, element)
    if (iconClass === 'fa-regular fa-folder-open') {
        const originalIconClass = "fa-solid fa-file-circle-plus";
        // file icon class
        const iconclass = originalIconClass.split(' ');
        // add file element
        const iconelement = document.createElement("i");
        iconclass.forEach(cls => {
            iconelement.classList.add(cls);
        });
        // add folder class
        const Addfolderclass = "fa-solid fa-folder-plus";
        const seperatedFolderClass = Addfolderclass.split(' ')
            // add foldeer element
        const folderElement = document.createElement("i")
        seperatedFolderClass.forEach(cls => {
            folderElement.classList.add(cls);
        });
        // inserts file icon
        element.parentNode.insertBefore(iconelement, element.nextSibling);
        // inserts folder icon
        element.parentNode.insertBefore(folderElement, element.nextSibling);
    }

});