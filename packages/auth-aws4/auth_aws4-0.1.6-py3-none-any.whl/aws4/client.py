from __future__ import annotations

from datetime import datetime, timezone

import aws4


class HttpxAWS4Auth:
    """AWS4-HMAC auth implementation for httpx."""

    def __init__(
        self,
        key_pair: aws4.key_pair.KeyPair,
        service: str,
        region: str,
        auth_schema: aws4.AuthSchema = aws4.AWSAuthSchema,
    ) -> None:
        self.key_pair = key_pair
        self.service = service
        self.region = region
        self.schema = auth_schema

    def __call__(self, request: "httpx.Request") -> "httpx.Request":  # noqa: UP037, F821
        """Generate authorization header."""
        dt = datetime.now(tz=timezone.utc)
        request.headers[f"{self.schema.header_prefix}-date"] = aws4.to_amz_date(dt)
        request.headers["host"] = request.url.netloc.decode("utf-8")

        body = request.content.decode("utf-8")
        if body:
            request.headers["Content-Length"] = str(len(body))

        aws4.sign_request(
            self.service,
            str(request.method),
            request.url,
            self.region,
            request.headers,
            body,
            self.key_pair.access_key_id,
            self.key_pair.secret_access_key,
            dt,
            self.schema,
        )

        return request

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, HttpxAWS4Auth) and other.key_pair == self.key_pair
