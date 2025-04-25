async function buildRobotCard(robot,mode = "rect",reloadMode = "card") {
    // Determine badge class based on robot type
    let badgeClass = 'badge-robot';
    switch (robot.robotTypes.robotTypeName) {
        case "Jetracer":         badgeClass = 'badge-jetracer'; break;
        case "Jetank": badgeClass = 'badge-jetank'; break;
        case "Jetank_Hiwonder":      badgeClass = 'badge-jetank-hiwonder'; break;
        default:
            badgeClass = 'badge-default';
            break;
    }

    // decide what type of robot card to make
    element = null
    switch (mode) {
        case "rect":
            element = await rectangleCard(robot,badgeClass,reloadMode);
            break;
        case "row":
            element = await rowCard(robot,badgeClass);
            break;
        default:
            break;
    }
    
    return element
}

async function rowCard(robot) {    
    let date = new Date(robot.insertDate);
    let robotCreationDate = date.toDateString();
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${robot.robotID}</td>
        <td>${robot.robotTypeName}</td>
        <td>${robot.robotNamespace}</td>
        <td>${robotCreationDate}</td>
        <td><span class="${robot.robotStatus ? 'status-active' : 'status-inactive'}">${robot.robotStatus ? 'Active' : 'Inactive'}</span></td>
        <td>
            <button class="${robot.robotStatus ? 'danger-btn' : 'success-btn'}"
                data-robot-id="${robot.robotID}">
                ${robot.robotStatus ? 'Deactivate' : 'Activate'}
            </button>
        </td>
    `;     
    return row  
}

async function toggleStatus(target) {
    robot_id = target.getAttribute("data-robot-id");
    
    const response = await fetch(`${serverURLPrefix}/robot/${robot_id}/toggle`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (!response.ok) {
        alert('Failed to fetch robot data');
        return;
    }

    const row = target.closest("tr");
    const spanStatus = row.querySelector("span");
    console.log(row,spanStatus);
    const isCurrentlyActive = spanStatus.classList.contains('status-active');

    if (isCurrentlyActive) {
        spanStatus.textContent = 'Inactive';
        spanStatus.classList = "status-inactive";
        spanStatus.style.color = '#e74c3c';
        
        target.classList = 'success-btn';
        target.textContent = 'Activate';
    } else {
        spanStatus.textContent = 'Active';
        spanStatus.classList = "status-active";
        spanStatus.style.color = '#2ecc71';
        
        target.classList = 'danger-btn';
        target.textContent = 'Deactivate';
    }
}