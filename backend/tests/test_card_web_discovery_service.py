import pytest

from app.services.card_web_discovery_service import CardWebDiscoveryService, WebDiscoveryResult


@pytest.mark.asyncio
async def test_discover_sources_success():
    async def fake_request(payload):
        return {
            "output": [
                {
                    "content": [
                        {"text": {"value": '{"official_url": "https://bank.example/card", "reddit_threads": ["https://reddit.com/r/test"]}', "annotations": []}}
                    ]
                }
            ]
        }

    service = CardWebDiscoveryService(request_func=fake_request)

    result = await service.discover_sources(bank_name="Bank", card_name="Card")

    assert isinstance(result, WebDiscoveryResult)
    assert result.official_url == "https://bank.example/card"
    assert result.reddit_threads == ["https://reddit.com/r/test"]


@pytest.mark.asyncio
async def test_discover_sources_retry_used_when_missing_official():
    calls = []

    async def fake_request(payload):
        calls.append(payload)
        if len(calls) == 1:
            return {
                "output": [
                    {"content": [{"text": {"value": '{"official_url": null, "reddit_threads": []}', "annotations": []}}]}
                ]
            }
        return {
            "output": [
                {"content": [{"text": {"value": '{"official_url": "https://official.example/card", "reddit_threads": ["https://reddit.com/r/test"]}', "annotations": []}}]}
            ]
        }

    service = CardWebDiscoveryService(request_func=fake_request)

    result = await service.discover_sources(bank_name="Bank", card_name="Card")

    assert result.official_url == "https://official.example/card"
    assert result.reddit_threads == ["https://reddit.com/r/test"]
    assert len(calls) == 2


@pytest.mark.asyncio
async def test_discover_sources_handles_invalid_json():
    async def fake_request(payload):
        return {"output": [{"content": [{"text": {"value": "not-json-data", "annotations": []}}]}]}

    service = CardWebDiscoveryService(request_func=fake_request)

    result = await service.discover_sources(bank_name="Bank", card_name="Card")

    assert result.official_url is None
    assert result.reddit_threads == []
