#!/usr/bin/env python3
"""Seed the Heist at Marble Arch backlog into a GitHub repo: the Quest 1 fallback.

Creates labels, milestones M1 to M3, five epics and their stories, and links each
story to its epic as a sub-issue. Safe to re-run: existing items are reused.

Needs the GitHub CLI (`gh auth login`). Standard library only.

  python scripts/seed_backlog.py --repo OWNER/REPO --dry-run
  python scripts/seed_backlog.py --repo OWNER/REPO
  python scripts/seed_backlog.py --repo OWNER/REPO --issue-types   # org repos with Epic/Task issue types
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "backlog" / "backlog.json"


class GhError(RuntimeError):
    pass


class GitHub:
    def __init__(self, repo: str, dry_run: bool) -> None:
        self.repo = repo
        self.dry_run = dry_run
        self._fake_id = 1000
        self._fake_number = 0

    def api(self, method: str, path: str, body: dict | None = None) -> object:
        if self.dry_run and method != "GET":
            print(f"  [dry-run] {method} {path} {json.dumps(body or {}, ensure_ascii=False)[:110]}")
            if path.endswith("/milestones"):
                return {"number": 1, "html_url": "(dry-run)"}
            if path.endswith("/issues"):
                self._fake_id += 1
                self._fake_number += 1
            return {"id": self._fake_id, "number": self._fake_number, "html_url": "(dry-run)"}
        if self.dry_run:
            return []
        cmd = ["gh", "api", "-X", method, path, "-H", "Accept: application/vnd.github+json"]
        data = None
        if body is not None:
            cmd += ["--input", "-"]
            data = json.dumps(body)
        result = subprocess.run(cmd, input=data, capture_output=True, text=True)
        if result.returncode != 0:
            raise GhError((result.stderr or result.stdout).strip())
        return json.loads(result.stdout) if result.stdout.strip() else {}


def ensure_labels(gh: GitHub, labels: list[dict]) -> None:
    for label in labels:
        try:
            gh.api("POST", f"repos/{gh.repo}/labels", label)
            print(f"  + label {label['name']}")
        except GhError as exc:
            if "already_exists" in str(exc) or "already exists" in str(exc):
                print(f"  = label {label['name']}")
            else:
                raise


def ensure_milestones(gh: GitHub, milestones: list[dict]) -> dict[str, int]:
    existing = {m["title"]: m["number"] for m in gh.api("GET", f"repos/{gh.repo}/milestones?state=all&per_page=100")}
    numbers: dict[str, int] = {}
    for milestone in milestones:
        if milestone["title"] in existing:
            numbers[milestone["key"]] = existing[milestone["title"]]
            print(f"  = milestone {milestone['title']}")
            continue
        body = {k: milestone[k] for k in ("title", "description", "due_on") if k in milestone}
        created = gh.api("POST", f"repos/{gh.repo}/milestones", body)
        numbers[milestone["key"]] = created["number"]
        print(f"  + milestone {milestone['title']}")
    return numbers


def existing_issues(gh: GitHub) -> dict[str, dict]:
    issues = gh.api("GET", f"repos/{gh.repo}/issues?state=all&per_page=100")
    return {i["title"]: i for i in issues if "pull_request" not in i}


def ensure_issue(gh: GitHub, cache: dict[str, dict], title: str, body: str, labels: list[str],
                 milestone: int | None, issue_type: str | None) -> dict:
    if title in cache:
        print(f"  = #{cache[title]['number']} {title}")
        return cache[title]
    payload = {"title": title, "body": body, "labels": labels}
    if milestone:
        payload["milestone"] = milestone
    if issue_type:
        payload["type"] = issue_type
    try:
        issue = gh.api("POST", f"repos/{gh.repo}/issues", payload)
    except GhError as exc:
        if issue_type:  # issue types only exist on organisation repos that define them
            print(f"  ! issue type '{issue_type}' not accepted ({str(exc)[:80]}); using labels only")
            payload.pop("type")
            issue = gh.api("POST", f"repos/{gh.repo}/issues", payload)
        else:
            raise
    cache[title] = issue
    print(f"  + #{issue['number']} {title}")
    return issue


def link_sub_issue(gh: GitHub, parent: dict, child: dict) -> None:
    try:
        gh.api("POST", f"repos/{gh.repo}/issues/{parent['number']}/sub_issues", {"sub_issue_id": child["id"]})
    except GhError as exc:
        if "already" in str(exc).lower() or "duplicate" in str(exc).lower():
            return
        print(f"  ! couldn't link #{child['number']} under #{parent['number']}: {str(exc)[:120]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, help="OWNER/REPO of your crew repository")
    parser.add_argument("--dry-run", action="store_true", help="print what would be created")
    parser.add_argument("--issue-types", action="store_true", help="also set Epic / Task issue types (organisation repos)")
    args = parser.parse_args()

    if not args.dry_run and not shutil.which("gh"):
        print("The GitHub CLI (gh) isn't installed or isn't on PATH. Install it, run `gh auth login`, then retry.")
        return 2

    plan = json.loads(BACKLOG.read_text(encoding="utf-8"))
    gh = GitHub(args.repo, args.dry_run)
    try:
        print("Labels"); ensure_labels(gh, plan["labels"])
        print("Milestones"); milestones = ensure_milestones(gh, plan["milestones"])
        print("Issues"); cache = existing_issues(gh)
        created = 0
        for epic in plan["epics"]:
            parent = ensure_issue(gh, cache, epic["title"], epic["body"], epic["labels"],
                                  milestones.get(epic["milestone"]), "Epic" if args.issue_types else None)
            for story in epic["stories"]:
                child = ensure_issue(gh, cache, story["title"], story["body"], story["labels"],
                                     milestones.get(epic["milestone"]), "Task" if args.issue_types else None)
                link_sub_issue(gh, parent, child)
                created += 1
    except GhError as exc:
        print(f"\nGitHub said: {exc}\nCheck `gh auth status` and that you can write issues in {args.repo}.")
        return 1

    print(f"\nDone: {len(plan['milestones'])} milestones, {len(plan['epics'])} epics, {created} stories.")
    print(f"Open https://github.com/{args.repo}/milestones to see the plan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
