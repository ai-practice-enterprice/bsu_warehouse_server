document.getElementById('createRobotForm').addEventListener('submit', async e => {
    e.preventDefault();

    const robotType = document.getElementById('robotType').value;
    const robotNamespace = document.getElementById('robotNamespace').value;
    const robotStatus = document.getElementById('robotStatus').checked;

    console.log('Creating robot:', {
        robotType,
        robotNamespace,
        robotStatus
    });

    const response = await fetch(`${serverURLPrefix}/robot`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            robotType,
            robotNamespace,
            robotStatus
        })
    })

    if(!response.ok) {
        alert('Failed to create robot');
        return;
    }

    location.reload();
});

async function getAllRobots() {
    const response = await fetch(`${serverURLPrefix}/robot/all`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })

    if(!response.ok) {
        alert('Failed to fetch robots');
        return;
    }

    const robots = await response.json();
    console.log(robots);

    const robotTableBody = document.getElementById('robotTableBody');

    robots.forEach(async (robot) => {
        row = await buildRobotCard(robot,"row");
        row.addEventListener("click",(e) => {
            if(e.target.getAttribute("data-robot-id")){
                const action = e.target.getAttribute("data-action");
                if (action === "toggle") {
                    toggleStatus(e.target);
                } else if (action === "reset") {
                    resetRobot(e.target);
                }
            }
        });
        robotTableBody.appendChild(row);
    });
}

window.onload = function() {
    getAllRobots();
};