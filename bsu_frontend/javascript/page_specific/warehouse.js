async function loadWarehouseMap() {
    const response = await fetch("http://localhost:8000/frontend/zone/map_warehouse", {
        method: "POST",
    });

    if (!response.ok) {
        alert('Failed to fetch the map');
        return;
    } else {
        console.log("Map fetched successfully");
        const svgText = await response.text();
        const svgPlaceHolder = document.getElementById("warehouse_map");
        svgPlaceHolder.innerHTML = svgText;

        console.log("SVG loaded successfully");
        addZoneClickHandlers(svgPlaceHolder);
        addchartData();
    }
}

function addZoneClickHandlers(svgPlaceHolder) {
    svgPlaceHolder.width = window.innerWidth;
    svgPlaceHolder.height = window.innerHeight;
    const zones = svgPlaceHolder.querySelectorAll("rect");

    zones.forEach(zone => {
        zone.addEventListener("click", async () => {
            const zoneId = zone.getAttribute("id");
            if (zoneId) {
                await fetchZoneData(zoneId);
            } else {
                console.error("Zone ID not found for clicked zone");
            }
        });
    });
}

async function addchartData(){
    const chartContainer = document.getElementById('data-holder');
    chartContainer.innerHTML = "";

    try {
        const response = await fetch('http://localhost:8000/frontend/zone/type/count');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        const chart = Plot.plot({
            title: "Number of Zones by Type",
            width: 400,
            height: 400,
            
            x: {
                label: "Zone Type",
                domain: data.map(d => d.zoneTypeName), 
            },
            
            y: {
                label: "Count",
                grid: true
            },
            
            tip: true,
            
            marks: [
                Plot.barY(data, {
                    x: "zoneTypeName",
                    y: "count",
                    fill: "steelblue",
                    title: d => `${d.zoneTypeName}: ${d.count}`
                }),
                Plot.text(data, {
                    x: "zoneTypeName",
                    y: "count",
                    text: "count",
                    dy: -5,
                    fill: "black"
                })
            ],
        });

        
        chartContainer.appendChild(chart);

    } catch (error) {
        console.error("Error fetching or creating the chart:", error);
        chartContainer.innerHTML = `<p style="color: red;">Error loading chart data.</p>`;
    }

}

async function fetchZoneData(zoneId) {
    try {
        const response = await fetch(`http://localhost:8000/frontend/zone/data/${zoneId}`, {
            method: "PATCH",
        });

        if (!response.ok) {
            alert('Failed to fetch zone data');
            return;
        }

        const zoneData = await response.json();
        await displayZoneData(zoneData);
    } catch (error) {
        console.log("Error fetching zone data: " + error);
    }
}

async function displayZoneData(zone) {
    const zoneDataContainer = document.querySelector(".zonedata");
    try {
        let zoneCard = await buildZoneCard(zone,"rect","warehouse map");
        zoneDataContainer.innerHTML = zoneCard.outerHTML;
    } catch (error) {
        console.log("Error displaying data: " + error);
    }

    zoneDataContainer.querySelectorAll(".zoneCapacity").forEach((ele) => {
        ele.addEventListener("input", (e) => {
            document.querySelector(".new-capacity").innerText = e.target.value;
        });
    });
}

window.onload = function() {
    loadWarehouseMap();
};