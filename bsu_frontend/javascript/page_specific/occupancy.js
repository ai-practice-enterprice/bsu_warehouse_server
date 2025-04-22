async function loadZones(zoneType = "DropZoneIn") {
    try {
        console.log('Fetching zone data...');
         
        // Get all zones
        const response = await fetch(`http://localhost:8000/frontend/zone/type?zone_type=${zoneType}`);

        if (!response.ok) {
            throw new Error(`Failed to fetch zones: ${response.status}`);
        }
        
        const zones = await response.json();
        console.log('Zones fetched:', zones);
        
        // Handle no zones case
        const noZonesMessage = document.getElementById('noZonesMessage');
        const zoneGrid = document.getElementById('zoneGrid');
        
        if (zones.length === 0) {
            noZonesMessage.style.display = 'block';
            zoneGrid.style.display = 'none';
            return;
        }
        
        // Show zone grid
        noZonesMessage.style.display = 'none';
        zoneGrid.style.display = 'grid';
        
        // Clear existing zone cards
        zoneGrid.innerHTML = '';
        
        // Create a card for each zone
        console.log('Creating zone card...');
        zones.forEach(async (zone) => {
            zoneCard = await buildZoneCard(zone,"rect","card")
            zoneGrid.appendChild(zoneCard);
        });

        zoneGrid.querySelectorAll(".zone-card").forEach((ele) => {
            rangeInput = ele.querySelector(".zoneCapacity");
            rangeInput.addEventListener("change", (e) => {
                ele.querySelector(".new-capacity").innerText = e.target.value;
            });
        });
        
    } catch (error) {
        console.error('Error loading zones:', error);
        alert('Failed to load zone data. Please try again later.');
    }
}

document.getElementById("zoneType").addEventListener("change", (e) => {
    // console.log(e.target.value)
    loadZones(e.target.value)
})

let interval = null;

window.onload = function() {
    loadZones("DropZoneIn");
};
