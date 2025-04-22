const dataContainer = document.getElementById("data-holder");
const domainSlider = document.getElementById("domainSlider");
const calendarOptionsContainer = document.getElementById("calendar-options"); 
calendarOptionsContainer.style.display = "None";
const lineChartOptionsContainer = document.getElementById("line-chart-options"); 
lineChartOptionsContainer.style.display = "None";
const tabNav = document.getElementById("tabs-nav");
const tabChartNav = document.getElementById("tabs-chart-nav");
const response = fetch("http://localhost:8000/frontend/package/all?group_by=day", {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
})
.then(response => response.json())
.then((response) => {
    data = response;
    data.forEach(record => {
        record.date = new Date(record.date);
    });
});

window.onload = async () => {
    // getPackageIntakeData(mode="line chart"); 
}

/* Event listeners */ // =======================================
domainSlider.addEventListener('input', () => {
    const sliderValue = parseInt(domainSlider.value);
    // map the slider value (0-100) to a domain extent (e.g., 0.01 to 0.1)
    const newDomainExtent = 0.01 + (sliderValue / 100) * 1;

    calendarOptionsContainer.querySelector("label").innerText = sliderValue;
    
    tabOpen = document.getElementById("tabs-nav").querySelector(".tab.active").getAttribute("data-tab-id");
    switch (tabOpen) {
        case "tab-1": 
            renderPackageIntakeCalendarChart(newDomainExtent);
            break;
        case "tab-2": 
            renderPackageStorageCalendarChart(newDomainExtent);
            break;
        default:
            break;
    }
});

tabNav.addEventListener("click",async (e) => {
    if(!e.target.classList.contains("tab")){
        return;
    }

    resetTabs("tabNav");
    e.target.classList = "tab active";

    switch (e.target.getAttribute("data-tab-id")) {
        case "tab-1": 
            calendarOptionsContainer.style.display = "none";
            lineChartOptionsContainer.style.display = "block";
            getPackageIntakeData(mode="line chart"); 
            break;
        case "tab-2": 
            calendarOptionsContainer.style.display = "none";
            lineChartOptionsContainer.style.display = "block";
            getPackageStorageData(mode="line chart"); 
            break;
        default:
            break;
    }
});

tabChartNav.addEventListener("click",async (e) => {
    if(!e.target.classList.contains("tab")){
        return;
    }

    resetTabs("tabChartNav");
    e.target.classList = "tab active";
    
    tabOpen = document.getElementById("tabs-nav").querySelector(".tab.active").getAttribute("data-tab-id");
    mode = e.target.getAttribute("data-mode");

    switch (tabOpen) {
        case "tab-1": 
            getPackageIntakeData(mode); 
            break;
        case "tab-2": 
            getPackageStorageData(mode); 
            break;
        default:
            break;
    }
});

/* get functions */ // =======================================
async function getPackageIntakeData(mode="calendar"){
    let chart = document.createElement("p");
    chart.innerText = `no chart available for ${mode}`;
    const initialDomainExtent = 0.06;

    switch (mode) {
        case "calendar":
            calendarOptionsContainer.style.display = "block";
            lineChartOptionsContainer.style.display = "none";
            renderPackageIntakeCalendarChart(initialDomainExtent);            
            break;
        case "line chart":
            calendarOptionsContainer.style.display = "none";
            lineChartOptionsContainer.style.display = "block";
            renderPackageIntakeLineChart();
            break;
        default:
            dataContainer.innerHTML = "";
            dataContainer.appendChild(chart);
            break;
    }
}

async function getPackageStorageData(mode="calendar"){
    let chart = document.createElement("p");
    chart.innerText = `no chart available for ${mode}`;

    switch (mode) {
        case "calendar":
            calendarOptionsContainer.style.display = "block";
            lineChartOptionsContainer.style.display = "none";
            renderPackageStorageCalendarChart();
            break;
        case "line chart":
            calendarOptionsContainer.style.display = "none";
            lineChartOptionsContainer.style.display = "block";
            renderPackageStorageLineChart();
            break;
        default:
            dataContainer.innerHTML = "";
            dataContainer.appendChild(chart);
            break;
    }
}

function resetTabs(tabsToReset) {
    if(tabsToReset == "tabChartNav"){
        tabChartNav.querySelectorAll(".tab").forEach((element) => {
            element.classList = "tab";
        });
        return;
    }

    if(tabsToReset == "tabNav"){
        tabNav.querySelectorAll(".tab").forEach((element) => {
            element.classList = "tab";
        });
        return;
    }
}

/* chart functions */ // =======================================
function renderPackageIntakeLineChart() {
    dataContainer.innerHTML = "";
    chart = Plot.plot({
        y: {grid: true, label: "Daily Package intake"},
        tip: true,
        marks: [
          Plot.ruleY([0]),
          Plot.lineY(data, {x: "date", y: "count", stroke: "steelblue",tip: "x"}),
          Plot.areaY(data, {x: "date", y: "count", fillOpacity: 0.2}),
        ]
    });
    dataContainer.appendChild(chart);
}

function renderPackageIntakeCalendarChart(domainExtent) {
    dataContainer.innerHTML = "";
    const chart = Plot.plot({
        padding: 0,
        x: { axis: null },
        y: { tickFormat: Plot.formatWeekday("en", "narrow"), tickSize: 0 },
        fy: { tickFormat: "", reverse: true },
        color: {
            scheme: "RdBu",
            legend: true,
            label: "Daily change of package intake",
            tickFormat: "+%",
            domain: [-domainExtent, domainExtent], // Dynamic domain
            type: "linear",
        },
        tip: true,
        marks: [
            Plot.cell(data, {
                x: (d) => d3.utcWeek.count(d3.utcYear(d.date), d.date),
                y: (d) => d.date.getUTCDay(),
                fy: (d) => d.date.getUTCFullYear(),
                fill: (d, i) => i > 0 ? ((d.count - data[i - 1].count) / data[i - 1].count) : NaN,
                title: (d, i) => i > 0 ? ("Number of packages: " + d.count + "\nChange " + (((d.count - data[i - 1].count) / data[i - 1].count) * 100).toFixed(2) + "%\nDate: " + d.date) : NaN,
                inset: 0.5,
            })
        ]
    });
    dataContainer.appendChild(chart);
}

async function renderPackageStorageCalendarChart() {
    dataContainer.innerHTML = "";
}

async function renderPackageStorageLineChart() {
    dataContainer.innerHTML = "";
}