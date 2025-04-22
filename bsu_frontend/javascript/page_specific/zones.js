// Tab switching functionality
function switchTab(event, tabId) {
    // Hide all tab contents
    const tabContents = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove("active");
    }
    
    // Remove active class from all tabs
    const tabs = document.getElementsByClassName("tab");
    for (let i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("active");
    }
    
    // Show the selected tab content and mark tab as active
    document.getElementById(tabId).classList.add("active");
    event.currentTarget.classList.add("active");
}

// Load zones for dropdowns and zone list
async function loadZones() {
    try {
        const response = await fetch('http://localhost:8000/frontend/zone/all');
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Server response not OK:', response.status, errorText);
            throw new Error(`Failed to fetch zones: ${response.status} ${response.statusText}`);
        }
        
        const zones = await response.json();
        console.log('Zones loaded successfully:', zones);
        
        // Populate zone dropdowns
        const startZoneSelect = document.getElementById('pathZoneStart');
        const endZoneSelect = document.getElementById('pathZoneEnd');
        
        // Clear existing options except the default one
        startZoneSelect.innerHTML = '<option value="">Select Start Zone</option>';
        endZoneSelect.innerHTML = '<option value="">Select End Zone</option>';
        
        // Add zone options
        zones.forEach(zone => {
            const option = document.createElement('option');
            option.value = zone.zoneID;
            option.text = `${zone.zoneID} - ${zone.zoneName} (${zone.zoneType})`;
            
            startZoneSelect.appendChild(option.cloneNode(true));
            endZoneSelect.appendChild(option);
        });
        
        // Populate zone table
        const zoneTableBody = document.getElementById('zoneTableBody');
        zoneTableBody.innerHTML = '';
        
        zones.forEach(async (zone) => {
            row = await buildZoneCard(zone,mode="row")
            zoneTableBody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading zones:', error);
        alert('Failed to load zones. Please check console for details.');
    }
}

// Load paths for path list
async function loadPaths() {
    try {
        const response = await fetch('http://localhost:8000/frontend/path/all');
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Server response not OK:', response.status, errorText);
            throw new Error(`Failed to fetch paths: ${response.status} ${response.statusText}`);
        }
        
        const paths = await response.json();
        console.log('Paths loaded successfully:', paths);
        
        // Populate path table
        const pathTableBody = document.getElementById('pathTableBody');
        pathTableBody.innerHTML = '';
        
        paths.forEach(path => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${path.pathID}</td>
                <td>${path.pathNumber}</td>
                <td><span class="badge badge-zone">${path.zoneStart.zoneName}</span></td>
                <td><span class="badge badge-zone">${path.zoneEnd.zoneName}</span></td>
                <td>${path.pathDescription}</td>
                <td><span class="${path.pathActive ? 'status-active' : 'status-inactive'}">${path.pathActive ? 'Active' : 'Inactive'}</span></td>
                <td class="action-buttons">
                    <button class="${path.pathActive ? 'danger-btn' : 'success-btn'}" 
                            onclick="togglePathStatus(${path.pathID})">
                        ${path.pathActive ? 'Deactivate' : 'Activate'}
                    </button>
                    <button class="warning-btn" onclick="viewPath(${path.pathID})">View</button>
                </td>
            `;
            
            pathTableBody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading paths:', error);
        alert('Failed to load paths. Please check console for details.');
    }
}

// Zone form submission
document.getElementById('createZoneForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form values
    const zoneName = document.getElementById('zoneName').value;
    const zoneType = document.getElementById('zoneType').value;
    const zoneDescription = document.getElementById('zoneDescription').value;
    const zoneAvailable = document.getElementById('zoneAvailable').checked;
    const zoneCheck = document.getElementById('zoneCheck').checked;
    
    try {
        const response = await fetch('http://localhost:8000/frontend/zone', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                zoneName,
                zoneType,
                zoneDescription,
                zoneAvailable,
                zoneCheck
            })
        });
        
        if (!response.ok) {
            const errorData = await response.text();
            console.error('Server response error:', response.status, errorData);
            throw new Error(`Failed to create zone: ${response.status} ${response.statusText}`);
        }
        
        // Reset form
        this.reset();
        document.getElementById('zoneAvailable').checked = true;
        document.getElementById('zoneCheck').checked = false;
        
        // Reload zones
        await loadZones();
        
        // Show success message
        alert('Zone created successfully!');
        
        // Switch to zone list tab
        switchTab({currentTarget: document.querySelector('.tab:nth-child(3)')}, 'zoneListTab');
        
    } catch (error) {
        console.error('Error creating zone:', error);
        alert('Failed to create zone. Please check console for details.');
    }
});

// Path form submission
document.getElementById('createPathForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form values
    const pathNumber = parseInt(document.getElementById('pathNumber').value);
    const pathDescription = document.getElementById('pathDescription').value;
    const pathZoneStart = parseInt(document.getElementById('pathZoneStart').value);
    const pathZoneEnd = parseInt(document.getElementById('pathZoneEnd').value);
    const pathActive = document.getElementById('pathActive').checked;
    
    // Get coordinates
    const coordPairs = document.querySelectorAll('.coordinate-pair');
    const pathCoordinates = [];
    
    coordPairs.forEach(pair => {
        const x = parseFloat(pair.querySelector('.coord-x').value);
        const y = parseFloat(pair.querySelector('.coord-y').value);
        if (!isNaN(x) && !isNaN(y)) {
            pathCoordinates.push([x, y]);
        }
    });
    
    if (pathCoordinates.length === 0) {
        alert('Please add at least one coordinate pair');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:8000/frontend/path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                pathNumber,
                pathDescription,
                pathZoneStart,
                pathZoneEnd,
                pathCoordinates,
                pathActive
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create path');
        }
        
        // Reset form
        this.reset();
        document.getElementById('pathActive').checked = false;
        document.getElementById('coordinatesList').innerHTML = `
            <div class="coordinate-pair">
                <input type="number" placeholder="X" class="coord-x" required>
                <input type="number" placeholder="Y" class="coord-y" required>
            </div>
        `;
        
        // Reset visualization
        document.getElementById('startZoneDisplay').textContent = 'Select Start Zone';
        document.getElementById('endZoneDisplay').textContent = 'Select End Zone';
        
        // Reload paths
        await loadPaths();
        
        // Show success message
        alert('Path created successfully!');
        
        // Switch to path list tab
        switchTab({currentTarget: document.querySelector('.tab:nth-child(4)')}, 'pathListTab');
        
    } catch (error) {
        console.error('Error creating path:', error);
        alert('Failed to create path. Please try again later.');
    }
});

// Zone availability toggle
async function toggleAvailability(id) {
    try {
        const response = await fetch(`http://localhost:8000/frontend/zone/${id}/toggle`, {
            method: 'PATCH'
        });
        
        if (!response.ok) {
            throw new Error('Failed to toggle zone availability');
        }
        
        // For demonstration, let's toggle the status in the UI
        const rows = document.getElementById('zoneTableBody').children;
        
        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].children;
            
            if (cells[0].textContent == id) {
                const statusCell = cells[4].children[0];
                const actionButton = cells[6].children[0];
                
                const isCurrentlyAvailable = statusCell.classList.contains('status-available');
                
                if (isCurrentlyAvailable) {
                    statusCell.classList.remove('status-available');
                    statusCell.classList.add('status-unavailable');
                    statusCell.textContent = 'Unavailable';
                    
                    actionButton.classList.remove('danger-btn');
                    actionButton.classList.add('success-btn');
                    actionButton.textContent = 'Set Available';
                } else {
                    statusCell.classList.remove('status-unavailable');
                    statusCell.classList.add('status-available');
                    statusCell.textContent = 'Available';
                    
                    actionButton.classList.remove('success-btn');
                    actionButton.classList.add('danger-btn');
                    actionButton.textContent = 'Set Unavailable';
                }
                
                break;
            }
        }
        
    } catch (error) {
        console.error('Error toggling zone availability:', error);
        alert('Failed to toggle zone availability. Please try again later.');
    }
}

// Path status toggle
async function togglePathStatus(id) {
    try {
        const response = await fetch(`http://localhost:8000/frontend/path/${id}/toggle`, {
            method: 'PATCH'
        });
        
        if (!response.ok) {
            throw new Error('Failed to toggle path status');
        }
        
        // For demonstration, let's toggle the status in the UI
        const rows = document.getElementById('pathTableBody').children;
        
        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].children;
            
            if (cells[0].textContent == id) {
                const statusCell = cells[5].children[0];
                const actionButton = cells[6].children[0];
                
                const isCurrentlyActive = statusCell.classList.contains('status-active');
                
                if (isCurrentlyActive) {
                    statusCell.classList.remove('status-active');
                    statusCell.classList.add('status-inactive');
                    statusCell.textContent = 'Inactive';
                    
                    actionButton.classList.remove('danger-btn');
                    actionButton.classList.add('success-btn');
                    actionButton.textContent = 'Activate';
                } else {
                    statusCell.classList.remove('status-inactive');
                    statusCell.classList.add('status-active');
                    statusCell.textContent = 'Active';
                    
                    actionButton.classList.remove('success-btn');
                    actionButton.classList.add('danger-btn');
                    actionButton.textContent = 'Deactivate';
                }
                
                break;
            }
        }
        
    } catch (error) {
        console.error('Error toggling path status:', error);
        alert('Failed to toggle path status. Please try again later.');
    }
}

// Update path visualization
function updateStartZoneDisplay() {
    const select = document.getElementById('pathZoneStart');
    const display = document.getElementById('startZoneDisplay');
    
    if (select.value) {
        const selectedOption = select.options[select.selectedIndex];
        display.textContent = selectedOption.text.split(' - ')[1].split(' (')[0];
    } else {
        display.textContent = 'Select Start Zone';
    }
}

function updateEndZoneDisplay() {
    const select = document.getElementById('pathZoneEnd');
    const display = document.getElementById('endZoneDisplay');
    
    if (select.value) {
        const selectedOption = select.options[select.selectedIndex];
        display.textContent = selectedOption.text.split(' - ')[1].split(' (')[0];
    } else {
        display.textContent = 'Select End Zone';
    }
}

// Add/remove coordinate pairs
function addCoordinatePair() {
    const container = document.getElementById('coordinatesList');
    const newPair = document.createElement('div');
    newPair.className = 'coordinate-pair';
    newPair.innerHTML = `
        <input type="number" placeholder="X" class="coord-x" required>
        <input type="number" placeholder="Y" class="coord-y" required>
    `;
    container.appendChild(newPair);
}

function removeCoordinatePair() {
    const container = document.getElementById('coordinatesList');
    if (container.children.length > 1) {
        container.removeChild(container.lastChild);
    }
}

// Load data when the page loads
window.onload = function() {
    loadZones();
    loadPaths();
};