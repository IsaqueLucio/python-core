"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Learning FastAPI: Exercise 1",
    description="Basic tests (no database)",
    version="0.1.0",
)


# TODO: define NoteCreate (input model)
# fields: text (str)
class NoteCreate(BaseModel):
    text: str

# TODO: create the `notes` list (starts empty)
notes: list[dict] = []

# TODO: POST "/notes" endpoint
# append {"id": len(notes) + 1, "text": text} to notes, return it
@app.post("/notes")
def post_notes(note: NoteCreate):
    new_note = {
        "id": len(notes) + 1,
        "text": note.text
    }
    notes.append(new_note)
    return new_note

# TODO: GET "/notes" endpoint
# return the full notes list
@app.get("/notes")
def get_notes():
    return notes

# TODO: GET "/notes/{note_id}" endpoint
# return the matching note, or raise HTTPException(404, "Note not found")
@app.get("/notes/{note_id}")
def get_notes_id(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")
    