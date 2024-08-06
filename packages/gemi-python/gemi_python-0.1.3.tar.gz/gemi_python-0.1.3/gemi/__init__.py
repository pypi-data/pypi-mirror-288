__software__ = "Gemi"
__version_info__ = (0, 1, 3)
__version__ = ".".join(str(v) for v in __version_info__)
__author__ = "Zoey Mae"
__homepage__ = "https://git.barkshark.xyz/barkshark/gemi"

import mimetypes
mimetypes.add_type("text/gemini", ".gmi", strict = True)

from .client import AsyncClient
from .enums import AppType, OutputFormat, StatusCode
from .error import BodyTooLargeError, GeminiError, ParsingError, TooManyRedirectsError
from .message import Message, Request, Response
from .misc import BaseApp, SslContext, Url, resolve_path
from .server import AsyncServer, Router, BaseRoute, Route, FileRoute, route

from .document import (
	Document,
	Element,
	Header,
	Link,
	ListItem,
	Preformatted,
	Quote,
	Text
)
