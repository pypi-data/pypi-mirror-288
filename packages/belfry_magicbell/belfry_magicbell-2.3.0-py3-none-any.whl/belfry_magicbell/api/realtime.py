import json
import logging
import typing

from pydantic import ValidationError

from ..model.notification import WrappedCreatedNotificationBroadcast, WrappedNotification
from ..model.response import Response
from ._base import BaseAPI
from ._parsing import build_request_content, build_response

logger = logging.getLogger(__name__)


class RealtimeAPI(BaseAPI):
    """APIs to manage notifications in real-time"""

    async def create_notification(
        self,
        wrapped_notification: typing.Union[WrappedNotification, typing.Dict],
        idempotency_key: typing.Optional[str] = None,
    ) -> WrappedCreatedNotificationBroadcast:
        """Send a notification to one or multiple users, returning a `Notification`.
        Specify `idempotency_key` to prevent duplicate notifications.
        https://www.magicbell.com/docs/rest-api/idempotent-requests
        """
        return (
            await self.create_notification_detailed(wrapped_notification, idempotency_key)
        ).parsed

    async def create_notification_detailed(
        self,
        wrapped_notification: typing.Union[WrappedNotification, typing.Dict],
        idempotency_key: typing.Optional[str] = None,
    ) -> Response[WrappedCreatedNotificationBroadcast]:
        """Send a notification to one or multiple users, returning a `Response`.
        Specify `idempotency_key` to prevent duplicate notifications.
        https://www.magicbell.com/docs/rest-api/idempotent-requests
        """
        response = None
        try:
            response = await self.client.post(
                "/broadcasts",
                headers=self.configuration.get_general_headers(idempotency_key=idempotency_key),
                content=build_request_content(wrapped_notification),
            )
            try:
                wrapped_response = build_response(
                    response=response, out_type=WrappedCreatedNotificationBroadcast
                )
            except ValidationError:
                """
                Intentionally only catch ValidationError to handle the case where magicbell returns the response as a JSON string instead of JSON, otherwise exception keeps raising.

                Within the outer try except to ensure if the json.loads(...) throws again it is still caught.
                """
                logger.warning("Falling back to json loads for request")
                response.content = json.loads(response.content)
                wrapped_response = build_response(
                    response=response, out_type=WrappedCreatedNotificationBroadcast
                )
            return wrapped_response
        except Exception as e:
            if response:
                rc = response.content
            else:
                rc = "No response, failed during post"
            logger.warning(
                f"Error sending {wrapped_notification} to magicbell; response - {rc}", exc_info=True
            )
            raise e
