const cards = document.querySelectorAll(".location-card");

cards.forEach(card => {
    card.addEventListener("click", () => {
        cards.forEach(c => c.classList.remove("active"));
        card.classList.add("active");
    });
});

// Button loading effect
document.querySelector("form").addEventListener("submit", function () {
    const btn = document.querySelector(".run-btn");
    btn.innerHTML = "Analyzing...";
    btn.style.opacity = "0.7";
});

// GSAP animations
gsap.from(".hero h1", {
    y: -40,
    opacity: 0,
    duration: 1
});

gsap.from(".tool-box", {
    y: 50,
    opacity: 0,
    duration: 1.2
});

// Create floating SERP cards
const bg = document.querySelector(".serp-bg");

for (let i = 0; i < 20; i++) {
    const card = document.createElement("div");
    card.className = "serp-card";

    card.style.left = Math.random() * 100 + "vw";
    card.style.top = Math.random() * 100 + "vh";
    card.style.animationDuration = (10 + Math.random() * 10) + "s";

    bg.appendChild(card);
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const loader = document.getElementById("loader");

    form.addEventListener("submit", function () {
        loader.classList.remove("hidden");
    });
});