const cellSize = 16; // height of a day
    const height = cellSize * 7; // height of a week (5 days + padding)
    const width = (cellSize + 1.5) * 53; // width of the chart
    
    // Define formatting functions for the axes and tooltips.
    const formatDate = d3.utcFormat("%x");
    const formatDay = i => "SMTWTFS"[i];
    const formatMonth = d3.utcFormat("%b");
    
    // Helpers to compute a day’s position in the week.
    const timeWeek = d3.utcMonday; 
    const countDay = i => (i + 6) % 7;

    const color = d3.scaleSequential(d3.interpolateRdPu).domain([0, 2500]);
    
    // Group data by year, in reverse input order. (Since the dataset is chronological,
    // this will show years in reverse chronological order.)
    const years = d3.groups(data, d => d.date.toUTCString()).reverse();
    
    // A function that draws a thin white line to the left of each month.
    function pathMonth(t) {
        const d = Math.max(0, Math.min(5, countDay(t.getUTCDay())));
        const w = timeWeek.count(d3.utcYear(t), t);
        return `${d === 0 ? `M${w * cellSize},0`
            : d === 5 ? `M${(w + 1) * cellSize},0`
            : `M${(w + 1) * cellSize},0V${d * cellSize}H${w * cellSize}`}V${5 * cellSize}`;
    }
    
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height * years.length)
        .attr("viewBox", [0, 0, width, height * years.length])
        .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");
    
    const year = svg.selectAll("g")
        .data(years)
        .join("g")
        .attr("transform", (d, i) => `translate(40.5,${height * i + cellSize * 1.5})`);
    
    year.append("text")
        .attr("x", -5)
        .attr("y", -5)
        .attr("font-weight", "bold")
        .attr("text-anchor", "end")
        .text(([key]) => key);
    
    year.append("g")
        .attr("text-anchor", "end")
        .selectAll()
        .data(d3.range(1, 6))
        .join("text")
        .attr("x", -5)
        .attr("y", i => (countDay(i) + 0.5) * cellSize)
        .attr("dy", "0.31em")
        .text(formatDay);
    
    year.append("g")
        .selectAll()
        .data(([, values]) => values.filter(d => ![0, 6].includes(d.date.getUTCDay())))
        .join("rect")
        .attr("width", cellSize - 1)
        .attr("height", cellSize - 1)
        .attr("x", d => timeWeek.count(d3.utcYear(d.date), d.date) * cellSize + 0.5)
        .attr("y", d => countDay(d.date.getUTCDay()) * cellSize + 0.5)
        .attr("fill", d => color(d.count))
        .append("title")
        .text(d => `${formatDate(d.date)} ${d.count}`);
    
    const month = year.append("g")
        .selectAll()
        .data(([, values]) => d3.utcMonths(d3.utcMonth(values[0].date), values.at(-1).date))
        .join("g");
    
    month.filter((d, i) => i).append("path")
        .attr("fill", "none")
        .attr("stroke", "#fff")
        .attr("stroke-width", 3)
        .attr("d", pathMonth);
    
    month.append("text")
        .attr("x", d => timeWeek.count(d3.utcYear(d), timeWeek.ceil(d)) * cellSize + 2)
        .attr("y", -5)
        .text(formatMonth);