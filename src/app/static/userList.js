// called when the page loads to get the added user list
function getAddedUserList() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = eval(this.response);
            for (const message of messages) {
                addUserList(message, "added user");
            }
        }
    };
    request.open("GET", "/addedUserList");
    request.send();
}

// called when the page loads to get the blocked user list
function getblockeduserlist() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = eval(this.response);
            for (const message of messages) {
                addUserList(message, "blocked user");
            }
        }
    };
    request.open("GET", "/blockedUserList");
    request.send();
}

// Renders a new user to the page
function addUserList(userList, status) {
    let myList = None
    if(status == "added user"){
        myList = document.getElementById('addedUserList');
    }else if(status = "blocked user"){
        myList = document.getElementById('blockedUserList');
    }
    myList.innerHTML += '<option value="' + userList["username"] + '"></option>';
}

// called when the page loads to add user page. This function will call other two functions to get user list
function welcome() {
    getAddedUserList()
    getblockeduserlist()
}
