const treeRootElements = document.querySelectorAll("ul.treeRoot li span");
const cancelfolder = document.getElementById('cancelfolder-btn');
const cancelfile = document.getElementById('cancelfile-btn');
const popupfile = document.querySelector('.popfile');
const popupfolder = document.querySelector('.popfolder');
const folderNameInput = document.getElementById('folderNameInput');
const folderName = folderNameInput.value;
const folderForm = document.querySelector('.folderForm');
const fileForm = document.querySelector('.fileForm');
const popfoldersmoke = document.querySelector('.popfoldersmoke');
const popfilesmoke = document.querySelector('.popfilesmoke');
const userId = document.getElementById('userId').value;
let parentFolder;

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
            popupfile.style.display = 'none';
            popupfolder.style.display = 'grid';
            popfoldersmoke.style.display = 'block';
            // test
            parentFolder = this.parentElement.innerText
            console.log(parentFolder);
        })
        iconelement.addEventListener('click', function() {
            popupfolder.style.display = 'none';
            popupfile.style.display = 'grid';
            popfilesmoke.style.display = 'block';
            parentFolder = this.parentElement.innerText
            console.log(parentFolder);
        })
    }

});

cancelfile.addEventListener('click', function() {
    popupfile.style.display = 'none';
    popfilesmoke.style.display = 'none';
})

cancelfolder.addEventListener('click', function() {
    popupfolder.style.display = 'none';
    popfoldersmoke.style.display = 'none';
})

popfoldersmoke.addEventListener('click', function() {
    popfoldersmoke.style.display = 'none';
    popupfolder.style.display = 'none';
})

popfilesmoke.addEventListener('click', function() {
    popfilesmoke.style.display = 'none';
    popupfile.style.display = 'none';
})

// SAVE FILE (file upload to DB)
fileForm.addEventListener("submit", function(event) {
    event.preventDefault();
    popupfile.style.display = 'none';
    popupfolder.style.display = 'none';
    popfoldersmoke.style.display = 'none';
    popfilesmoke.style.display = 'none'
    const fileNameInput = document.getElementById('fileNameInput');
    const fileName = fileNameInput.value;
    fileInfo = {
        "file_name": fileName,
        "parent_folder": parentFolder
    }

    fetch(`/api/v1/users/${userId}/files`, {
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

// LOAD  USER FILES FROM DB
const userFiles = fetch(`/api/v1/users/${userId}/files`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Files loaded successsfully: ', data);
    })
    .catch(error => {
        console.error('Problem loading files: ', error);
    })
console.log(userFiles)