import asyncio
import sys

from blib import AsyncTransport

from ..enums import AppType, StatusCode
from ..error import GeminiError, TooManyRedirectsError
from ..message import Request, Response
from ..misc import BaseApp, Url


REDIR_STATUS = (
	StatusCode.TEMPORARY_REDIRECT,
	StatusCode.PERMANENT_REDIRECT
)

SUCCESS_STATUS = (
	StatusCode.SUCCESS,
	*REDIR_STATUS
)


class AsyncClient(BaseApp):
	"Client for the Gemini protocol"

	apptype: AppType = AppType.CLIENT

	timeout: int
	"Time in seconds to wait before giving up on connecting or reading data"


	def __init__(self, name: str = "Default", timeout: int = 30, redirect_limit: int = 5) -> None:
		"""
			Create a new client object

			:param name: Internal name of the client
			:param timeout: Time in seconds to wait before giving up
			:param redirect_limit: Number of times a request can redirect before raising an
				exception
		"""

		BaseApp.__init__(self, name, timeout = timeout)

		self.redirect_limit: int = redirect_limit
		"Number of times a request can redirect before raising an exception"


	async def request(self,
					url: Url | str,
					follow_redirects: bool = True,
					raise_on_error: bool = False) -> Response:

		"""
			Create a new request and send it to a server

			:param url: Url of the resource to fetch
			:param follow_redirects: If a redirect is returned (30 or 31), send a new request with
				the redirect url until the final request is found
			:param raise_on_error: If an error code is returned, raise a :class:`GeminiError`
		"""

		return await self.send_request(Request(url))


	async def send_request(self,
						request: Request,
						follow_redirects: bool = True,
						raise_on_error: bool = False) -> Response:

		"""
			Send a request to a server

			:param request: The request to be sent
			:param follow_redirects: If a redirect is returned (30 or 31), send a new request with
				the redirect url until the final request is found
			:param raise_on_error: If an error code is returned, raise a :class:`GeminiError`
		"""

		reader, writer = await asyncio.open_connection(
			host = request.url.domain,
			port = request.url.port,
			ssl = self.ssl_context,
			ssl_handshake_timeout = self.timeout,
			ssl_shutdown_timeout = self.timeout
		)

		redir_count = 0
		transport = AsyncTransport(reader, writer, self.timeout)
		await transport.write(request.build())

		response = await Response.from_transport(transport)
		response.url = request.url
		response.origin_url = request.url

		if raise_on_error and response.status not in SUCCESS_STATUS:
			raise GeminiError(response.status, response.meta)

		if not follow_redirects and response.status in REDIR_STATUS:
			return response

		while response.status in REDIR_STATUS:
			redir_count += 1

			if redir_count >= 5:
				raise TooManyRedirectsError(redir_count)

			response = await self.request(response.meta, False, raise_on_error)
			response.origin_url = request.url

		return response
