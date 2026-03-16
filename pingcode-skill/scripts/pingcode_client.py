#!/usr/bin/env python3
"""Minimal PingCode API client for Codex skills."""

from __future__ import annotations

import os
from typing import Any

import httpx


class PingCodeError(RuntimeError):
    """Raised when PingCode API returns an error."""


class PingCodeClient:
    def __init__(
        self,
        base_url: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        access_token: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("PINGCODE_BASE_URL") or "https://open.pingcode.com").rstrip("/")
        self.client_id = client_id or os.getenv("PINGCODE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("PINGCODE_CLIENT_SECRET")
        self.access_token = access_token or os.getenv("PINGCODE_ACCESS_TOKEN")
        self.timeout = timeout or float(os.getenv("PINGCODE_TIMEOUT", "15"))

    def get_access_token(self) -> str:
        if self.access_token:
            return self.access_token
        if not self.client_id or not self.client_secret:
            raise PingCodeError(
                "缺少鉴权信息。请设置 PINGCODE_ACCESS_TOKEN，或同时设置 PINGCODE_CLIENT_ID 和 PINGCODE_CLIENT_SECRET。"
            )

        response = httpx.get(
            f"{self.base_url}/v1/auth/token",
            params={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=self.timeout,
        )
        payload = self._parse_response(response)
        token = payload.get("access_token")
        if not token:
            raise PingCodeError(f"鉴权成功但响应中没有 access_token: {payload}")
        self.access_token = token
        return token

    def list_projects(self, identifier: str | None = None) -> dict[str, Any]:
        params = {"identifier": identifier} if identifier else None
        return self._request("GET", "/v1/project/projects", params=params)

    def get_task(self, identifier: str) -> dict[str, Any]:
        return self._request("GET", "/v1/project/work_items", params={"identifier": identifier})

    def create_project(
        self,
        name: str,
        identifier: str,
        project_type: str = "scrum",
        description: str = "",
        visibility: str = "private",
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            "/v1/project/projects",
            json={
                "name": name,
                "identifier": identifier,
                "type": project_type,
                "description": description,
                "visibility": visibility,
            },
        )

    def create_work_item(
        self,
        project_id: str,
        title: str,
        type_id: str = "task",
        description: str = "",
        parent_id: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "project_id": project_id,
            "title": title,
            "type_id": type_id,
            "description": description,
        }
        if parent_id:
            payload["parent_id"] = parent_id
        return self._request("POST", "/v1/project/work_items", json=payload)

    def update_work_item(
        self,
        work_item_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
        type_id: str | None = None,
        parent_id: str | None = None,
        state_id: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if type_id is not None:
            payload["type_id"] = type_id
        if parent_id is not None:
            payload["parent_id"] = parent_id
        if state_id is not None:
            payload["state_id"] = state_id
        if not payload:
            raise PingCodeError("更新工作项时至少提供一个可修改字段。")
        return self._request("PATCH", f"/v1/project/work_items/{work_item_id}", json=payload)

    def get_project_members(self, project_id: str) -> dict[str, Any]:
        return self._request("GET", f"/v1/project/projects/{project_id}/members")

    def add_project_member(self, project_id: str, user_id: str, role_id: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"user_id": user_id}
        if role_id:
            payload["role_id"] = role_id
        return self._request("POST", f"/v1/project/projects/{project_id}/members", json=payload)

    def update_project_member(self, project_id: str, member_id: str, role_id: str) -> dict[str, Any]:
        return self._request(
            "PATCH",
            f"/v1/project/projects/{project_id}/members/{member_id}",
            json={"role_id": role_id},
        )

    def remove_project_member(self, project_id: str, member_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"/v1/project/projects/{project_id}/members/{member_id}")

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        token = self.get_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        response = httpx.request(
            method,
            f"{self.base_url}{path}",
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        return self._parse_response(response)

    @staticmethod
    def _parse_response(response: httpx.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError as exc:
            raise PingCodeError(f"PingCode 返回了非 JSON 响应，HTTP {response.status_code}") from exc
        if response.is_success:
            return payload
        message = payload.get("error_description") or payload.get("message") or payload.get("error") or str(payload)
        raise PingCodeError(f"PingCode API 请求失败，HTTP {response.status_code}: {message}")
