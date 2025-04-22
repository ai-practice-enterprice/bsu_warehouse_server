async function buildZoneCard(zone,mode = "rect",reloadMode = "card" | "warehouse map") {

    // Determine badge class based on zone type
    let badgeClass = 'badge-zone';
    switch (zone.zoneTypes.zoneTypeName) {
        case "Void":         badgeClass = 'badge-void';         break;
        case "RobotStation": badgeClass = 'badge-robotstation'; break;
        case "Storage":      badgeClass = 'badge-storage';      break;
        case "DropZoneIn":   badgeClass = 'badge-dropzonein';   break;
        case "ErrorZone":    badgeClass = 'badge-errorzone';    break;
        case "Normal":       badgeClass = 'badge-normal';       break;
        case "DropZoneOut":  badgeClass = 'badge-dropzoneout';  break;
        default:
            break;
    }
    // decide what type of zone card to make
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
    
    return element;
}

async function rowCard(zone,badgeClass) {    
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${zone.zoneID}</td>
        <td>${zone.zoneName}</td>
        <td><span class="badge ${badgeClass}">${zone.zoneTypes.zoneTypeName}</span></td>
        <td>${zone.zoneDescription}</td>
        <td><span class="${zone.zoneAvailable ? 'status-available' : 'status-unavailable'}">${zone.zoneAvailable ? 'Available' : 'Unavailable'}</span></td>
        <td>${zone.zoneCheck ? 'Yes' : 'No'}</td>
        <td class="action-buttons">
            <button class="${zone.zoneAvailable ? 'danger-btn' : 'success-btn'}" 
                    onclick="toggleAvailability(${zone.zoneID})">
                ${zone.zoneAvailable ? 'Set Unavailable' : 'Set Available'}
            </button>
            <button class="warning-btn" onclick="editZone(${zone.zoneID})">Edit</button>
        </td>
    `;     
    return row;
}

async function rectangleCard(zone,badgeClass,reloadMode) {
    let selectElement = null;
    try {
        selectElement = await buildSelectZoneType(mode="create",zone.zoneID);
    } catch (error) {
        console.log("could not fetch zone types: " + error);
    }
    let selectHTML = selectElement.outerHTML;

    const zoneCard = document.createElement('div');
    zoneCard.className = 'zone-card';
    /*  title of the card => perhaps add more styling */
    zoneCard.innerHTML = `<h3>${zone.zoneName}</h3>`;
    /*  the details contain the badge + desc + status of zone */
    zoneCard.innerHTML += `
        <div class="zone-details">
            <p>
                <span class="badge ${badgeClass}">
                    ${zone.zoneTypes.zoneTypeName}
                </span>
            </p>
            <p>${zone.zoneDescription}</p>
            <p>Status: 
                <span class="${zone.zoneAvailable ? 'status-available' : 'status-unavailable'}">
                        ${zone.zoneAvailable ? 'Available' : 'Occupied'}
                </span>
            </p>
        </div>
    `;
    /*  [OPTIONAL] based upon the zone type to change the zone's capacity */
    if (zone.zoneTypes.zoneTypeName.includes("DropZone") || zone.zoneTypes.zoneTypeName.includes("Storage")){
        zoneCard.innerHTML += `
            <div class="form-group" style="flex: 1;">
                <p>Current capacity:
                    <span class="zone-capacity">${zone.zoneCapacity}</span>
                </p>
                <p>New capacity:
                    <span class="zone-capacity new-capacity">${zone.zoneCapacity}</span>
                </p>
                <input type="range" class="zoneCapacity" id="zoneCapacity" name="zoneCapacity" value="${zone.zoneCapacity}" min="0" max="8" step="1"/>
                <button class="change-type-btn" onclick="changeZoneCapacity(${zone.zoneID})">Change zone capacity</button>
            </div>
        `;
    }
    /*  to change the zone's functionality  */
    zoneCard.innerHTML += `
        <div class="form-group" style="flex: 1;">
            <label for="zoneType">Zone Type</label>
            ${selectHTML}
            <button class="change-type-btn" onclick="changeZoneType(${zone.zoneID},'${reloadMode}')">Change zone function</button>
        </div>
    `;

    // zone.zoneCapacity

    if (zone.zoneTypes.zoneTypeName.includes("DropZone")){
        zoneCard.innerHTML += `<div class="zone-actions">
            ${zone.zoneAvailable 
                ? `<button class="success-btn" onclick="enterZone(${zone.zoneID},'${reloadMode}')">Enter Zone</button>`
                : `<button class="danger-btn" onclick="exitZone(${zone.zoneID},'${reloadMode}')">Exit Zone</button>`
            }
        </div>`
    }
    return zoneCard;
}

async function changeZoneCapacity(zoneID,reloadMode) {
    let newZoneCapacity = document.getElementById("zoneCapacity").value;
    const response = await fetch(`http://localhost:8000/frontend/zone/change/capacity?zone_id=${zoneID}&new_zone_capacity=${newZoneCapacity}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    // Reload zones to refresh UI
    switch (reloadMode) {
        case "card": 
            await loadZones(); 
            break;
        case "warehouse map": 
            await loadWarehouseMap();
            await fetchZoneData(zoneID); 
            break;
        default:
            break;
    }
} 

async function changeZoneType(zoneID,reloadMode) {
    let newZoneType = document.getElementById("zoneType").value;
    const response = await fetch(`http://localhost:8000/frontend/zone/change/type?zone_id=${zoneID}&new_zone_type=${newZoneType}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    // Reload zones to refresh UI
    switch (reloadMode) {
        case "card": 
            await loadZones(); 
            break;
        case "warehouse map": 
            await loadWarehouseMap();
            await fetchZoneData(zoneID); 
            break;
        default:
            break;
    }
} 