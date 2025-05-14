async function loadUsers(current_user_id){

    fetch(`${serverURLPrefix}/user/all`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: current_user_id,
        }),
    })
    .then(
        (response) => response.json()
    )
    .then(
        (responseData) => {
        displayUserData(responseData);
    });
}

async function displayUserData(userData) {
    const container = document.getElementById("userTable").querySelector("tbody");

    userData.forEach(async (user) => {
        let userCard = await buildUserCard(user,"row");
        container.appendChild(userCard);
    });
}


window.onload = function() {
    loadUsers(current_user_id);
};


document.getElementById("createUserForm").addEventListener("submit",(e) => {
    e.preventDefault();
    changeUser(e,"create");
});



