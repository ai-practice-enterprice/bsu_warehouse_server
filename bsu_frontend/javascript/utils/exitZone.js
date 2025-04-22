// Exit a zone (set as not checked)
async function exitZone(zoneId,reloadMode = "card" | "warehouse map") {
    try {
        console.log(`Exiting zone ${zoneId}`);
        
        const response = await fetch(`http://localhost:8000/frontend/zone/${zoneId}/exit`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to exit zone');
        }
        
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
        
    } catch (error) {
        console.error('Error exiting zone:', error);
        alert(error.message || 'Failed to exit zone. Please try again.');
    }
}