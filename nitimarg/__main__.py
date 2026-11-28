"""CLI: python -m nitimarg <command>."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from . import pipeline, state
from .config import Config
from .placeholders import ensure_poses


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="nitimarg", description="Niti Marg video pipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="daily run: topic -> script -> video -> Telegram")
    run.add_argument("--topic", help="force a topic id from topics.json")
    run.add_argument("--script", type=Path, help="render an existing script JSON (skips the LLM)")
    run.add_argument("--no-send", action="store_true", help="render only, do not send to Telegram")
    sub.add_parser("poll", help="handle Telegram approve/reject taps")
    sub.add_parser("trends", help="weekly sentiment check, proposes topics on Telegram")
    poses = sub.add_parser("poses", help="create placeholder pose images for missing poses")
    poses.add_argument("--overwrite", action="store_true")
    sub.add_parser("status", help="show queue, runs and streak")
    prep = sub.add_parser("prep-poses", help="cut out real pose art and copy it into the poses folder")
    prep.add_argument("src", type=Path, help="folder with neutral.png, worried.jpg, ...")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = Config()

    if args.cmd == "run":
        res = pipeline.run_daily(cfg, topic_id=args.topic, script_file=args.script, send=not args.no_send)
        print(json.dumps({"run": res["id"], "dir": res["dir"], "factcheck": res["factcheck"]}, indent=2))
    elif args.cmd == "poll":
        print(f"handled {pipeline.poll_approvals(cfg)} taps")
    elif args.cmd == "trends":
        for t in pipeline.weekly_trends(cfg):
            print(f"proposed: {t['id']} - {t['name']}")
    elif args.cmd == "poses":
        made = ensure_poses(cfg.poses_dir, overwrite=args.overwrite)
        print(f"created {len(made)} pose files in {cfg.poses_dir}")
    elif args.cmd == "prep-poses":
        from .poses import prepare
        for p in prepare(args.src, cfg.poses_dir):
            print(f"ready: {p}")
    elif args.cmd == "status":
        st = state.load(cfg.state_file)
        print(f"videos made: {st['videos_made']} | streak: {state.streak(st['approved_days'])} days")
        for rid, r in sorted(st["runs"].items())[-10:]:
            print(f"  {rid}: {r['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
