// ================= ELEMENTS =================// 
const form = document.getElementById("analyzeForm");

const bigResult = document.getElementById("bigResult");
const explanation = document.getElementById("explanation");
const credibilityScore = document.getElementById("credibilityScore");
const fill = document.getElementById("confidenceFill");
const icon = document.getElementById("resultIcon");

const textToggle = document.getElementById("textToggle");
const imageToggle = document.getElementById("imageToggle");
const textInput = document.getElementById("textInput");
const imageInput = document.getElementById("imageInput");

const imagePreview = document.getElementById("imagePreview");
const imagePreviewContainer = document.getElementById("imagePreviewContainer");
const retryBtn = document.getElementById("retryBtn");


// ================= TOGGLE =================
textToggle.onclick = () => {
    textInput.style.display = "block";
    imageInput.style.display = "none";
};

imageToggle.onclick = () => {
    textInput.style.display = "none";
    imageInput.style.display = "block";
};


// ================= IMAGE PREVIEW =================
imageInput.addEventListener("change", () => {

    const file = imageInput.files[0];

    if (!file) {
        imagePreviewContainer.style.display = "none";
        return;
    }

    imagePreview.src = URL.createObjectURL(file);
    imagePreviewContainer.style.display = "block";
});


// ================= RESET (FIXED BUG HERE) =================
retryBtn.onclick = () => {

    form.reset();

    textInput.style.display = "block";
    imageInput.style.display = "none";

    imagePreviewContainer.style.display = "none";
    imagePreview.src = "";

    // ✅ remove old colors + animation
    icon.className = "result-icon";
    icon.innerText = "•";

    bigResult.innerText = "Result will appear here";
    credibilityScore.innerText = "-";
    fill.style.width = "0%";
    explanation.innerHTML = "";
};


// ================= ANALYSIS DETAILS =================
function showDetails(result){

    explanation.innerHTML = "";

    const rows = [
        `Result is ${result.label.toUpperCase()}`,
        `Model is ${result.score}% confident about this prediction`,
        result.explanation || "Pattern analysis completed successfully"
    ];

    rows.forEach(text => {

        const div = document.createElement("div");
        div.className = "analysis-row";

        div.innerHTML = `
            <span class="tick">✓</span>
            <span>${text}</span>
        `;

        explanation.appendChild(div);
    });
}


// ================= SUBMIT =================
form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const data = new FormData(form);

    // ✅ animated loader
    icon.className = "result-icon loading-spin";
    icon.innerText = "";

    bigResult.innerText = "Analyzing...";
    credibilityScore.innerText = "-";
    fill.style.width = "0%";
    explanation.innerHTML = "";

    // send request immediately
    const resPromise = fetch("/api/analyze", {
        method: "POST",
        body: data
    });

// wait minimum 5 seconds + response
    const [res] = await Promise.all([
        resPromise,
        new Promise(r => setTimeout(r, 5000))
    ]);

    const result = await res.json();


    // remove loader animation
    icon.className = "result-icon";

    if (result.label === "Real") {
        icon.innerText = "✓";
        icon.classList.add("real-bg");
        bigResult.innerText = "REAL";
    } else {
        icon.innerText = "✕";
        icon.classList.add("fake-bg");
        bigResult.innerText = "FAKE";
    }

    credibilityScore.innerText = `Confidence: ${result.score}%`;
    fill.style.width = result.score + "%";
    fill.className = "confidence-fill " + (result.label === "Real" ? "real" : "fake");

    showDetails(result);
});