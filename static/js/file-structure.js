const treeRootElements = document.querySelectorAll("ul.treeRoot li span");
const cancelfolder = document.getElementById('cancelfolder-btn');
const cancelfile = document.getElementById('cancelfile-btn');
const popupfile = document.querySelector('.popfile');
const popupfolder = document.querySelector('.popfolder');
const folderNameInput = document.getElementById('folderNameInput');
// const fileNameInput = document.getElementById('fileNameInput');
const folderName = folderNameInput.value;
// const fileName = fileNameInput.value;
const folderForm = document.querySelector('.folderForm');
const fileForm = document.querySelector('.fileForm');

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
    // test
    // iconElement.addEventListener('click', function() {
    //     console.log('i clicked it')
    // })
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
        folderElement.addEventListener('click', function() {
            popupfolder.style.display = 'grid';
            console.log('clicked')
        })
        iconelement.addEventListener('click', function() {
            console.log('clicked')
            popupfile.style.display = 'grid';
        })
    }

});

cancelfile.addEventListener('click', function() {
    popupfile.style.display = 'none';
})

cancelfolder.addEventListener('click', function() {
    popupfolder.style.display = 'none';
})



// SAVE FILE
function uploadFile(event) {
    event.preventDefault();


}

fileForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const fileNameInput = document.getElementById('fileNameInput');
    const fileName = fileNameInput.value;

    fileInfo = {
        "file_name": fileName,
        "parent_folder": "Python"
    }

    fetch('/api/v1/users/1/files', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(fileInfo)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('File uploaded successsfully: ', data);
        })
        .catch(error => {
            console.error('Problem uploading file: ', error);
        })
})