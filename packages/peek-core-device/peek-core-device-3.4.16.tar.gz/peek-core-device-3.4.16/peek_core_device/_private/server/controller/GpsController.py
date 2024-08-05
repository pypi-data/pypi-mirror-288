import logging
from collections import namedtuple
from datetime import datetime
from typing import Optional

import pytz

from peek_core_device.tuples.DeviceGpsLocationTuple import (
    DeviceGpsLocationTuple,
)
from peek_plugin_base.storage.RunPyInPg import runPyInPg
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from twisted.internet.defer import Deferred
from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from vortex.DeferUtil import callMethodLater
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.DeferUtil import vortexLogFailure
from vortex.TupleAction import TupleActionABC
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleActionProcessor import TupleActionProcessorDelegateABC
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

from peek_core_device._private.server.controller.NotifierController import (
    NotifierController,
)
from peek_core_device._private.tuples.UpdateDeviceGpsLocationTupleAction import (
    UpdateDeviceGpsLocationTupleAction,
)
from peek_core_device.tuples.DeviceGpsLocationTuple import (
    DeviceGpsLocationTuple,
)
from peek_plugin_base.LoopingCallUtil import peekCatchErrbackWithLogger
from peek_plugin_base.storage.RunPyInPg import runPyInPg

logger = logging.getLogger(__name__)
DeviceLocationTuple = namedtuple(
    "DeviceLocationTuple",
    ["deviceToken", "latitude", "longitude", "updatedDate"],
)
TimezoneSetting = namedtuple("TimezoneSetting", ["timezone"])


class GpsController(TupleActionProcessorDelegateABC):
    INSERT_SECONDS = 120.0

    def __init__(
        self,
        dbSessionCreator,
        tupleObservable: TupleDataObservableHandler,
        notifierController: NotifierController,
    ):
        self._dbSessionCreator = dbSessionCreator
        self._tupleObservable = tupleObservable
        self._notifierController = notifierController

        self._insertQueue = []
        self._insertLoopingCall = None

    def start(self):
        wrappedCall = peekCatchErrbackWithLogger(logger)(self._poll)
        self._insertLoopingCall = LoopingCall(wrappedCall)
        d = self._insertLoopingCall.start(self.INSERT_SECONDS)
        d.addErrback(vortexLogFailure, logger)

    def shutdown(self):
        if self._insertLoopingCall and self._insertLoopingCall.running:
            self._insertLoopingCall.stop()

        self._insertLoopingCall = None
        self._notifierController = None
        self._insertQueue = []

    def processTupleAction(self, tupleAction: TupleActionABC) -> Deferred:
        if isinstance(tupleAction, UpdateDeviceGpsLocationTupleAction):
            self._insertQueue.append(tupleAction)
            return []

    @inlineCallbacks
    def _poll(self):
        if not self._insertQueue:
            return

        self._insertQueue, toProcess = [], self._insertQueue

        startTime = datetime.now(pytz.UTC)
        yield runPyInPg(
            logger,
            self._dbSessionCreator,
            self._insertGpsLocation,
            None,
            toProcess,
        )
        logger.debug(
            "Inserted %s GPS Locations in %s",
            len(toProcess),
            datetime.now(pytz.UTC) - startTime,
        )

        self._notifyTuple(toProcess)

    @callMethodLater
    def _notifyTuple(self, queue: list[UpdateDeviceGpsLocationTupleAction]):
        for item in queue:
            self._tupleObservable.notifyOfTupleUpdate(
                TupleSelector(
                    DeviceGpsLocationTuple.tupleName(),
                    dict(deviceToken=item.deviceToken),
                )
            )

            self._notifierController.notifyDeviceGpsLocation(
                item.deviceToken,
                item.latitude,
                item.longitude,
                updatedDate=item.datetime,
            )

        self._notifierController.notifyAllDeviceGpsLocation()

    @classmethod
    def _insertGpsLocation(
        cls, plpy, actionTuples: list[UpdateDeviceGpsLocationTupleAction]
    ) -> None:
        plan = plpy.prepare(
            """
            INSERT INTO core_device."GpsLocation"
             ("deviceToken", "latitude", "longitude", "updatedDate")
             VALUES
             ($1, $2, $3, $4)
             ON CONFLICT ("deviceToken")
             DO 
             UPDATE SET
                "latitude" = $2,
                "longitude" = $3,
                "updatedDate" = $4
                ;
            """,
            ["text", "float", "float", "timestamp with time zone"],
        )
        for item in actionTuples:
            plpy.execute(
                plan,
                [
                    item.deviceToken,
                    item.latitude,
                    item.longitude,
                    item.datetime,
                ],
            )

        plan = plpy.prepare(
            """
            INSERT INTO core_device."GpsLocationHistory"
             ("deviceToken", "latitude", "longitude", "loggedDate")
             VALUES
             ($1, $2, $3, $4);
            """,
            ["text", "float", "float", "timestamp with time zone"],
        )
        for item in actionTuples:
            plpy.execute(
                plan,
                [
                    item.deviceToken,
                    item.latitude,
                    item.longitude,
                    item.datetime,
                ],
            )
