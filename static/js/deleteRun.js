const deleteRunForm = document.getElementById("deleteRunForm");
const deleteRunButton = document.getElementById("deleteRunButton");
const deleteRunList = document.getElementById("deleteRunList");

/**
* Function is called by "DOMContentLoaded" event. It hides or displays different sections of the page depending on whether the 'pageLocation' variable passed from the server contains the string 'runDeleted' or 'deleteRunForm'.
* @param {string} pageSection - pageLocation variable which can be string "runDeleted" or "deleteRunForm".
*/
function hidePageSection(pageSection){
    if(pageSection == "runDeleted"){
        deleteRunForm.classList.add("hide");
        deleteRunButton.classList.add("hide");
        deleteRunList.classList.add("deleted");
    } else if(pageSection == "deleteRunForm") {
        deleteRunForm.classList.remove("hide");
        deleteRunButton.classList.remove("hide");
        deleteRunList.classList.remove("deleted");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    hidePageSection(pageLocation);
});