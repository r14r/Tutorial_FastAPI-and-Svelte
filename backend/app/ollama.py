"""Utilities and API routes that proxy requests to an Ollama server."""

from __future__ import annotations

import json
import os
from typing import Any, AsyncGenerator, Dict

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from . import schemas


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

_TIMEOUT = httpx.Timeout(60.0, connect=30.0, read=None, write=30.0)


router = APIRouter(prefix="/ollama", tags=["ollama"])


def _extract_error_detail(raw: str) -> str:
    if not raw:
        return "Upstream Ollama request failed"

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw

    if isinstance(payload, dict):
        for key in ("error", "message", "detail"):
            value = payload.get(key)
            if value:
                return str(value)
    return raw


async def _raise_for_response(response: httpx.Response) -> None:
    if response.status_code < 400:
        return

    detail = _extract_error_detail(response.text)
    raise HTTPException(status_code=response.status_code, detail=detail)


async def _post(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    async with httpx.AsyncClient(base_url=OLLAMA_BASE_URL, timeout=_TIMEOUT) as client:
        response = await client.post(endpoint, json=payload)

    await _raise_for_response(response)
    try:
        return response.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama") from None


async def _stream_post(endpoint: str, payload: Dict[str, Any]) -> AsyncGenerator[bytes, None]:
    async with httpx.AsyncClient(base_url=OLLAMA_BASE_URL, timeout=_TIMEOUT) as client:
        async with client.stream("POST", endpoint, json=payload) as response:
            if response.status_code >= 400:
                body = await response.aread()
                detail = _extract_error_detail(body.decode())
                raise HTTPException(status_code=response.status_code, detail=detail)

            async for chunk in response.aiter_bytes():
                if chunk:
                    yield chunk


@router.post("/chat", response_model=Dict[str, Any])
async def chat(request: schemas.OllamaChatRequest):
    payload = request.model_dump(exclude_none=True)
    payload["stream"] = False
    return await _post("/api/chat", payload)


@router.post("/chat/stream")
async def chat_stream(request: schemas.OllamaChatRequest):
    payload = request.model_dump(exclude_none=True)
    payload["stream"] = True
    return StreamingResponse(
        _stream_post("/api/chat", payload),
        media_type="application/x-ndjson",
    )


@router.post("/generate", response_model=Dict[str, Any])
async def generate(request: schemas.OllamaGenerateRequest):
    payload = request.model_dump(exclude_none=True)
    payload["stream"] = False
    return await _post("/api/generate", payload)


@router.post("/generate/stream")
async def generate_stream(request: schemas.OllamaGenerateRequest):
    payload = request.model_dump(exclude_none=True)
    payload["stream"] = True
    return StreamingResponse(
        _stream_post("/api/generate", payload),
        media_type="application/x-ndjson",
    )


@router.get("/models", response_model=Dict[str, Any])
async def list_models():
    async with httpx.AsyncClient(base_url=OLLAMA_BASE_URL, timeout=_TIMEOUT) as client:
        response = await client.get("/api/tags")

    await _raise_for_response(response)
    try:
        return response.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama") from None


@router.post("/pull")
async def pull(request: schemas.OllamaPullRequest):
    payload = request.model_dump(exclude_none=True)
    stream = payload.pop("stream", True)

    if stream:
        return StreamingResponse(
            _stream_post("/api/pull", payload),
            media_type="application/x-ndjson",
        )

    return await _post("/api/pull", payload)


@router.delete("/models/{model}", response_model=Dict[str, Any])
async def remove_model(model: str):
    async with httpx.AsyncClient(base_url=OLLAMA_BASE_URL, timeout=_TIMEOUT) as client:
        response = await client.delete("/api/models", json={"model": model})

    await _raise_for_response(response)
    try:
        return response.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama") from None


@router.get("/health", response_model=Dict[str, Any])
async def healthcheck():
    async with httpx.AsyncClient(base_url=OLLAMA_BASE_URL, timeout=_TIMEOUT) as client:
        response = await client.get("/")

    await _raise_for_response(response)
    try:
        return response.json()
    except json.JSONDecodeError:
        # Ollama's root endpoint may return plain text; expose it as a message.
        return {"status": response.text or "ok"}
