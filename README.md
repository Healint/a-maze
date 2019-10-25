# a-maze
A project for the engineering challenge in Healint.

Team Mate: Yikun & Yingdan

This document is outdated, I will find a time to polish a thing or
two when I have time.

The project itself is more or less completed. Running

```
gunicorn src.app:api
```

would give you a working maze generation endpoint.


# Iteration designs

v1:

- Support the basic mechanics of a maze.
- Support validation checking (Maze is solvable)

v2:

- Support Three different types of traps
    * static spike trap
    * dynamic spike trap
    * dynamic fire bridge (instance death)

- Support the generation of a treasure
    * armor - able to block static and dynamic spike traps

v3:

- Support the generation of Keys - Doors pairs to block path / guard treasure
- Support additional treasures guarded with keys
    * Shovel - allows to destroy walls a few times
