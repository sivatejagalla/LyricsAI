const genreData = JSON.parse(
    document.getElementById("genre-data").textContent
);

const moodData = JSON.parse(
    document.getElementById("mood-data").textContent
);

// Genre Chart

new Chart(document.getElementById("genreChart"), {

    type: "pie",

    data: {

        labels: genreData.map(item => item.genre),

        datasets: [{

            label: "Genres",

            data: genreData.map(item => item.count)

        }]

    }

});

// Mood Chart

new Chart(document.getElementById("moodChart"), {

    type: "bar",

    data: {

        labels: moodData.map(item => item.mood),

        datasets: [{

            label: "Songs",

            data: moodData.map(item => item.count)

        }]

    }

});