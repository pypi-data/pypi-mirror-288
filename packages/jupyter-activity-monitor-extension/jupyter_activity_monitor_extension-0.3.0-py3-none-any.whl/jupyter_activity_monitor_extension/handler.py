from jupyter_server.base.handlers import JupyterHandler, json_errors
import json
from datetime import datetime, timezone
from tornado import gen, web
from jupyter_activity_monitor_extension.docker_sidecar_check import (
    check_if_sidecars_idle,
)
import os

first_request_time = None


class IdleHandler(JupyterHandler):
    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self):
        # record the time when the request was first made to the endpoint
        global first_request_time
        if first_request_time is None:
            first_request_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fz")
        sm = self.settings["session_manager"]
        tm = self.terminal_manager
        sessions = yield sm.list_sessions()
        terminals = tm.list()
        largest_last_activity = self.get_last_active_timestamp(
            sessions, terminals, first_request_time
        )
        # check if any running sidecars are broadcasting as not idle
        all_sidecars_idle = check_if_sidecars_idle()
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fz")
        if (largest_last_activity is not None) and all_sidecars_idle:
            response = {"lastActiveTimestamp": largest_last_activity}
        elif not all_sidecars_idle:
            response = {"lastActiveTimestamp": current_time}
        else:
            response = {}
        self.finish(json.dumps(response))

    def get_last_active_timestamp(self, sessions, terminals, first_request_time):

        session_last_activity_time = max(
            (
                datetime.strptime(
                    session["kernel"]["last_activity"], "%Y-%m-%dT%H:%M:%S.%fz"
                )
                for session in sessions
            ),
            default=datetime.strptime(first_request_time, "%Y-%m-%dT%H:%M:%S.%fz"),
        )
        terminals_last_activity_time = max(
            (
                datetime.strptime(terminal["last_activity"], "%Y-%m-%dT%H:%M:%S.%fz")
                for terminal in terminals
            ),
            default=datetime.strptime(first_request_time, "%Y-%m-%dT%H:%M:%S.%fz"),
        )

        max_last_activity_time = max(
            session_last_activity_time, terminals_last_activity_time
        )
        return max_last_activity_time.strftime("%Y-%m-%dT%H:%M:%S.%fz")
