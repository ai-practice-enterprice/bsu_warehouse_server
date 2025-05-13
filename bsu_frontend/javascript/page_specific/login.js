document.getElementById("responseCard").style.display = "none";

document.addEventListener("submit", (event) => {
    event.preventDefault();
    let inputId = event.submitter.getAttribute("data-inputID");
    
    let formElement = event.target.closest("form");  // <form> contains-> <input type="submit">    
    let formData = new FormData(formElement);
    formData.append("execute_request",inputId);
    formData.append("formClass",formElement.classList);

    fetch(ApacheServerURLPrefix,{
        method: "post",
        body: formData
    })
    .then(
        (response) => response.json()
    )
    .then(
        (responseJsonFormatted) => {
            if(responseJsonFormatted.newlocation){
                window.location.assign(ApacheServerURLPrefix);
            }
            responseCard = document.getElementById("responseCard");
            responseCard.setAttribute("class","card " + responseJsonFormatted.class);
            responseCard.innerHTML = responseJsonFormatted.responseData;
            responseCard.style.display = "block";
        } 
    );
});