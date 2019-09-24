
import numpy as np

from . import Behaviour


class LightToCamera(Behaviour):
    """Move the light to the same position as the camera so that the objects
    are always lit."""
    def __init__(self, offset=[0, 0, 0]):
        self._offset = offset

    def behave(self, params):
        newpos = params.scene.camera_position + self._offset
        if np.allclose(newpos, params.scene.light):
            return

        params.scene.light = newpos
        params.refresh = True


class AddObjectsSequentially(Behaviour):
    """Add a series of objects to a scene at constant time intervals.

    Arguments
    ---------
        objects: A list of Renderable objects
        interval: The interval between additions of objects in ticks
    """
    def __init__(self, objects, interval=30):
        self._objects = objects
        self._interval = interval

        self._ticks = interval
        self._index = len(objects)

    def behave(self, params):
        self._ticks += 1
        if self._ticks > self._interval:
            self._ticks = 0
            if self._index >= len(self._objects):
                for o in self._objects:
                    params.scene.remove(o)
                self._index = 0
            params.scene.add(self._objects[self._index])
            self._index += 1
            params.refresh = True


class CycleThroughObjects(Behaviour):
    """Add a set of objects to the scene removing the ones previously added.

    Arguments
    ---------
        objects: A list of lists of Renderable objects
        interval: The interval between additions and removals in ticks
    """
    def __init__(self, objects, interval=30):
        self._objects = objects
        self._interval = interval

        self._ticks = interval
        self._object = -1

    def behave(self, params):
        self._ticks += 1
        if self._ticks > self._interval:
            self._ticks = 0
            for o in self._objects[self._object]:
                params.scene.remove(o)
            self._object = (self._object + 1) % len(self._objects)
            for i in self._objects[self._object]:
                params.scene.add(o)
            params.refresh = True
