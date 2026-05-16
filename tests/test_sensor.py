"""Tests for the TrendPredictorData calculation logic."""

from collections import deque
from datetime import datetime, timedelta, timezone

import pytest


def _make_data(min_value: float = 0.0, max_value: float = 100.0, time_window: int = 30):
    class FakeData:
        def __init__(self):
            self.min_value = min_value
            self.max_value = max_value
            self.time_window = time_window
            self._history = deque()
            self.rate = None
            self.hours_remaining = None
            self.predicted_time = None
            self.active_target = None

        def _recalculate(self):
            history = list(self._history)
            if len(history) < 2:
                self.rate = None
                self.hours_remaining = None
                self.predicted_time = None
                self.active_target = None
                return

            t0 = history[0][0]
            times = [(t - t0).total_seconds() / 3600 for t, _ in history]
            values = [v for _, v in history]

            n = len(times)
            sum_t = sum(times)
            sum_v = sum(values)
            sum_tv = sum(t * v for t, v in zip(times, values))
            sum_t2 = sum(t * t for t in times)

            denom = n * sum_t2 - sum_t**2
            if denom == 0:
                self.rate = None
                self.hours_remaining = None
                self.predicted_time = None
                self.active_target = None
                return

            rate = (n * sum_tv - sum_t * sum_v) / denom
            intercept = (sum_v - rate * sum_t) / n
            current_v = rate * times[-1] + intercept
            self.rate = round(rate, 4)

            if rate == 0:
                self.hours_remaining = None
                self.predicted_time = None
                self.active_target = None
                return

            target = self.min_value if rate < 0 else self.max_value
            self.active_target = target
            hours = (target - current_v) / rate

            if hours < 0:
                self.hours_remaining = None
                self.predicted_time = None
            else:
                self.hours_remaining = round(hours, 2)
                self.predicted_time = datetime.now(timezone.utc) + timedelta(hours=hours)

    return FakeData()


def _add_points(data, values_per_hour: list[tuple[float, float]]):
    base = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    for hours_offset, value in values_per_hour:
        data._history.append((base + timedelta(hours=hours_offset), value))


class TestRecalculate:
    def test_fewer_than_two_points_returns_none(self):
        data = _make_data()
        _add_points(data, [(0, 50.0)])
        data._recalculate()
        assert data.rate is None
        assert data.hours_remaining is None
        assert data.active_target is None

    def test_falling_trend_targets_min(self):
        data = _make_data(min_value=0.0, max_value=100.0)
        # -10 %/h: t=0 → 100%, t=0.5h → 95%, t=1h → 90%
        _add_points(data, [(0, 100.0), (0.5, 95.0), (1.0, 90.0)])
        data._recalculate()
        assert data.rate == pytest.approx(-10.0, abs=0.01)
        assert data.active_target == 0.0
        # From 90% at -10/h → 9h to reach 0
        assert data.hours_remaining == pytest.approx(9.0, abs=0.1)

    def test_rising_trend_targets_max(self):
        data = _make_data(min_value=0.0, max_value=100.0)
        # +5 %/h: t=0 → 20%, t=0.5h → 22.5%, t=1h → 25%
        _add_points(data, [(0, 20.0), (0.5, 22.5), (1.0, 25.0)])
        data._recalculate()
        assert data.rate == pytest.approx(5.0, abs=0.01)
        assert data.active_target == 100.0
        # From 25% at +5/h → 15h to reach 100
        assert data.hours_remaining == pytest.approx(15.0, abs=0.1)

    def test_custom_bounds(self):
        data = _make_data(min_value=200.0, max_value=1000.0)
        # Falling: should target min_value=200
        _add_points(data, [(0, 800.0), (0.5, 750.0), (1.0, 700.0)])
        data._recalculate()
        assert data.active_target == 200.0
        assert data.rate == pytest.approx(-100.0, abs=0.1)
        assert data.hours_remaining == pytest.approx(5.0, abs=0.1)

    def test_flat_trend_returns_none(self):
        data = _make_data()
        _add_points(data, [(0, 50.0), (0.5, 50.0), (1.0, 50.0)])
        data._recalculate()
        assert data.hours_remaining is None
        assert data.active_target is None

    def test_predicted_time_is_set_for_valid_trend(self):
        data = _make_data()
        _add_points(data, [(0, 60.0), (0.5, 55.0), (1.0, 50.0)])
        data._recalculate()
        assert data.predicted_time is not None
        assert data.active_target == 0.0
