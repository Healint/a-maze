import logging
import falcon

from falcon_cors import CORS

from src.maze import MazeGenerator
from src import PROJECT_DESCRIPTION, PROJECT_NAME, PROJECT_AUTHOR
from src.__version__ import VERSION
from src.helpers import serialise_maze

logger = logging.getLogger(__name__)


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

        # parse req
        raw_json = req.media
        try:
            req_dimension = raw_json["dimension"]
        except KeyError:
            raise falcon.HTTPBadRequest(
                "You need to provide an integer as maze dimension. "
            )

        try:
            req_traps = raw_json["traps"]
        except KeyError:
            logger.warning("No traps config past to the generator, taking the default")
            req_traps = {"FireBridge": 2, "DynamicSpike": 2, "StaticSpike": 2}

        maze = MazeGenerator(dimension=req_dimension, traps=req_traps)

        maze.initialise_maze()

        base_maze = maze.maze
        object_maze = maze.object_maze

        resp.media = {
            "base_maze": serialise_maze(base_maze),
            "object_maze": serialise_maze(object_maze),
            "user_position_x": base_maze.entrance.x,
            "user_position_y": base_maze.entrance.y
        }


cors = CORS(
    allow_all_headers=True,
    allow_all_methods=True,
    allow_all_origins=True
)
cors_middleware = cors.middleware

api = falcon.API(middleware=[cors_middleware])

api.add_route("/", HealthcheckResource())
api.add_route("/generate", MazeGenerationResource())
