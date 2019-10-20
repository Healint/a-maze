import falcon

from src import PROJECT_DESCRIPTION, PROJECT_NAME, PROJECT_AUTHOR
from src.__version__ import VERSION


class HealthcheckResource:
    def on_get(self, req, resp):
        message = {
            "project_name": PROJECT_NAME,
            "project_description": PROJECT_DESCRIPTION,
            "author": PROJECT_AUTHOR,
            "version": VERSION,
        }

        resp.media = message


class MazeGenerationResource:
    def on_post(self, req, resp):
        resp.media = {"message": "successfully generated maze"}


api = falcon.API()

api.add_route("/", HealthcheckResource())
api.add_route("/generate", MazeGenerationResource())
