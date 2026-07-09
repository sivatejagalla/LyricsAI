from flask import Flask, render_template, request, redirect, send_file

from analyzer import analyze_lyrics

from database import (
    create_database,
    save_analysis,
    get_history,
    search_history,
    delete_song,
    favorite_song,
    get_favorites,
    get_dashboard,
    get_song,
    get_genre_stats,
    get_mood_stats
)

from export_utils import (
    export_pdf,
    export_json,
    export_txt
)

app = Flask(__name__)

create_database()


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        lyrics = request.form["lyrics"]

        result = analyze_lyrics(lyrics)

        save_analysis(result)

    return render_template(
        "index.html",
        result=result
    )


@app.route("/history")
def history():

    keyword = request.args.get("search")

    if keyword:
        history = search_history(keyword)
    else:
        history = get_history()

    return render_template(
        "history.html",
        history=history
    )


@app.route("/song/<int:song_id>")
def song_details(song_id):

    song = get_song(song_id)

    return render_template(
        "song_details.html",
        song=song
    )


@app.route("/delete/<int:song_id>")
def delete(song_id):

    delete_song(song_id)

    return redirect("/history")


@app.route("/favorite/<int:song_id>")
def favorite(song_id):

    favorite_song(song_id)

    return redirect("/history")


@app.route("/favorites")
def favorites():

    songs = get_favorites()

    return render_template(
        "favorites.html",
        songs=songs
    )


@app.route("/dashboard")
def dashboard():

    stats = get_dashboard()

    genre_stats = get_genre_stats()

    mood_stats = get_mood_stats()

    return render_template(
        "dashboard.html",
        stats=stats,
        genre_stats=genre_stats,
        mood_stats=mood_stats
    )


@app.route("/about")
def about():

    return render_template("about.html")


# ---------- EXPORT ROUTES ----------

@app.route("/export/pdf/<int:song_id>")
def export_song_pdf(song_id):

    song = get_song(song_id)

    filepath = export_pdf(song)

    return send_file(filepath, as_attachment=True)


@app.route("/export/json/<int:song_id>")
def export_song_json(song_id):

    song = get_song(song_id)

    filepath = export_json(song)

    return send_file(filepath, as_attachment=True)


@app.route("/export/txt/<int:song_id>")
def export_song_txt(song_id):

    song = get_song(song_id)

    filepath = export_txt(song)

    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)