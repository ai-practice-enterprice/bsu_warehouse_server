async function buildRobotCard(robot,mode = "rect",reloadMode = "card" | "warehouse map") {
    // decide what type of robot card to make
    element = null
    switch (mode) {
        case "rect":
            element = await rectangleCard(zone,badgeClass,reloadMode);
            break;
        case "row":
            element = await rowCard(zone,badgeClass);
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
        <td>${robot.robotType}</td>
        <td>${robot.robotNamespace}</td>
        <td>${robotCreationDate}</td>
        <td><span class="${robot.robotStatus ? 'status-active' : 'status-inactive'}">${robot.robotStatus ? 'Active' : 'Inactive'}</span></td>
        <td>
            <button class="${robot.robotStatus ? 'danger-btn' : 'success-btn'}"
                onclick="toggleStatus(${robot.robotID})">
                ${robot.robotStatus ? 'Deactivate' : 'Activate'}
            </button>
        </td>
    `;     
    return row  
}

async function toggleStatus(robot_id) {
    const response = await fetch(`http://localhost:8000/frontend/robot/${robot_id}/toggle`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (!response.ok) {
        alert('Failed to fetch robot data');
        return;
    }

    const robotData = await response.json();

    const rows = document.getElementById('robotTableBody').children;
    
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].children;
        
        if (cells[0].textContent == robot_id) {
            const statusCell = cells[3].children[0];
            const actionButton = cells[4].children[0];
            
            const isCurrentlyActive = statusCell.classList.contains('status-active');
            
            if (isCurrentlyActive) {
                statusCell.classList = "status-inactive";
                statusCell.textContent = 'Inactive';
                actionButton.style.backgroundColor = '#2ecc71';
                actionButton.textContent = 'Activate';
            } else {
                statusCell.classList = "status-active";
                statusCell.textContent = 'Active';
                actionButton.style.backgroundColor = '#e74c3c';
                actionButton.textContent = 'Deactivate';
            }
        }
    }
}