import { editor } from "./IDE.js";

const treeRootElements = document.querySelectorAll("ul.treeRoot li span");
const cancelfolder = document.getElementById('cancelfolder-btn');
const spans = document.querySelectorAll('.spanned')
const cancelfile = document.getElementById('cancelfile-btn');
const popupfile = document.querySelector('.popfile');
const popupfolder = document.querySelector('.popfolder');
const folderForm = document.querySelector('.folderForm');
const fileForm = document.querySelector('.fileForm');
const popfoldersmoke = document.querySelector('.popfoldersmoke');
const popfilesmoke = document.querySelector('.popfilesmoke');
const userId = document.getElementById('userId').value;
const spanId = document.querySelector('.spanned')
const tree = document.querySelector('.treeRoot')
const fileSpace = document.querySelector('.filename')
let parentFolder;
let usersfiles;

spans.forEach(function(element) {
    element.addEventListener('click', function() {
        console.log(element.id)
        fetch(`/api/v1/users/${userId}/files/${element.id}`, {
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
                console.log(data)
                const Filename = String(data.name)
                console.log(Filename)
                fileSpace.innerText = `file name: ${data.name}`
                fileSpace.value = data._id
                console.log(data.file_contents)
                editor.setValue(`${data.file_contents}`);
            })
            .catch(error => {
                console.error('Problem loading files: ', error);
                throw error;
            })

    })
})

// Function to update the file tree
function updateFileTree(userId) {
    fetch(`/api/v1/users/${userId}/file-tree`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            // tree.innerHTML = "";
            tree.innerHTML = html;
            console.log(html)
            alert('Reload page in order to add another file')
        })
        .catch(error => {
            console.error('Problem updating file tree: ', error);
        });
}

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
            // inserts file icon
        element.parentNode.insertBefore(iconelement, element.nextSibling);
        iconelement.addEventListener('click', function() {
            popupfolder.style.display = 'none';
            popupfile.style.display = 'grid';
            popfilesmoke.style.display = 'block';
            parentFolder = this.parentElement.innerText
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

// LOAD  USER FILES FROM DB
const getUserFiles = (userId) => {
    return fetch(`/api/v1/users/${userId}/files`, {
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
            return data;
        })
        .catch(error => {
            console.error('Problem loading files: ', error);
            throw error;
        })
}



// SAVE FILE (file upload to DB)
fileForm.addEventListener("submit", function(event) {
    event.preventDefault();
    popupfile.style.display = 'none';
    popupfolder.style.display = 'none';
    popfoldersmoke.style.display = 'none';
    popfilesmoke.style.display = 'none'
    const fileNameInput = document.getElementById('fileNameInput');
    const fileName = fileNameInput.value;
    const spid = spanId.id
        // const pid = `${spid}`
    const fileInfo = {
        "name": fileName,
        "parent_folder_id": spid,
        "file_contents": "",
        "children": []
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
    updateFileTree(userId);
})