import json
import shutil
import subprocess
from datetime import date
from pathlib import Path

import pytest

from nitimarg import audio, factcheck, publish, render, state, telegram, topics, tts
from nitimarg.config import Config
from nitimarg.llm import extract_json
from nitimarg.placeholders import ensure_poses
from nitimarg.script import normalise

PKG = Path(__file__).resolve().parents[1]
SAMPLE = json.loads((PKG / "data/scripts/pm-kisan.json").read_text(encoding="utf-8"))
TOPICS = topics.load_topics(PKG / "data/topics.json")


def test_topics_file_valid():
    ids = [t["id"] for t in TOPICS]
    assert len(ids) == len(set(ids))
    for t in TOPICS:
        assert t["official_url"].startswith("https://")
        assert t["category"] in {"kisan", "women", "loans", "nri", "pm-tenure", "general"}


def test_pick_topic_nri_every_fifth():
    picks = [topics.pick_topic(TOPICS, [], n, 5)["category"] for n in range(5)]
    assert picks[4] == "nri"
    assert all(c != "nri" for c in picks[:4])


def test_pick_topic_skips_used_and_disabled():
    ts = [{"id": "a", "category": "general"}, {"id": "b", "category": "general"},
          {"id": "c", "category": "general", "enabled": False}]
    assert topics.pick_topic(ts, ["a"], 0)["id"] == "b"
    assert topics.pick_topic(ts, ["a", "b"], 0)["id"] == "a"  # recycle oldest


def test_streak():
    days = ["2026-11-25", "2026-11-26", "2026-11-27"]
    assert state.streak(days, date(2026, 11, 27)) == 3
    assert state.streak(days, date(2026, 11, 28)) == 3
    assert state.streak(days, date(2026, 11, 30)) == 0


def test_single_instance_lock(tmp_path):
    with state.single_instance(tmp_path / "x.lock"):
        with pytest.raises(RuntimeError):
            with state.single_instance(tmp_path / "x.lock"):
                pass


def test_extract_json_handles_fences_and_think():
    assert extract_json('<think>hmm</think>```json\n{"a": 1}\n```') == {"a": 1}


def test_normalise_fixes_bad_pose_and_order():
    raw = {"title": "T", "beats": [
        {"beat": "cta", "pose": "dancing", "line": "Subscribe"},
        {"beat": "hook", "pose": "worried", "line": "Paise"},
        {"beat": "scheme", "pose": "explaining", "line": "x"},
        {"beat": "eligibility", "pose": "explaining", "line": "x"},
        {"beat": "apply", "pose": "holding_phone", "line": "x"},
        {"beat": "warning", "pose": "warning", "line": "x"},
    ], "hashtags": ["A", "#B"]}
    s = normalise(raw, {"id": "t", "name": "T", "official_url": "https://x.gov.in"})
    assert [b["beat"] for b in s["beats"]][0] == "hook"
    assert s["beats"][-1]["pose"] == "celebrating"
    assert s["hashtags"] == ["#A", "#B", "#NitiMarg"]


def test_normalise_rejects_missing_beats():
    with pytest.raises(ValueError):
        normalise({"beats": [{"beat": "hook", "line": "x"}]},
                  {"id": "t", "name": "T", "official_url": "https://x"})


def test_factcheck_numbers():
    src = factcheck.page_text("<p>Rs 6000 per year in 3 instalments of Rs. 2,000</p><script>99</script>")
    script = {"beats": [{"line": "6,000 rupaye, 2,000 ki teen kist", "screen": "₹9,999"}]}
    rep = factcheck.check(script, src)
    assert rep["missing"] == ["9999"]
    assert not rep["ok"]
    assert "9999" in factcheck.summary(rep)


def test_description_has_fold_link_chapters_disclaimer():
    chs = [("hook", 0), ("problem", 3), ("scheme", 20), ("eligibility", 45), ("apply", 70),
           ("warning", 90), ("cta", 110)]
    d = publish.description(SAMPLE, chs, 130, "https://nitimarg.in")
    lines = d.splitlines()
    assert "pmkisan.gov.in" in lines[1]
    assert "0:00" in d and "Chapters:" in d
    assert publish.DISCLAIMER in d
    assert lines[-1] == "#PMKisan #SarkariYojana #KisanYojana"


def test_chapters_merge_short_ones():
    out = publish.chapters([("hook", 3), ("problem", 8), ("scheme", 30), ("apply", 60)], 80)
    assert out[0] == ("hook", 0.0)
    assert ("problem", 8) not in out


def test_tags_include_extra_hashtags():
    assert "NitiMarg" in publish.tags(SAMPLE)


def test_telegram_callback_parse():
    upd = {"callback_query": {"id": "1", "data": "nm:approve:run1", "message": {"chat": {"id": 42}}}}
    assert telegram.parse_callback(upd) == ("1", "approve", "run1", "42")
    assert telegram.parse_callback({"callback_query": {"id": "1", "data": "other"}}) is None


def test_caption_chunks():
    line = " ".join(["word"] * 30)
    chunks = render.caption_chunks(line)
    assert len(chunks) >= 3 and " ".join(chunks) == line


def test_mouth_track_and_concat(tmp_path):
    a, b = tmp_path / "a.wav", tmp_path / "b.wav"
    tts.preview("Namaste didi, paise mil gaye?", a)
    audio.silence(b, 1.0)
    runs = audio.mouth_track(a, 8)
    assert any(r[0] for r in runs) and any(not r[0] for r in runs)
    assert abs(sum(r[1] for r in runs) - audio.duration(a)) < 0.01
    out = tmp_path / "ab.wav"
    starts = audio.concat([a, b], out, gap=0.35)
    assert starts[1] == pytest.approx(audio.duration(a) + 0.35, abs=0.01)
    audio.trim(out, 1.0)
    assert audio.duration(out) == pytest.approx(1.0, abs=0.01)


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg not installed")
def test_render_sample_end_to_end(tmp_path, monkeypatch):
    monkeypatch.setenv("NM_TTS", "preview")
    cfg = Config()
    cfg.poses_dir = tmp_path / "poses"
    cfg.long_size = (640, 360)
    cfg.short_size = (360, 640)
    ensure_poses(cfg.poses_dir)
    wavs = {}
    for b in SAMPLE["beats"]:
        wavs[b["beat"]] = tmp_path / f"{b['beat']}.wav"
        tts.speak(cfg, b["line"], wavs[b["beat"]])
    long = render.render(cfg, SAMPLE, wavs, tmp_path / "long.mp4", cfg.long_size)
    short = render.render(cfg, SAMPLE, wavs, tmp_path / "short.mp4", cfg.short_size,
                          beats=["hook", "warning"], intro=False, endcard=True, max_seconds=12)
    assert long["chapters"][0] == ("hook", render.INTRO_SECONDS)
    for path, expected in ((long["path"], long["duration"]), (short["path"], 12.0)):
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", path]).strip())
        assert dur == pytest.approx(expected, abs=0.3)
    thumb = render.thumbnail(cfg, SAMPLE, tmp_path / "t.jpg")
    assert thumb.stat().st_size > 10_000
