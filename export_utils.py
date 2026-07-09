from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import json
import os

EXPORT_FOLDER = "exports"

os.makedirs(EXPORT_FOLDER, exist_ok=True)


def export_pdf(song):

    filename = f"{song['title'].replace(' ', '_')}.pdf"

    filepath = os.path.join(EXPORT_FOLDER, filename)

    document = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>LyricsAI Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Title:</b> {song['title']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Artist:</b> {song['artist']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Album:</b> {song['album']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Release Year:</b> {song['release_year']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Genre:</b> {song['genre']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Mood:</b> {song['mood']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Emotion:</b> {song['emotion']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Theme:</b> {song['theme']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Language:</b> {song['language']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Confidence:</b> {song['confidence']}", styles["BodyText"]))

    story.append(Paragraph("<br/><b>Summary</b>", styles["Heading2"]))

    story.append(Paragraph(song["summary"], styles["BodyText"]))

    document.build(story)

    return filepath


def export_json(song):

    filename = f"{song['title'].replace(' ', '_')}.json"

    filepath = os.path.join(EXPORT_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:

        json.dump(dict(song), file, indent=4)

    return filepath


def export_txt(song):

    filename = f"{song['title'].replace(' ', '_')}.txt"

    filepath = os.path.join(EXPORT_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:

        for key, value in dict(song).items():

            file.write(f"{key}: {value}\n")

    return filepath