const searchBox = document.getElementById("searchBox")
const categoryBox = document.getElementById("categoryBox")
const newsContainer = document.getElementById("newsContainer")
const alertBox = document.getElementById("alertBox")
const badge = document.getElementById("liveBadge")

let allNews = []

async function loadNews() {

    newsContainer.innerHTML = "<div class='loader'>Loading live news...</div>"

    try {

        const category = categoryBox.value || ""

        const res = await fetch(`/api/live-news?category=${category}`)
        const data = await res.json()

        allNews = Array.isArray(data) ? data : []

        render()
        showAlerts()
        flashBadge()

    } catch (e) {
        console.log(e)
        newsContainer.innerHTML = "<p>Unable to load news</p>"
    }
}

function render(){

    const search = (searchBox.value || "").toLowerCase()
    newsContainer.innerHTML = ""

    if(!allNews.length){
        newsContainer.innerHTML = "<p>No news available</p>"
        return
    }

    allNews
    .filter(n => n.title.toLowerCase().includes(search))
    .forEach(n => {

        const div = document.createElement("div")
        div.className = "newsCard"

        const color = n.label === "Real" ? "#19b36b" : "#e53935"

        div.innerHTML = `
            <h4>${n.title}</h4>
            <p>Source: ${n.source}</p>

            <p class="${n.label === 'Real' ? 'real':'fake'}">
                ${n.label} (${n.score}%)
            </p>

            <div class="bar">
                <div class="fill" style="width:${n.score}%; background:${color}"></div>
            </div>

            <br>
            <a href="${n.url}" target="_blank">Read More →</a>
        `

        newsContainer.appendChild(div)
    })
}

function showAlerts(){

    alertBox.innerHTML = ""

    allNews
    .filter(n => n.label === "Fake" && n.score > 70)
    .slice(0,5)
    .forEach(n=>{
        alertBox.innerHTML += `⚠ ${n.title}<br>`
    })
}

function flashBadge(){
    badge.style.background = "#00c853"
    setTimeout(()=> badge.style.background="#ff3b3b", 400)
}

searchBox.oninput = render
categoryBox.onchange = loadNews

loadNews()
setInterval(loadNews, 30000)