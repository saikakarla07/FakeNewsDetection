const socket = io();

/* ================= ELEMENTS ================= */
const totalEl = document.getElementById("total");
const realEl = document.getElementById("real");
const fakeEl = document.getElementById("fake");
const recentList = document.getElementById("recentList");

const pieCanvas = document.getElementById("pieChart");
const hourCanvas = document.getElementById("hourChart");


/* ================= STATE ================= */
let chartPie, chartHour;
let history = [];
let currentPeriod = "today";


/* ================= INIT ================= */
window.onload = async () => {
    await loadData();
    setInterval(loadData, 3000);
};


/* ================= LOAD ================= */
async function loadData() {
    const res = await fetch("/stats-data");
    const data = await res.json();

    history = data.history || [];
    render();
}


/* ================= SOCKET ================= */
socket.on("stats_update", (data) => {
    history = data.history;
    render();
});


/* ================= FILTER ================= */
function filterHistory() {
    const now = Date.now();

    return history.filter(x => {
        const diff = now - new Date(x.time).getTime();

        if (currentPeriod === "week")
            return diff <= 7 * 24 * 3600000;

        return diff <= 24 * 3600000;
    });
}


/* ================= RENDER ================= */
function render() {
    const periodText = document.getElementById("periodText");

    if(currentPeriod === "week"){
        periodText.innerText = "Activity from the last 7 days";
    }else{
        periodText.innerText = "Activity from the last 24 hours";
    }
    const filtered = filterHistory();

    const total = filtered.length;
    const real = filtered.filter(x => x.label === "Real").length;
    const fake = total - real;

    totalEl.innerText = total;
    realEl.innerText = real;
    fakeEl.innerText = fake;


    /* ================= PIE ================= */
    if (chartPie) chartPie.destroy();

    chartPie = new Chart(pieCanvas, {
        type: "doughnut",
        data: {
            labels: ["Real", "Fake"],
            datasets: [{
                data: [real, fake],
                backgroundColor: ["#22c55e", "#ef4444"],
                borderWidth: 0
            }]
        },
        options: {
            cutout: "70%",
            animation: { animateRotate: true }
        }
    });


    /* ================================================= */
    /* ============ HOURLY FIXED LABELS ================= */
    /* ================================================= */
    if (chartHour) chartHour.destroy();

    const realHours = new Array(24).fill(0);
    const fakeHours = new Array(24).fill(0);

    filtered.forEach(x => {
        const h = new Date(x.time).getHours();
        x.label === "Real" ? realHours[h]++ : fakeHours[h]++;
    });

    /* 🔥 FULL 24 labels (correct) */
    const hourLabels = Array.from({ length: 24 }, (_, i) =>
        i.toString().padStart(2, "0")
    );

    chartHour = new Chart(hourCanvas, {
        type: "bar",
        data: {
            labels: hourLabels,
            datasets: [
                {
                    label: "Real",
                    data: realHours,
                    backgroundColor: "#22c55e",
                    borderRadius: 6
                },
                {
                    label: "Fake",
                    data: fakeHours,
                    backgroundColor: "#ef4444",
                    borderRadius: 6
                }
            ]
        },
        options: {
            animation: { duration: 900 },
            scales:{
    x:{
        ticks:{ color:"#9ca3af" },
        grid:{ color:"#1f2937" }
    },
    y:{
        beginAtZero:true,
        ticks:{
            color:"#9ca3af",
            precision:0,     // ✅ integers only
            stepSize:1       // ✅ 0,1,2,3 (no decimals)
        },
        grid:{ color:"#1f2937" }
    }
}
        }
    });


    /* ================= RECENT (UPDATED UI ONLY) ================= */
recentList.innerHTML = "";

filtered.slice().reverse().slice(0, 8).forEach(x => {

    const card = document.createElement("div");
    card.className = "recent-card-grid";

    const typeIcon = x.type === "image" ? "🖼" : "📝";
    const typeText = x.type === "image" ? "Image analysed" : "Text analysed";

    const badgeClass = x.label === "Real" ? "badge-real" : "badge-fake";
    const badgeIcon  = x.label === "Real" ? "✔" : "✖";

    card.innerHTML = `
        <div class="recent-left">
            <div class="recent-icon">${typeIcon}</div>

            <div>
                <div class="recent-title">${typeText}</div>
                <div class="recent-meta">
                    ${new Date(x.time).toLocaleTimeString()} • Credibility ${x.score}%
                </div>
            </div>
        </div>

        <div class="${badgeClass}">
            ${badgeIcon} ${x.label}
        </div>
    `;

    recentList.appendChild(card);
});
}


document.getElementById("dailyBtn").onclick = () => {
    currentPeriod = "today";

    document.getElementById("dailyBtn").classList.add("active");
    document.getElementById("weeklyBtn").classList.remove("active");

    render();
};

document.getElementById("weeklyBtn").onclick = () => {
    currentPeriod = "week";

    document.getElementById("weeklyBtn").classList.add("active");
    document.getElementById("dailyBtn").classList.remove("active");

    render();
};