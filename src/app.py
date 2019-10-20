import json

import falcon

from src.maze import MazeGenerator
from src import PROJECT_DESCRIPTION, PROJECT_NAME, PROJECT_AUTHOR
from src.__version__ import VERSION
from src.helpers import serialise_maze


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
        maze = MazeGenerator(
            dimension=10, traps={"FireBridge": 2, "DynamicSpike": 2, "StaticSpike": 2}
        )
        maze.initialise_maze()
        base_maze = maze.maze
        object_maze = maze.object_maze

        resp.media = {
            "base_maze": serialise_maze(base_maze),
            "object_maze": serialise_maze(object_maze),
        }


api = falcon.API()

api.add_route("/", HealthcheckResource())
api.add_route("/generate", MazeGenerationResource())
