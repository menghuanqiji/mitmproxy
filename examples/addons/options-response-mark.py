"""
Add a new mitmproxy option.

Usage:

    mitmproxy -s options-response-mark.py --set response_mark_name=code --set response_mark_value=!200
"""

from mitmproxy import ctx

MARK_NAME = "response_mark_name"
MARK_VALUE = "response_mark_value"


class ResponseMarker:

    def load(self, loader):
        loader.add_option(
            name=MARK_NAME,
            typespec=str,
            default="",
            help="marker name on responses",
        )
        loader.add_option(
            name=MARK_VALUE,
            typespec=str,
            default="",
            help="marker value on responses",
        )

    def response(self, flow):
        mark_name: str = ctx.options.__getattr__(MARK_NAME)
        mark_value: str = ctx.options.__getattr__(MARK_VALUE)

        if mark_name is None:
            return False

        if self.is_marked(flow, mark_name, mark_value):
            # 🏴
            flow.marked = ":scotland:"

    def is_marked(self, flow, mark_name: str, mark_value: str) -> bool:
        negative: bool = False
        if mark_value is not None and mark_value.startswith("!"):
            mark_value = mark_value[1:]
            negative = True
        if negative ^ self.is_match(flow, mark_name, mark_value):
            return True
        else:
            return False
    def is_match(self, flow, mark_name: str, mark_value: str) -> bool:
        if flow.response is None:
            return False

        if not flow.response.headers.get("Content-Type", "").startswith("application/json"):
            return False

        json = flow.response.json()
        if not isinstance(json, dict):
            return False

        value = json.get(mark_name)
        if value is None:
            return False
        value = str(value)

        if mark_value == value:
            return True

        return False

addons = [ResponseMarker()]
