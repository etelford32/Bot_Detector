"""Command-line interface for thread analysis."""

import argparse
import json
import sys
from pathlib import Path

from ingestion.thread_fetcher import fetch_thread, fetch_subreddit_window
from analysis.consensus_score import calculate_consensus_score
from explainability.rationale import (
    generate_rationale,
    generate_short_summary,
    format_detailed_report,
)
from explainability.summaries import (
    generate_json_summary,
    format_markdown_report,
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ConsensusWatch - Detect synthetic consensus in Reddit threads"
    )

    # Analysis mode
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Analyze thread
    thread_parser = subparsers.add_parser("analyze", help="Analyze a Reddit thread")
    thread_parser.add_argument(
        "--url",
        type=str,
        help="Reddit thread URL",
    )
    thread_parser.add_argument(
        "--subreddit",
        type=str,
        help="Subreddit to analyze (alternative to --url)",
    )
    thread_parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Time window in hours (for subreddit analysis)",
    )
    thread_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output with detailed metrics",
    )
    thread_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path (JSON or Markdown)",
    )
    thread_parser.add_argument(
        "--format",
        "-f",
        type=str,
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format",
    )
    thread_parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable embedding cache",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args)
    else:
        parser.print_help()
        sys.exit(1)


def analyze_command(args):
    """Handle analyze command."""
    try:
        # Determine analysis mode
        if args.url:
            analyze_single_thread(args)
        elif args.subreddit:
            analyze_subreddit(args)
        else:
            print("Error: Must provide either --url or --subreddit")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def analyze_single_thread(args):
    """Analyze a single thread."""
    print(f"Fetching thread: {args.url}")

    # Fetch thread
    thread_data = fetch_thread(args.url)

    print(f"Analyzing {thread_data['comments_analyzed']} comments...")

    # Calculate score
    use_cache = not args.no_cache
    score, metrics = calculate_consensus_score(thread_data, use_cache)

    # Generate output
    if args.format == "json":
        output = generate_json_output(thread_data, score, metrics)
    elif args.format == "markdown":
        output = format_markdown_report(thread_data, score, metrics)
    else:
        output = generate_text_output(thread_data, score, metrics, args.verbose)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output)
        print(f"\nResults written to: {args.output}")
    else:
        print("\n" + output)


def analyze_subreddit(args):
    """Analyze subreddit over time window."""
    print(f"Fetching threads from r/{args.subreddit} (last {args.hours} hours)...")

    # Fetch threads
    threads = fetch_subreddit_window(
        args.subreddit,
        hours=args.hours,
    )

    if not threads:
        print("No threads found matching criteria")
        return

    print(f"Analyzing {len(threads)} threads...")

    # Analyze each thread
    results = []
    for i, thread_data in enumerate(threads, 1):
        print(f"  [{i}/{len(threads)}] {thread_data['title'][:60]}...")

        try:
            use_cache = not args.no_cache
            score, metrics = calculate_consensus_score(thread_data, use_cache)

            results.append({
                "thread": thread_data,
                "score": score,
                "metrics": metrics,
            })
        except Exception as e:
            print(f"    Error: {str(e)}")
            continue

    # Generate summary
    if args.format == "json":
        output = json.dumps({
            "subreddit": args.subreddit,
            "time_window_hours": args.hours,
            "threads_analyzed": len(results),
            "results": [
                generate_json_summary(r["thread"], r["score"], r["metrics"])
                for r in results
            ],
        }, indent=2)
    else:
        output = generate_subreddit_summary(args.subreddit, args.hours, results)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output)
        print(f"\nResults written to: {args.output}")
    else:
        print("\n" + output)


def generate_text_output(thread_data, score, metrics, verbose):
    """Generate text output."""
    if verbose:
        return format_detailed_report(score, metrics, include_raw_metrics=True)
    else:
        return generate_rationale(score, metrics)


def generate_json_output(thread_data, score, metrics):
    """Generate JSON output."""
    summary = generate_json_summary(thread_data, score, metrics)
    return json.dumps(summary, indent=2)


def generate_subreddit_summary(subreddit, hours, results):
    """Generate summary for subreddit analysis."""
    if not results:
        return "No results to summarize"

    scores = [r["score"] for r in results]

    summary = []
    summary.append("=" * 80)
    summary.append(f"SUBREDDIT ANALYSIS: r/{subreddit}")
    summary.append(f"Time window: Last {hours} hours")
    summary.append("=" * 80)
    summary.append("")

    # Statistics
    summary.append(f"Threads analyzed: {len(results)}")
    summary.append(f"Average score: {sum(scores) / len(scores):.1f}")
    summary.append(f"Max score: {max(scores):.1f}")
    summary.append(f"Min score: {min(scores):.1f}")
    summary.append("")

    # Risk breakdown
    high_risk = sum(1 for s in scores if s >= 75)
    medium_risk = sum(1 for s in scores if 50 <= s < 75)
    low_risk = sum(1 for s in scores if s < 50)

    summary.append("Risk Distribution:")
    summary.append(f"  High risk (≥75):    {high_risk} threads")
    summary.append(f"  Medium risk (50-74): {medium_risk} threads")
    summary.append(f"  Low risk (<50):      {low_risk} threads")
    summary.append("")

    # Top threads by score
    summary.append("-" * 80)
    summary.append("Top 5 Highest Risk Threads:")
    summary.append("-" * 80)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    for i, result in enumerate(sorted_results[:5], 1):
        thread = result["thread"]
        score = result["score"]
        interpretation = result["metrics"]["interpretation"]["level"]

        title = thread["title"]
        if len(title) > 60:
            title = title[:57] + "..."

        summary.append(f"{i}. [{score:.1f}] {title}")
        summary.append(f"   {interpretation}")
        summary.append("")

    return "\n".join(summary)


if __name__ == "__main__":
    main()
