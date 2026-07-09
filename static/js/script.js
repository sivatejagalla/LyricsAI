document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    const button = document.getElementById("analyzeBtn");

    if (form) {

        form.addEventListener("submit", function () {

            button.disabled = true;

            button.innerHTML = "⏳ Analyzing Lyrics...";

        });

    }

});