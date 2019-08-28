from db import Database
from auth import Auth
from aiohttp import web
from datetime import datetime, timedelta
import functools
import json


class Handler():
    def __init__(self):
        pass

    async def _json_content(self, content):
        content = await content.read()
        content = content.decode("utf-8")
        return json.loads(content)
    async def handle_register(self, request):
        try:
            data = await self._json_content(request.content)
            username = data["username"]
            password = Auth().generate_hash(data["password"])
            db.register(username, password)

        except Exception as err:
            return web.json_response(
                {
                    "status": "error",
                    "msg": str(err)
                },  status=400
            )

        else:
            return web.json_response(
                    {
                        "status":   "OK",
                        "msg":      "Account created successfully"
                    },  status=200
            )

    async def handle_login(self, request):
        try:
            data = await self._json_content(request.content)
            username = data["username"]
            password = Auth().generate_hash(data["password"])

        except Exception as err:
            return web.json_response(
                {
                    "status": "error",
                    "msg": str(err)
                },  status=400
            )

        else:
            if db.login(username, password):    # == true
                token = Auth().generate_token(username)
                user_id = db.get_user_id(username)
                expiration_date = datetime.now() + timedelta(hours=1)

                db.add_token(user_id, token, expiration_date)

                return web.json_response(
                    {
                        "status":   "OK",
                        "token":    token,
                        "user_id":  user_id
                    },  status=200
                )

            else:
                return web.json_response(
                    {
                        "status":   "error",
                        "msg":      "Authorization failed"
                    },  status=401
                )

    async def handle_create_note(self, request):
        try:
            data = await self._json_content(request.content)
            title = data["title"]
            content = data["content"]
            user_id = db.get_user_id(data["username"])
            token = data["token"]

        except Exception as err:
            return web.json_response(
                {
                    "status":   "error",
                    "msg":      str(err)
                },  status=400
            )

        else:
            creation_date = datetime.now()
            token_expiration_date = db.get_token_expiration_date(token)
            if Auth().verify_token(token, token_expiration_date):
                db.create_note(title, creation_date, user_id, content)

                return web.json_response(
                    {
                        "status":   "ok",
                        "msg":      "note created successful"
                    },  status=200
                )

            else:
                return web.json_response(
                    {
                        "status":   "error",
                        "msg":      "Authorization failed"
                    },  status=401
                )

    async def handle_get_notes_list(self, request):
        try:
            data = await self._json_content(request.content)
            user_id = db.get_user_id(data["username"])
            token = data["token"]
            token_expiration_date = db.get_token_expiration_date(token)

        except Exception as err:
            return web.json_response(
                {
                    "status":   "error",
                    "msg":      str(err)
                },  status=400
            )

        else:
            if Auth().verify_token(token, token_expiration_date):
                notes = db.get_notes_list(user_id)
                for note in notes:
                    note["creation_date"] = note["creation_date"].timestamp()
                return web.json_response(
                    {
                        "status":   "OK",
                        "notes":    notes
                    }, status=200
                )

            else:
                db.remove_token(token)
                return web.json_response(
                    {
                        "status":   "error",
                        "msg":      "Authorization failed"
                    },  status=401
                )

    async def handle_get_note(self, request):
        try:
            data = await self._json_content(request.content)
            note_id = data["note_id"]
            user_id = db.get_user_id(data["username"])
            token = data["token"]
            token_expiration_date = db.get_token_expiration_date(token)

        except Exception as err:
            return web.json_response(
                {
                    "status": "error",
                    "msg": str(err)
                }, status=400
            )

        else:
            if Auth().verify_token(token, token_expiration_date):
                note = db.get_note(note_id, user_id)
                note["creation_date"] = note["creation_date"].timestamp()
                return web.json_response(
                    {
                        "status":   "OK",
                        "note":     note
                    }, status=200
                )

            else:
                db.remove_token(token)
                return web.json_response(
                    {
                        "status":   "error",
                        "msg":      "Authorization failed"
                    }, status=401
                )
    async def handle_remove_note(self, request):
        try:
            data = await self._json_content(request.content)
            note_id = data["note_id"]
            user_id = db.get_user_id(data["username"])
            token = data["token"]
            token_expiration_date = db.get_token_expiration_date(token)
        except Exception as err:
            return web.json_response(
                {
                    "status":   "error",
                    "msg":      str(err)
                }, status=400
            )
        else:
            if Auth().verify_token(token, token_expiration_date):
                db.remove_note(note_id, user_id)
                return web.json_response(
                    {
                        "status":   "OK",
                        "msg":      "note removed successfully"
                    },  status=200
                )
            else:
                db.remove_token(token)
                return web.json_response(
                    {
                        "status":   "error",
                        "msg":      "Authorization failed"
                    }, status=401
                )

    async def handle_modify_note(self, request):
        try:
            data = await self._json_content(request.content)
            note_id = data["note_id"]
            user_id = db.get_user_id(data["username"])
            token = data["token"]
            token_expiration_date = db.get_token_expiration_date(token)
            title = data["title"]
            content = data["content"]

        except Exception as err:
            return web.json_response(
                {
                    "status":   "error",
                    "msg":      str(err)
                },  status=400
            )

        else:
            if Auth().verify_token(token, token_expiration_date):
                db.modify_note(note_id, user_id, title, content)
                note = db.get_note(note_id, user_id)
                note["creation_date"] = note["creation_date"].timestamp()

                return web.json_response(
                    {
                        "status":   "OK",
                        "msg":      "Note modified successfully",
                        "note":     note
                    },  status=200
                )

            else:
                db.remove_token(token)
                return web.json_response(
                    {
                        "status":   "error",
                        "msg":      "Authorization failed"
                    },  status=401
                )

db = Database("localhost", "root", "3dSynN3K", "pyNotes")
handler = Handler()

app = web.Application()
app.add_routes([
    web.put("/modifyNote", handler.handle_modify_note),
    web.post("/getNote", handler.handle_get_note),
    web.post("/createNote", handler.handle_create_note),
    web.post("/getNotesList", handler.handle_get_notes_list),
    web.delete("/removeNote", handler.handle_remove_note),
    web.post("/login", handler.handle_login),
    web.post("/register", handler.handle_register)
])

if __name__ == "__main__":
    web.run_app(app)
