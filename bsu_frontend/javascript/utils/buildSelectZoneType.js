async function buildSelectZoneType(mode="create",zoneID) {
    const response = await fetch("http://localhost:8000/frontend/zone/type/all", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        alert('Failed to fetch the zone types');
        return;
    }

    const zones = await response.json();

    switch (mode) {
        case "create":
            var zoneType = document.createElement("select");
            zoneType.setAttribute("id","zoneType");
            zoneType.setAttribute("name","zoneType");
            zoneType.required = true;
            break;
        case "add":
            var zoneType = document.getElementById("zoneType");
            break;
        default:
            break;
    }

    zoneType.innerHTML =  '<option value="">Select new type</option>';
    console.log("adding options to select element")
    zones.forEach(async (zone) => {
        const option = document.createElement('option');
        option.value = zone.zoneTypeName;
        option.text = zone.zoneTypeDescription;
        zoneType.appendChild(option);
    });

    return zoneType;
}