from aiohttp import web
from db import Database
from datetime import datetime
import functools
import json


class Handler():
    def __init__(self):
        pass

    async def _json_content(self, content):
        content = await content.read()
        content = content.decode("utf-8")
        return json.loads(content)

    async def handle_create_note(self, request):
        try:
            data = await self._json_content(request.content)
            title = data["title"]
            content = data["content"]
            author_id = data["author_id"]   # TODO: Authorization

        except Exception as e:
            return web.json_response(
                {"status": "error", "msg": str(e)}, status=400
            )

        else:
            creation_date = datetime.now()
            db.create_note(title, creation_date, author_id, content)

            return web.json_response(
                {"status": "ok", "msg": "note created successful"}, status=200
            )

    async def handle_get_notes_list(self, request):
        try:
            data = await self._json_content(request.content)
            notes = db.get_notes_list(data["author_id"])

        except Exception as e:
            return web.json_response(
                {"status": "error", "msg": str(e)}, status=400
            )

        else:
            for note in notes:
                note["creation_date"] = note["creation_date"].timestamp()
            return web.json_response(
                {"status": "OK", "notes": notes}, status=200
            )

db = Database("localhost", "root", "3dSynN3K", "pyNotes")
handler = Handler()

app = web.Application()
app.add_routes([
    web.post("/createNote", handler.handle_create_note),
    web.post("/getNotesList", handler.handle_get_notes_list)
])

if __name__ == "__main__":
    web.run_app(app)
