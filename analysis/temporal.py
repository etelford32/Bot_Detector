"""Temporal analysis of comment patterns."""

from typing import Dict, List, Any, Tuple
import numpy as np
from datetime import datetime
from collections import Counter


def calculate_posting_rate(
    timestamps: List[int],
    window_size: int = 900,  # 15 minutes in seconds
) -> Dict[str, Any]:
    """Calculate posting rate metrics.

    Args:
        timestamps: List of Unix timestamps
        window_size: Window size in seconds

    Returns:
        Dictionary of posting rate metrics
    """
    if len(timestamps) < 2:
        return {
            "avg_rate": 0.0,
            "peak_rate": 0.0,
            "baseline_rate": 0.0,
            "burst_coefficient": 0.0,
        }

    timestamps_sorted = sorted(timestamps)
    min_time = timestamps_sorted[0]
    max_time = timestamps_sorted[-1]
    duration = max_time - min_time

    if duration == 0:
        return {
            "avg_rate": len(timestamps),
            "peak_rate": len(timestamps),
            "baseline_rate": len(timestamps),
            "burst_coefficient": 1.0,
        }

    # Calculate average rate (comments per second)
    avg_rate = len(timestamps) / duration

    # Sliding window analysis
    window_rates = []
    current_time = min_time

    while current_time <= max_time:
        window_end = current_time + window_size
        count = sum(1 for t in timestamps_sorted if current_time <= t < window_end)
        rate = count / window_size
        window_rates.append(rate)
        current_time += window_size // 2  # 50% overlap

    peak_rate = max(window_rates) if window_rates else 0.0
    median_rate = np.median(window_rates) if window_rates else 0.0
    baseline_rate = median_rate

    # Burst coefficient (peak vs baseline)
    burst_coefficient = peak_rate / baseline_rate if baseline_rate > 0 else 1.0

    return {
        "avg_rate": float(avg_rate),
        "peak_rate": float(peak_rate),
        "baseline_rate": float(baseline_rate),
        "burst_coefficient": float(burst_coefficient),
    }


def detect_bursts(
    timestamps: List[int],
    window_size: int = 900,
    threshold: float = 3.0,
) -> List[Dict[str, Any]]:
    """Detect posting bursts.

    Args:
        timestamps: List of Unix timestamps
        window_size: Window size in seconds
        threshold: Burst threshold (ratio to baseline)

    Returns:
        List of detected bursts
    """
    if len(timestamps) < 5:
        return []

    rate_metrics = calculate_posting_rate(timestamps, window_size)
    baseline_rate = rate_metrics["baseline_rate"]

    if baseline_rate == 0:
        return []

    timestamps_sorted = sorted(timestamps)
    min_time = timestamps_sorted[0]
    max_time = timestamps_sorted[-1]

    bursts = []
    current_time = min_time

    while current_time <= max_time:
        window_end = current_time + window_size

        # Count comments in window
        window_timestamps = [
            t for t in timestamps_sorted if current_time <= t < window_end
        ]
        count = len(window_timestamps)
        rate = count / window_size

        # Check if this is a burst
        if rate >= baseline_rate * threshold:
            burst = {
                "start_time": int(current_time),
                "end_time": int(window_end),
                "count": count,
                "rate": float(rate),
                "ratio_to_baseline": float(rate / baseline_rate),
                "timestamps": window_timestamps,
            }
            bursts.append(burst)

        current_time += window_size // 2

    # Merge overlapping bursts
    merged_bursts = merge_overlapping_bursts(bursts)

    return merged_bursts


def merge_overlapping_bursts(bursts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge overlapping burst periods.

    Args:
        bursts: List of burst dictionaries

    Returns:
        List of merged bursts
    """
    if not bursts:
        return []

    # Sort by start time
    bursts_sorted = sorted(bursts, key=lambda x: x["start_time"])

    merged = [bursts_sorted[0]]

    for burst in bursts_sorted[1:]:
        last = merged[-1]

        # Check if overlapping
        if burst["start_time"] <= last["end_time"]:
            # Merge
            last["end_time"] = max(last["end_time"], burst["end_time"])
            last["count"] = max(last["count"], burst["count"])
            last["rate"] = max(last["rate"], burst["rate"])
        else:
            merged.append(burst)

    return merged


def calculate_timing_entropy(timestamps: List[int]) -> float:
    """Calculate entropy of inter-comment intervals.

    Args:
        timestamps: List of Unix timestamps

    Returns:
        Shannon entropy of intervals (higher = more random/organic)
    """
    if len(timestamps) < 2:
        return 0.0

    timestamps_sorted = sorted(timestamps)

    # Calculate intervals
    intervals = np.diff(timestamps_sorted)

    # Bin intervals (in seconds)
    bins = [0, 10, 30, 60, 120, 300, 600, 1800, 3600, float('inf')]
    binned = np.digitize(intervals, bins)

    # Calculate entropy
    counts = Counter(binned)
    total = len(binned)
    probabilities = [count / total for count in counts.values()]

    entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)

    return float(entropy)


def detect_coordinated_timing(
    timestamps: List[int],
    tolerance: int = 60,  # seconds
) -> List[Tuple[List[int], int]]:
    """Detect groups of comments posted at nearly the same time.

    Args:
        timestamps: List of Unix timestamps
        tolerance: Time tolerance in seconds

    Returns:
        List of (timestamp_group, count) tuples
    """
    if len(timestamps) < 3:
        return []

    timestamps_sorted = sorted(timestamps)

    coordinated = []
    i = 0

    while i < len(timestamps_sorted):
        group = [timestamps_sorted[i]]
        j = i + 1

        # Find all timestamps within tolerance
        while j < len(timestamps_sorted):
            if timestamps_sorted[j] - timestamps_sorted[i] <= tolerance:
                group.append(timestamps_sorted[j])
                j += 1
            else:
                break

        # If group is large enough, it's coordinated
        if len(group) >= 3:
            coordinated.append((group, len(group)))

        i = j if j > i + 1 else i + 1

    # Sort by group size (largest first)
    coordinated.sort(key=lambda x: x[1], reverse=True)

    return coordinated


def calculate_temporal_score(
    timestamps: List[int],
    window_size: int = 900,
    burst_threshold: float = 3.0,
) -> Dict[str, float]:
    """Calculate temporal coordination score.

    Args:
        timestamps: List of Unix timestamps
        window_size: Window size in seconds
        burst_threshold: Burst detection threshold

    Returns:
        Dictionary of temporal metrics
    """
    if len(timestamps) < 5:
        return {
            "temporal_score": 0.0,
            "burst_coefficient": 0.0,
            "timing_entropy": 1.0,
            "n_bursts": 0,
        }

    # Calculate posting rate metrics
    rate_metrics = calculate_posting_rate(timestamps, window_size)
    burst_coefficient = rate_metrics["burst_coefficient"]

    # Detect bursts
    bursts = detect_bursts(timestamps, window_size, burst_threshold)
    n_bursts = len(bursts)

    # Calculate timing entropy
    timing_entropy = calculate_timing_entropy(timestamps)
    max_entropy = np.log2(9)  # Max possible entropy with our binning
    normalized_entropy = timing_entropy / max_entropy

    # Detect coordinated timing
    coordinated_groups = detect_coordinated_timing(timestamps)
    max_coordinated = max([count for _, count in coordinated_groups], default=0)
    coordinated_ratio = max_coordinated / len(timestamps) if len(timestamps) > 0 else 0

    # Calculate temporal score (0-100)
    # Higher score = more suspicious timing patterns
    temporal_score = (
        0.4 * min(burst_coefficient * 10, 100) +  # Burst detection
        0.3 * ((1.0 - normalized_entropy) * 100) +  # Low entropy = suspicious
        0.3 * (coordinated_ratio * 100)  # Coordinated posting
    )

    return {
        "temporal_score": float(temporal_score),
        "burst_coefficient": burst_coefficient,
        "timing_entropy": timing_entropy,
        "normalized_entropy": normalized_entropy,
        "n_bursts": n_bursts,
        "max_coordinated_group": max_coordinated,
        "coordinated_ratio": coordinated_ratio,
    }


def analyze_time_series(
    timestamps: List[int],
    bin_size: int = 3600,  # 1 hour bins
) -> Dict[str, Any]:
    """Analyze posting time series.

    Args:
        timestamps: List of Unix timestamps
        bin_size: Time bin size in seconds

    Returns:
        Time series analysis dictionary
    """
    if not timestamps:
        return {
            "bins": [],
            "counts": [],
            "times": [],
        }

    timestamps_sorted = sorted(timestamps)
    min_time = timestamps_sorted[0]
    max_time = timestamps_sorted[-1]

    bins = []
    counts = []
    times = []

    current_time = min_time
    while current_time <= max_time:
        bin_end = current_time + bin_size
        count = sum(1 for t in timestamps_sorted if current_time <= t < bin_end)

        bins.append(int(current_time))
        counts.append(count)
        times.append(datetime.fromtimestamp(current_time).isoformat())

        current_time += bin_size

    return {
        "bins": bins,
        "counts": counts,
        "times": times,
        "bin_size": bin_size,
    }
