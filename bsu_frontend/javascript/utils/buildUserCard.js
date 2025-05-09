async function buildUserCard(user,mode = "rect") {
    let badgeClass = 'badge-user';
    switch (user.adminPrivilege) {
        case true:          badgeClass = 'badge-admin-user'; break;
        case false:         badgeClass = 'badge-normal-user'; break;
        default:
            badgeClass = 'badge-default';
            break;
    }

    // decide what type of robot card to make
    element = null
    switch (mode) {
        case "rect":
            element = await rectangleCard(user,badgeClass);
            break;
        case "row":
            element = await rowCard(user,badgeClass);
            break;
        default:
            break;
    }
    
    return element
}

async function rowCard(user,badgeClass) {    
    let date = new Date(user.registrationDate);
    let userRegistrationDate = date.toDateString();
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${user.userID}</td>
        <td>${user.userName}</td>
        <td>${userRegistrationDate}</td>
        <td><span class="badge ${badgeClass}">${user.adminPrivilege ? 'Admin' : 'Worker'}</span></td>
        <td>${user.active ? 'Active' : 'Unactive'}</td>
        <td class="action-buttons">
            <button class="warning-btn" onclick="editUser(${user.userID})">Edit</button>
        </td>
    `;     
    return row;
}

async function rectangleCard(user,badgeClass) {
    let date = new Date(user.registrationDate);
    let userRegistrationDate = date.toDateString();
    const userCard = document.createElement('div');
    userCard.innerHTML += `
        <table>
            <tr>
                <th>Email address</th>
                <th>Registration date</th>
                <th>privilege</th>
                <th>Status</th>
            </tr>
            <tr>
                <td>${user.userName}</td>
                <td>${userRegistrationDate}</td>
                <td><span class="badge ${badgeClass}">${user.adminPrivilege ? 'Admin' : 'Worker'}</span></td>
                <td>${user.active ? 'Active' : 'Unactive'}</td>
            </tr>
        </table>
        <div class="card">
            <form id="changeUserForm">
                <div class="form-group">
                    <label for="adminPrivilege">User Type</label>
                    <select id="adminPrivilege" name="adminPrivilege">
                        <option ${user.adminPrivilege ? "selected" : ""} value="true">Admin</option>
                        <option ${user.adminPrivilege ? "" : "selected"} value="false">Worker</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="userName">Username</label>
                    <input type="email" id="userName" name="userName" placeholder="${user.userName}">
                </div>

                <div class="form-group">
                    <label for="userPassword">User password</label>
                    <input type="password" id="userPassword" name="userPassword">
                </div>
                
                <div class="form-group checkbox-group">
                    <input type="checkbox" id="userStatus" name="userStatus" ${user.active ? 'checked' : ''}>
                    <label for="userStatus">Active Status</label>
                </div>
                
                <button type="submit" value=${user.userID}>Change User</button>
                <button type="submit" class="closeBtn">Cancel</button>
            </form>
        </div>
    `;

    return userCard;
}

function editUser(userID) {
    fetch(`${serverURLPrefix}/user/select`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: userID,
        }),
    })
    .then( 
        (response) => response.json()
    )
    .then(
        async (data) => {
            if (data[0].userID !== null) {
                console.log(data,data[0].userID);
                let newDialog = document.createElement("dialog");
    
                // newDialog.setAttribute("class","card");
                newDialog.addEventListener("submit",(e) => {
                    e.preventDefault();

                    if(e.target.classList == "closeBtn"){
                        closeElement(e);
                    } 
                    else {
                        changeUser(e,"update");
                    }
                });
                
                let userCard = await buildUserCard(data[0],"rect");
                
                newDialog.append(userCard);
                try{
                    document.body.appendChild(newDialog);
                    newDialog.showModal();
                    newDialog.classList.add("opening");

                }catch(error) {
                    console.error('Error fetching user:', error);
                }
            }
        }
    )
}

function closeElement(event){
    var dialogElement = event.target.closest("dialog");
    
    if(dialogElement){
        dialogElement.classList.remove("opening");
        dialogElement.classList.add("closing");
        dialogElement.addEventListener("transitionend",() => {
            dialogElement.close();
            dialogElement.remove();
        },{once: true});
        return;
    } 
    return;

}

function changeUser(e,mode){
    closeElement(e);
    
    let form = e.target.closest("form");
    let formData = new FormData(form);

    var object = {};
    formData.forEach(function(value, key){
        object[key] = value;
    });

    if (object["userStatus"] == "on"){
        object["userStatus"] = "True";
    } else {
        object["userStatus"] = "False";
    }

    if (object["adminPrivilege"] == "true"){
        object["adminPrivilege"] = "True";
    } else {
        object["adminPrivilege"] = "False";
    }
    

    switch (mode) {
        case "create":
            object["userImagePath"] = "";
            fetch(`${serverURLPrefix}/user`,{
                method: "post",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    active : object["userStatus"],
                    admin_privilege : object["adminPrivilege"],
                    user_image_path : object["userImagePath"],
                    user_name : object["userName"],
                    user_password : object["userPassword"],
                }),
            });
            
            break;
        case "update":
            object["user_id"] = current_user_id;

            console.log(object);

            fetch(`${serverURLPrefix}/user/update`,{
                method: "post",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_id : object["user_id"],
                    admin_privilege : object["adminPrivilege"],
                    user_name : object["userName"],
                    user_password : object["userPassword"],
                    active : object["active"],
                }),
            });
    
            break;
        default:
            alert("Client : No action received");
            break;
    }

}
