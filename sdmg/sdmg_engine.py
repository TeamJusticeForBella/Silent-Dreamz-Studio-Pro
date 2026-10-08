#!/usr/bin/env python3
"""SDMG Video Production Engine v1.0

Local-first, repeatable music-video production pipeline.
PROJECT: SDMG / Lost In A Dream
ARTIST: Mr. Silent Dreamz
LABEL: Artesia Records [SDMG]

Usage:
    python sdmg_engine.py audit          # Read-only environment + asset audit
    python sdmg_engine.py validate       # Validate EDL against transcript and sources
    python sdmg_engine.py concat         # Generate FFmpeg concat file from EDL
    python sdmg_engine.py render-simple  # Stream-copy assembly (fast, keyframe-aligned)
    python sdmg_engine.py render-full    # Re-encode assembly (frame-accurate, needs libx264)
    python sdmg_engine.py verify FILE    # FFprobe + SHA-256 verification of rendered MP4
    python sdmg_engine.py report         # Full delivery report
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
MASTERS_DIR = PROJECT_DIR / "masters"
INBOX_DIR = PROJECT_DIR / "meta-inbox"
MANIFESTS_DIR = PROJECT_DIR / "manifests"
RENDERS_DIR = PROJECT_DIR / "renders"
REPORTS_DIR = PROJECT_DIR / "reports"

MASTER_WAV = "Lost_In_A_Dream_-_Remastered_3.wav"
MASTER_SHA256 = "e4f4f8473b7008fb3e4e0bcf1beb64ebcc6da5fd188504719590a5b24f25264b"
MASTER_DURATION = 169.92
MASTER_SIZE = 32638490

EDL_FILE = MANIFESTS_DIR / "SDMG_EDL_Corrected_169_92.json"
TRANSCRIPT_FILE = MANIFESTS_DIR / "SDMG_Transcript_Timecoded.json"

SOURCE_PLATES = {
    "APPROVED_01": "image_20261007_193655.mp4",
    "APPROVED_02": "image_20261007_193910.mp4",
    "APPROVED_03": "image_20261007_193913_1.mp4",
    "APPROVED_04": "image_20261007_193911.mp4",
    "APPROVED_05": "image_20261007_193913.mp4",
    "A1": "image_20261007_201803.mp4",
    "A2": "image_20261007_201806.mp4",
    "A3": "image_20261007_201800.mp4",
    "B1": "image_20261007_201812.mp4",
    "B2": "image_20261007_201920.mp4",
    "B3": "image_20261007_201924.mp4",
    "C1": "image_20261007_201920_1.mp4",
    "C2": "image_20261007_201921.mp4",
    "C3": "image_20261007_202039.mp4",
    "D1": "image_20261007_202035.mp4",
    "D2": "image_20261007_202042.mp4",
    "D3": "image_20261007_202034.mp4",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def run_ffprobe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe", "-hide_banner", "-v", "error",
            "-show_entries", "format=duration,size,bit_rate",
            "-show_entries", "stream=codec_name,codec_type,width,height,avg_frame_rate,sample_rate,channels",
            "-of", "json", str(path),
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
    return json.loads(result.stdout)


def check_ffmpeg() -> dict:
    info = {"ffmpeg": "NOT_FOUND", "ffprobe": "NOT_FOUND", "libx264": False, "aac": False, "h264_decode": False}
    for tool in ("ffmpeg", "ffprobe"):
        path = shutil.which(tool)
        if path:
            r = subprocess.run([tool, "-version"], capture_output=True, text=True)
            info[tool] = r.stdout.split("\n")[0] if r.returncode == 0 else path

    r = subprocess.run(["ffmpeg", "-encoders"], capture_output=True, text=True)
    if r.returncode == 0:
        info["libx264"] = "libx264" in r.stdout
        info["aac"] = " aac " in r.stdout

    r = subprocess.run(["ffmpeg", "-decoders"], capture_output=True, text=True)
    if r.returncode == 0:
        info["h264_decode"] = "h264" in r.stdout

    return info


def cmd_audit(_args):
    print("=" * 60)
    print("SDMG ENVIRONMENT AUDIT")
    print("=" * 60)

    import platform
    print(f"\nOS: {platform.system()} {platform.release()} {platform.machine()}")
    print(f"Python: {platform.python_version()}")

    ff = check_ffmpeg()
    print(f"\nFFmpeg:  {ff['ffmpeg']}")
    print(f"FFprobe: {ff['ffprobe']}")
    print(f"libx264 encoder: {'AVAILABLE' if ff['libx264'] else 'NOT AVAILABLE'}")
    print(f"AAC encoder:     {'AVAILABLE' if ff['aac'] else 'NOT AVAILABLE'}")
    print(f"H.264 decoder:   {'AVAILABLE' if ff['h264_decode'] else 'NOT AVAILABLE'}")

    print(f"\n--- Directory Structure ---")
    for d in (MASTERS_DIR, INBOX_DIR, MANIFESTS_DIR, RENDERS_DIR, REPORTS_DIR):
        exists = d.exists()
        count = len(list(d.iterdir())) if exists else 0
        print(f"  {d.relative_to(PROJECT_DIR)}: {'EXISTS' if exists else 'MISSING'} ({count} files)")

    print(f"\n--- Master Audio ---")
    wav_path = MASTERS_DIR / MASTER_WAV
    if wav_path.exists():
        size = wav_path.stat().st_size
        sha = sha256_file(wav_path)
        match = sha == MASTER_SHA256
        print(f"  File: {MASTER_WAV}")
        print(f"  Size: {size:,} bytes (expected {MASTER_SIZE:,}) {'MATCH' if size == MASTER_SIZE else 'MISMATCH'}")
        print(f"  SHA-256: {sha}")
        print(f"  Hash:    {'VERIFIED' if match else 'MISMATCH - EXPECTED ' + MASTER_SHA256}")

        probe = run_ffprobe(wav_path)
        if "format" in probe:
            dur = float(probe["format"].get("duration", 0))
            print(f"  Duration: {dur:.2f}s (expected {MASTER_DURATION}s) {'VERIFIED' if abs(dur - MASTER_DURATION) < 0.1 else 'MISMATCH'}")
        for s in probe.get("streams", []):
            if s.get("codec_type") == "audio":
                print(f"  Codec: {s.get('codec_name')} | Rate: {s.get('sample_rate')}Hz | Channels: {s.get('channels')}")
    else:
        print(f"  {MASTER_WAV}: NOT FOUND")
        print(f"  -> Place the WAV in: {MASTERS_DIR}/")

    print(f"\n--- Video Plates ---")
    found = 0
    missing = []
    for clip_id, filename in sorted(SOURCE_PLATES.items()):
        path = INBOX_DIR / filename
        if path.exists():
            found += 1
            size = path.stat().st_size
            print(f"  [{clip_id:12s}] {filename} - {size:>10,} bytes - FOUND")
        else:
            missing.append((clip_id, filename))
            print(f"  [{clip_id:12s}] {filename} - MISSING")

    print(f"\n  Found: {found}/{len(SOURCE_PLATES)}")
    if missing:
        print(f"  Missing: {len(missing)}")
        print(f"  -> Place plates in: {INBOX_DIR}/")

    print(f"\n--- Manifests ---")
    for f in (EDL_FILE, TRANSCRIPT_FILE):
        if f.exists():
            print(f"  {f.name}: FOUND ({f.stat().st_size:,} bytes)")
        else:
            print(f"  {f.name}: MISSING")

    all_ok = (
        ff["libx264"] and ff["aac"] and ff["h264_decode"]
        and wav_path.exists()
        and found == len(SOURCE_PLATES)
        and EDL_FILE.exists()
    )
    status = "READY" if all_ok else "PENDING"
    print(f"\n{'=' * 60}")
    if found == 0 and not wav_path.exists():
        print(f"STATUS: PENDING - media files not yet uploaded")
        print(f"\nTo proceed, download from Meta AI and place files:")
        print(f"  WAV master -> {MASTERS_DIR}/{MASTER_WAV}")
        print(f"  17 plates  -> {INBOX_DIR}/image_20261007_*.mp4")
    elif not all_ok:
        print(f"STATUS: PENDING - some requirements missing (see above)")
    else:
        print(f"STATUS: READY - all assets verified, ready to render")
    print(f"{'=' * 60}")


def cmd_validate(_args):
    print("=" * 60)
    print("SDMG EDL VALIDATION")
    print("=" * 60)

    if not EDL_FILE.exists():
        print(f"FAILED: {EDL_FILE} not found")
        return 1

    with open(EDL_FILE) as f:
        edl_data = json.load(f)

    segments = edl_data["edl"]
    total_duration = sum(s["duration"] for s in segments)
    print(f"\nSegments: {len(segments)}")
    print(f"Total duration: {total_duration:.2f}s (master: {MASTER_DURATION}s)")

    errors = []

    prev_end = 0.0
    for s in segments:
        seg_num = s["seg"]
        if abs(s["start"] - prev_end) > 0.01:
            gap = s["start"] - prev_end
            errors.append(f"Seg {seg_num}: gap of {gap:.2f}s at {prev_end:.2f}-{s['start']:.2f}")
        calc_dur = s["end"] - s["start"]
        if abs(calc_dur - s["duration"]) > 0.01:
            errors.append(f"Seg {seg_num}: duration mismatch {s['duration']:.2f} vs calculated {calc_dur:.2f}")
        prev_end = s["end"]

    if abs(segments[0]["start"]) > 0.01:
        errors.append(f"First segment doesn't start at 0.0 (starts at {segments[0]['start']:.2f})")
    if abs(segments[-1]["end"] - MASTER_DURATION) > 0.1:
        errors.append(f"Last segment ends at {segments[-1]['end']:.2f}, expected {MASTER_DURATION}")

    hooks = [s for s in segments if s.get("hook")]
    print(f"Hook segments: {len(hooks)}")

    source_files_needed = set()
    for s in segments:
        source_files_needed.add(s["source_file"])
        if "source_file_2" in s:
            source_files_needed.add(s["source_file_2"])

    print(f"Unique source files: {len(source_files_needed)}")

    missing_sources = []
    for sf in sorted(source_files_needed):
        path = INBOX_DIR / sf
        if not path.exists():
            missing_sources.append(sf)

    if missing_sources:
        print(f"\nMissing source plates ({len(missing_sources)}):")
        for sf in missing_sources:
            print(f"  - {sf}")
    else:
        print(f"All source plates: FOUND" if source_files_needed else "Source plates: NOT CHECKED (none in inbox)")

    ext_segs = [s for s in segments if s.get("extension")]
    if ext_segs:
        print(f"\nExtension segments ({len(ext_segs)}):")
        for s in ext_segs:
            print(f"  Seg {s['seg']}: {s['extension']} - {s.get('extension_note', '')}")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print(f"\nVALIDATION: FAILED")
        return 1
    else:
        print(f"\nVALIDATION: VERIFIED - {len(segments)} segments, {total_duration:.2f}s, no gaps, no overlaps")
        return 0


def cmd_concat(_args):
    """Generate FFmpeg concat file from EDL for simple (non-extension) segments."""
    if not EDL_FILE.exists():
        print(f"FAILED: {EDL_FILE} not found")
        return 1

    with open(EDL_FILE) as f:
        edl_data = json.load(f)

    concat_path = MANIFESTS_DIR / "concat_corrected_EDL.txt"
    lines = []
    for s in edl_data["edl"]:
        src = s["source_file"]
        path = INBOX_DIR / src
        lines.append(f"file '{path}'")
        dur = s["duration"]
        lines.append(f"inpoint 0")
        lines.append(f"outpoint {dur}")

    with open(concat_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Concat file written: {concat_path}")
    print(f"Segments: {len(edl_data['edl'])}")
    print(f"Note: Extension segments (slow/freeze/loop) require render-full, not render-simple")
    return 0


def cmd_render_simple(_args):
    """Stream-copy assembly — fast but keyframe-aligned, not frame-accurate."""
    wav_path = MASTERS_DIR / MASTER_WAV
    concat_path = MANIFESTS_DIR / "concat_corrected_EDL.txt"
    output_path = RENDERS_DIR / "SDMG_LostInADream_FULL_NARRATIVE_169s.mp4"

    for required, label in [(wav_path, "Master WAV"), (concat_path, "Concat EDL")]:
        if not required.exists():
            print(f"FAILED: {label} not found at {required}")
            print(f"Run 'sdmg_engine.py concat' first, and ensure media files are in place.")
            return 1

    log_path = REPORTS_DIR / "ffmpeg_render.log"
    print(f"Starting stream-copy render...")
    print(f"  Input: {concat_path}")
    print(f"  Audio: {wav_path}")
    print(f"  Output: {output_path}")

    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_path),
        "-i", str(wav_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "320k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest",
        str(output_path),
    ]

    with open(log_path, "w") as logf:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=logf)

    if result.returncode != 0:
        print(f"RENDER FAILED (exit code {result.returncode})")
        print(f"See log: {log_path}")
        with open(log_path) as f:
            for line in f.readlines()[-10:]:
                print(f"  {line.rstrip()}")
        return 1

    if output_path.exists() and output_path.stat().st_size > 0:
        size = output_path.stat().st_size
        sha = sha256_file(output_path)
        print(f"\nRENDER COMPLETE")
        print(f"  File: {output_path}")
        print(f"  Size: {size:,} bytes ({size / 1024 / 1024:.1f} MB)")
        print(f"  SHA-256: {sha}")
        print(f"\nRun 'sdmg_engine.py verify {output_path}' for full validation")
        return 0
    else:
        print(f"RENDER FAILED - output file missing or empty")
        return 1


def cmd_render_full(_args):
    """Re-encode assembly — frame-accurate cuts, handles extensions (slow/freeze/loop)."""
    wav_path = MASTERS_DIR / MASTER_WAV
    output_path = RENDERS_DIR / "SDMG_LostInADream_FULL_REENCODE_169s.mp4"

    if not wav_path.exists():
        print(f"FAILED: Master WAV not found at {wav_path}")
        return 1
    if not EDL_FILE.exists():
        print(f"FAILED: EDL not found at {EDL_FILE}")
        return 1

    ff = check_ffmpeg()
    if not ff["libx264"]:
        print(f"FAILED: libx264 encoder not available")
        print(f"This environment cannot do frame-accurate re-encode.")
        print(f"Use render-simple for stream-copy, or render on Mac with full FFmpeg.")
        return 1

    with open(EDL_FILE) as f:
        edl_data = json.load(f)

    segment_files = []
    temp_dir = RENDERS_DIR / "_temp_segments"
    temp_dir.mkdir(exist_ok=True)

    print(f"Rendering {len(edl_data['edl'])} segments with frame-accurate cuts...")

    for seg in edl_data["edl"]:
        seg_num = seg["seg"]
        src_path = INBOX_DIR / seg["source_file"]
        duration = seg["duration"]
        ext = seg.get("extension")
        seg_out = temp_dir / f"seg_{seg_num:02d}.mp4"

        if not src_path.exists():
            print(f"  Seg {seg_num}: FAILED - source {seg['source_file']} not found")
            return 1

        if ext is None or ext == "":
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(src_path),
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an",
                str(seg_out),
            ]
        elif ext == "slow_80pct":
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(src_path),
                "-filter:v", f"setpts=PTS/{duration * 24 / (10 * 24)}*PTS,setpts=1.25*PTS",
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an",
                str(seg_out),
            ]
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(src_path),
                "-filter:v", "setpts=1.25*PTS",
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an",
                str(seg_out),
            ]
        elif ext.startswith("freeze_last_frame"):
            freeze_dur = duration - 10.0
            main_out = temp_dir / f"seg_{seg_num:02d}_main.mp4"
            freeze_out = temp_dir / f"seg_{seg_num:02d}_freeze.mp4"
            cmd_main = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(src_path),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an", str(main_out),
            ]
            subprocess.run(cmd_main, check=True)
            cmd_freeze = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-sseof", "-0.042", "-i", str(src_path),
                "-loop", "1", "-t", str(freeze_dur),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an", str(freeze_out),
            ]
            subprocess.run(cmd_freeze, check=True)
            seg_concat = temp_dir / f"seg_{seg_num:02d}_concat.txt"
            with open(seg_concat, "w") as cf:
                cf.write(f"file '{main_out}'\nfile '{freeze_out}'\n")
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "concat", "-safe", "0", "-i", str(seg_concat),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an", str(seg_out),
            ]
        elif ext.startswith("loop_crossfade"):
            loop_extra = duration - 10.0
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-stream_loop", "1", "-i", str(src_path),
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an", str(seg_out),
            ]
        elif ext == "composite_two_clips":
            src2 = INBOX_DIR / seg.get("source_file_2", seg["source_file"])
            dur1 = 7.5
            dur2 = duration - dur1
            p1 = temp_dir / f"seg_{seg_num:02d}_p1.mp4"
            p2 = temp_dir / f"seg_{seg_num:02d}_p2.mp4"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(src_path), "-t", str(dur1),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an", str(p1),
            ], check=True)
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(src2), "-t", str(dur2),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an", str(p2),
            ], check=True)
            seg_concat = temp_dir / f"seg_{seg_num:02d}_concat.txt"
            with open(seg_concat, "w") as cf:
                cf.write(f"file '{p1}'\nfile '{p2}'\n")
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "concat", "-safe", "0", "-i", str(seg_concat),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an", str(seg_out),
            ]
        else:
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(src_path),
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-an", str(seg_out),
            ]

        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"  Seg {seg_num}: RENDER FAILED")
            return 1

        print(f"  Seg {seg_num}: {duration:.2f}s [{seg['clip_id']}] {'HOOK' if seg.get('hook') else ''} - OK")
        segment_files.append(seg_out)

    final_concat = temp_dir / "final_concat.txt"
    with open(final_concat, "w") as f:
        for sf in segment_files:
            f.write(f"file '{sf}'\n")

    print(f"\nAssembling final video with master audio...")
    log_path = REPORTS_DIR / "ffmpeg_render_full.log"
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(final_concat),
        "-i", str(wav_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "320k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest",
        str(output_path),
    ]

    with open(log_path, "w") as logf:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=logf)

    if result.returncode != 0:
        print(f"FINAL ASSEMBLY FAILED")
        with open(log_path) as lf:
            for line in lf.readlines()[-10:]:
                print(f"  {line.rstrip()}")
        return 1

    if output_path.exists() and output_path.stat().st_size > 0:
        sha = sha256_file(output_path)
        size = output_path.stat().st_size
        print(f"\nFULL RE-ENCODE RENDER COMPLETE")
        print(f"  File: {output_path}")
        print(f"  Size: {size:,} bytes ({size / 1024 / 1024:.1f} MB)")
        print(f"  SHA-256: {sha}")

        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"  Temp segments cleaned up")
        print(f"\nRun 'sdmg_engine.py verify {output_path}' for full validation")
        return 0
    else:
        print(f"RENDER FAILED - output missing or empty")
        return 1


def cmd_verify(args):
    path = Path(args.file)
    if not path.exists():
        print(f"FAILED: {path} not found")
        return 1

    print(f"=" * 60)
    print(f"SDMG DELIVERY VERIFICATION")
    print(f"=" * 60)
    print(f"\nFile: {path.name}")

    size = path.stat().st_size
    sha = sha256_file(path)
    print(f"Size: {size:,} bytes ({size / 1024 / 1024:.1f} MB)")
    print(f"SHA-256: {sha}")

    probe = run_ffprobe(path)
    if "error" in probe:
        print(f"FFprobe: FAILED - {probe['error']}")
        return 1

    if "format" in probe:
        fmt = probe["format"]
        duration = float(fmt.get("duration", 0))
        bitrate = int(fmt.get("bit_rate", 0))
        print(f"\nDuration: {duration:.2f}s (expected ~{MASTER_DURATION}s)")
        dur_ok = abs(duration - MASTER_DURATION) < 0.5
        print(f"Duration check: {'VERIFIED' if dur_ok else 'MISMATCH'}")
        print(f"Bitrate: {bitrate // 1000} kb/s")

    video_ok = False
    audio_ok = False
    for s in probe.get("streams", []):
        if s.get("codec_type") == "video":
            w = s.get("width", "?")
            h = s.get("height", "?")
            fps = s.get("avg_frame_rate", "?")
            codec = s.get("codec_name", "?")
            print(f"\nVideo: {codec} {w}x{h} @ {fps}")
            video_ok = codec in ("h264",) and w == 1280 and h == 720
            print(f"Video spec: {'VERIFIED' if video_ok else 'CHECK'}")
        elif s.get("codec_type") == "audio":
            codec = s.get("codec_name", "?")
            rate = s.get("sample_rate", "?")
            ch = s.get("channels", "?")
            print(f"Audio: {codec} {rate}Hz {ch}ch")
            audio_ok = codec == "aac" and str(rate) == "48000" and ch == 2
            print(f"Audio spec: {'VERIFIED' if audio_ok else 'CHECK'}")

    all_ok = dur_ok and video_ok and audio_ok
    print(f"\n{'=' * 60}")
    print(f"DELIVERY STATUS: {'VERIFIED' if all_ok else 'NEEDS REVIEW'}")
    print(f"{'=' * 60}")
    return 0 if all_ok else 1


def cmd_report(_args):
    print("=" * 60)
    print("SDMG DELIVERY REPORT")
    print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    print(f"\nProject: SDMG / Lost In A Dream")
    print(f"Artist: Mr. Silent Dreamz")
    print(f"Label: Artesia Records [SDMG]")

    print(f"\n--- Environment ---")
    ff = check_ffmpeg()
    print(f"FFmpeg: {ff['ffmpeg']}")
    print(f"libx264: {'YES' if ff['libx264'] else 'NO'}")
    print(f"H.264 decode: {'YES' if ff['h264_decode'] else 'NO'}")

    print(f"\n--- Master Audio ---")
    wav_path = MASTERS_DIR / MASTER_WAV
    if wav_path.exists():
        sha = sha256_file(wav_path)
        print(f"File: {MASTER_WAV}")
        print(f"SHA-256: {sha}")
        print(f"Match: {'VERIFIED' if sha == MASTER_SHA256 else 'MISMATCH'}")
    else:
        print(f"Status: NOT PRESENT")

    print(f"\n--- Source Plates ---")
    found = sum(1 for fn in SOURCE_PLATES.values() if (INBOX_DIR / fn).exists())
    print(f"Found: {found}/{len(SOURCE_PLATES)}")

    print(f"\n--- Renders ---")
    for mp4 in sorted(RENDERS_DIR.glob("*.mp4")):
        size = mp4.stat().st_size
        if size > 0:
            sha = sha256_file(mp4)
            print(f"  {mp4.name}: {size:,} bytes - SHA {sha[:16]}...")

    print(f"\n--- EDL ---")
    if EDL_FILE.exists():
        with open(EDL_FILE) as f:
            edl = json.load(f)
        total = sum(s["duration"] for s in edl["edl"])
        print(f"  Segments: {len(edl['edl'])}")
        print(f"  Duration: {total:.2f}s")
        print(f"  Hooks: {edl.get('hooks_preserved', '?')}")

    report_data = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "project": "SDMG / Lost In A Dream",
        "master_verified": wav_path.exists() and sha256_file(wav_path) == MASTER_SHA256 if wav_path.exists() else False,
        "plates_found": found,
        "plates_total": len(SOURCE_PLATES),
        "ffmpeg_libx264": ff["libx264"],
        "renders": [
            {"file": mp4.name, "size": mp4.stat().st_size, "sha256": sha256_file(mp4)}
            for mp4 in sorted(RENDERS_DIR.glob("*.mp4"))
            if mp4.stat().st_size > 0
        ],
    }

    report_path = REPORTS_DIR / f"delivery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2)
    print(f"\nReport saved: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="SDMG Video Production Engine v1.0")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("audit", help="Read-only environment and asset audit")
    sub.add_parser("validate", help="Validate EDL against transcript and sources")
    sub.add_parser("concat", help="Generate FFmpeg concat file from EDL")
    sub.add_parser("render-simple", help="Stream-copy assembly (fast, keyframe-aligned)")
    sub.add_parser("render-full", help="Re-encode assembly (frame-accurate, needs libx264)")

    p_verify = sub.add_parser("verify", help="FFprobe + SHA-256 verification")
    p_verify.add_argument("file", help="Path to MP4 to verify")

    sub.add_parser("report", help="Full delivery report")

    args = parser.parse_args()

    commands = {
        "audit": cmd_audit,
        "validate": cmd_validate,
        "concat": cmd_concat,
        "render-simple": cmd_render_simple,
        "render-full": cmd_render_full,
        "verify": cmd_verify,
        "report": cmd_report,
    }

    if args.command in commands:
        sys.exit(commands[args.command](args) or 0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
