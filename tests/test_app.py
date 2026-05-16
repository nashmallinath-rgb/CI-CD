"""Tests for the FastAPI application."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(app)


class TestRoot:
    def test_root_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200

    def test_root_has_message(self):
        r = client.get("/")
        assert "message" in r.json()


class TestHealth:
    def test_health_ok(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"

    def test_health_has_uptime(self):
        r = client.get("/health")
        assert "uptime_seconds" in r.json()


class TestCoins:
    def test_list_coins(self):
        r = client.get("/coins")
        assert r.status_code == 200
        assert r.json()["count"] == 5

    def test_valid_coin(self):
        r = client.get("/coins/bitcoin")
        assert r.status_code == 200
        assert r.json()["tracked"] is True

    def test_invalid_coin_404(self):
        r = client.get("/coins/dogecoin")
        assert r.status_code == 404

    def test_all_coins_valid(self):
        for coin in ["bitcoin", "ethereum", "solana", "cardano", "polkadot"]:
            r = client.get(f"/coins/{coin}")
            assert r.status_code == 200, f"Failed for {coin}"
