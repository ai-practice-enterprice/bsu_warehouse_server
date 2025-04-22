// Enter a zone (set as checked)
async function enterZone(zoneId,reloadMode = "card" | "warehouse map") {
    try {
        console.log(`Entering zone ${zoneId}`);
        
        const response = await fetch(`http://localhost:8000/frontend/zone/${zoneId}/enter`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to enter zone');
        }
        
        // Reload zones to refresh UI
        switch (reloadMode) {
            case "card": 
                await loadZones(); 
                break;
            case "warehouse map": 
                await loadWarehouseMap();
                await fetchZoneData(zoneId); 
                break;
            default:
                break;
        }
        
    } catch (error) {
        console.error('Error entering zone:', error);
        alert(error.message || 'Failed to enter zone. Please try again.');
    }
}