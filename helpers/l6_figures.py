"""Supplied display helpers for Lab 6 opening sections.

These helpers draw supplied summaries and observations. They do not sample,
score responses, join tables, choose bands, or change analysis eligibility.
They require Pillow and return PIL images suitable for notebook display.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


INK = "#243746"
MUTED = "#4e626f"
GRID = "#dce3e7"
COLORS = ["#176b93", "#a34d34", "#6b5a9b", "#32745b"]
COI_LABELS = {1: "Very low", 2: "Low", 3: "Moderate", 4: "High", 5: "Very high"}


def _font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu") / (
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        ),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


def _text(draw, xy, value, size=22, bold=False, fill=INK, anchor=None):
    draw.text(xy, str(value), font=_font(size, bold), fill=fill, anchor=anchor)


def _linewrap(draw, xy, value, max_width, size=20, fill=MUTED, spacing=7):
    """Draw text within a known width; return the bottom y coordinate."""
    x, y = xy
    line = ""
    for word in str(value).split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=_font(size)) > max_width and line:
            _text(draw, (x, y), line, size, fill=fill)
            y += size + spacing
            line = word
        else:
            line = trial
    if line:
        _text(draw, (x, y), line, size, fill=fill)
        y += size + spacing
    return y


def _safe_number(value):
    try:
        return float(value) if pd.notna(value) else math.nan
    except (ValueError, TypeError):
        return math.nan


def _axis(draw, left, right, y, maximum, ticks, label, size=19):
    draw.line((left, y, right, y), fill=INK, width=2)
    for tick in ticks:
        x = left + tick / maximum * (right - left)
        draw.line((x, y, x, y + 6), fill=INK, width=2)
        _text(draw, (x, y + 13), f"{tick:g}", size, anchor="mt")
    _text(draw, ((left + right) / 2, y + 48), label, 21, anchor="mt")


def discovery_figure(summary, samples,
                     days_field="instructional_cannabis_days_30d",
                     band_field="ace_band", *,
                     dataset_version="0.6.0-rc1", realization=0):
    """Draw any-use rates and positive-day observations for supplied samples.

    ``summary`` columns: sample, ace_band, usable_n, users, any_use_pct,
    mean_days_all. ``samples`` maps A (and optionally B) to supplied frames.
    Omitted samples are never accessed or displayed, supporting prediction
    before revealing the second sample. Nonusers contribute to occurrence
    denominators; the lower panel explicitly displays users only.
    """
    keys = list(samples)
    if not keys or len(keys) > 2:
        raise ValueError("Supply one or two exploration samples.")
    required = {"sample", "ace_band", "usable_n", "users", "any_use_pct"}
    if not required.issubset(summary.columns):
        raise ValueError(f"Missing summary columns: {sorted(required-set(summary.columns))}")
    panel_width = 760
    width = panel_width * len(keys) + 40
    # Fixed six-pixel spacing preserves an actual one-dot-per-user display.
    # Allocate enough height for the largest tie stack in either sample;
    # rows therefore stay aligned across A/B without overplotting dense ties.
    first_rows = summary.loc[summary["sample"].astype(str).eq(str(keys[0]))]
    ordered_bands = first_rows["ace_band"].astype(str).tolist()
    row_centers = {}
    cursor = 739
    for band in ordered_bands:
        max_tie = 0
        for key in keys:
            frame = samples[key]
            if not {days_field, band_field}.issubset(frame.columns):
                raise ValueError("Samples lack the requested days/band columns.")
            values = pd.to_numeric(frame.loc[frame[band_field].astype(str).eq(band), days_field], errors="coerce")
            ties = values.loc[values.gt(0)].value_counts()
            max_tie = max(max_tie, int(ties.max()) if len(ties) else 0)
        row_height = max(58, max(0, max_tie - 1) * 6 + 26)
        row_centers[band] = cursor + row_height / 2
        cursor += row_height
    lower_axis_y = cursor + 15
    height = int(lower_axis_y + 140)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    _text(draw, (35, 23), "Cannabis use across ACE10 count bands", 31, True)
    cohort_label = "production 0" if realization == 0 else f"realization {realization}"
    _linewrap(draw, (35, 68),
              "All participants and values are fictional",
              width - 70, 19, spacing=3)
    _linewrap(draw, (35, 105),
              "Two descriptive questions: how common is use, and how are use-days distributed among users?",
              width - 70, 20)
    available = summary.loc[summary["sample"].astype(str).isin([str(k) for k in keys])]
    rate_max = pd.to_numeric(available["any_use_pct"], errors="coerce").max()
    maximum = max(10, int(math.ceil((float(rate_max) if pd.notna(rate_max) else 0) / 5) * 5 + 5))
    maximum = min(100, maximum)
    step = 5 if maximum <= 35 else 10 if maximum <= 70 else 20
    ticks = list(range(0, maximum + 1, step))
    if ticks[-1] != maximum:
        ticks.append(maximum)
    for column, key in enumerate(keys):
        rows = summary.loc[summary["sample"].astype(str).eq(str(key))].copy()
        if rows.empty:
            raise ValueError(f"No summary for sample {key}.")
        if rows["ace_band"].astype(str).duplicated().any():
            raise ValueError("Each sample/band must have exactly one summary row.")
        frame = samples[key]
        if not {days_field, band_field}.issubset(frame.columns):
            raise ValueError("Samples lack the requested days/band columns.")
        bands = rows["ace_band"].astype(str).tolist()
        if bands != ordered_bands:
            raise ValueError("Use identical ordered ACE bands in every displayed sample.")
        if len(bands) > 5:
            raise ValueError("The opening display supports at most five prespecified bands.")
        xbase = 35 + column * panel_width
        left, right = xbase + 72, xbase + 590
        usable_total = int(pd.to_numeric(rows["usable_n"]).sum())
        _text(draw, (xbase, 163), f"Sample {key} | {len(frame):,} sampled; {usable_total:,} usable", 24, True)
        _text(draw, (xbase, 205), "Occurrence: percentage reporting any broad cannabis use", 20)
        _text(draw, (xbase, 238), "ACE10 band", 18, True)
        top_y = 288
        row_step = min(70, 210 / max(1, len(bands) - 1))
        for tick in ticks:
            x = left + tick / maximum * (right - left)
            draw.line((x, 270, x, 540), fill=GRID, width=1)
        for i, (_, row) in enumerate(rows.iterrows()):
            y = top_y + i * row_step
            band = str(row["ace_band"])
            n, k = int(row["usable_n"]), int(row["users"])
            rate = _safe_number(row["any_use_pct"])
            _text(draw, (left - 20, y), band, 22, True, anchor="rm")
            color = COLORS[i % len(COLORS)]
            if n == 0 or not math.isfinite(rate):
                _text(draw, (left + 10, y), "No available observations", 19, anchor="lm")
            else:
                x = left + rate / maximum * (right - left)
                draw.ellipse((x-6, y-6, x+6, y+6), fill=color)
                label = f"{rate:.1f}%  ({k}/{n})"
                # Keep labels inside the panel even for a high rate.
                label_width = draw.textlength(label, font=_font(19))
                if x + 14 + label_width < xbase + panel_width - 8:
                    _text(draw, (x + 14, y), label, 19, anchor="lm")
                else:
                    _text(draw, (x - 14, y - 16), label, 19, anchor="rm")
        _axis(draw, left, right, 547, maximum, ticks, "Any broad cannabis use (%)")
        _text(draw, (xbase, 635), "Use-days among users only", 24, True)
        _linewrap(draw, (xbase, 673),
                  "Each dot is one user. Nonusers are omitted here and remain in the occurrence denominator above.",
                  panel_width - 45, 19, spacing=5)
        for i, band in enumerate(bands):
            y = row_centers[band]
            color = COLORS[i % len(COLORS)]
            _text(draw, (left - 20, y), band, 22, True, anchor="rm")
            group = pd.to_numeric(frame.loc[frame[band_field].astype(str).eq(band), days_field], errors="coerce")
            positive = group.loc[group.gt(0)].dropna()
            if ((positive < 1) | (positive > 30)).any():
                raise ValueError("Positive use-days must be within 1–30.")
            k = len(positive)
            if not k:
                _text(draw, (left + 12, y), "No observed users", 19, anchor="lm")
            for day, count in positive.value_counts().sort_index().items():
                count = int(count)
                x = left + float(day) / 30 * (right - left)
                # Symmetric tie stacks; no randomness and no slope by sorted rank.
                offsets = (np.arange(count) - (count - 1) / 2) * 6
                radius = 2.3
                for offset in offsets:
                    draw.ellipse((x-radius, y+offset-radius, x+radius, y+offset+radius), fill=color)
            note = f"users={k}" + ("*" if 0 < k < 10 else "")
            _text(draw, (right + 12, y), note, 18, anchor="lm")
        _axis(draw, left, right, lower_axis_y, 30, [0, 5, 10, 15, 20, 25, 30], "Broad cannabis use-days")
    _linewrap(draw, (35, height - 55),
              "* Fewer than 10 users: interpret the displayed distribution cautiously. Descriptive sample results.",
              width - 70, 17, spacing=3)
    return image


def coi_figure(summary, *, sample="A", dataset_version="0.6.0-rc1", realization=0):
    """Display fixed ACE10 bands as 100% stacked bars for one supplied sample.

    Each of five COI levels retains its own usable denominator. Required
    columns are sample, coi_level, n, and n_*/pct_* for 0, 1, 2_3, 4_plus.
    The default reveals Sample A only. Pass sample="B" for a later review.
    """
    band_keys = ["0", "1", "2_3", "4_plus"]
    band_labels = ["0", "1", "2–3", "4+"]
    required = {"sample", "coi_level", "n"}
    required.update(f"{prefix}_{key}" for prefix in ["n", "pct"] for key in band_keys)
    if not required.issubset(summary.columns):
        raise ValueError(f"Missing COI columns: {sorted(required-set(summary.columns))}")
    rows = summary.loc[summary["sample"].astype(str).eq(str(sample))].copy()
    rows["coi_level"] = pd.to_numeric(rows["coi_level"], errors="raise")
    if rows["coi_level"].duplicated().any():
        raise ValueError("Each COI level needs exactly one summary row per sample.")
    if set(rows["coi_level"]) != set(range(1,6)):
        raise ValueError("Supply all five COI levels, including n=0 rows, for the requested sample.")
    rows = rows.set_index("coi_level")
    for level in range(1,6):
        row = rows.loc[level]
        n = _safe_number(row["n"])
        counts = np.array([_safe_number(row[f"n_{key}"]) for key in band_keys])
        percentages = np.array([_safe_number(row[f"pct_{key}"]) for key in band_keys])
        if (not math.isfinite(n) or n < 0 or n != math.floor(n)
                or not np.isfinite(counts).all() or (counts < 0).any()
                or not np.equal(counts, np.floor(counts)).all() or counts.sum() != n):
            raise ValueError("ACE10 band counts must be nonnegative integers summing to the usable n.")
        if n == 0:
            if not np.isnan(percentages).all():
                raise ValueError("A COI level with n=0 must have missing percentages, not zero percentages.")
        elif not np.isfinite(percentages).all() or not np.allclose(percentages, 100*counts/n, rtol=0, atol=1e-8):
            raise ValueError("ACE10 band percentages must use the supplied usable n.")

    image = Image.new("RGB", (1540, 900), "white")
    draw = ImageDraw.Draw(image)
    _text(draw, (35, 25), f"Sample {sample}: ACE10 bands across historical COI levels", 31, True)
    _text(draw, (35, 72), "COI 2.0 | National reference | Source year 2015 | Geography 2010", 21)
    cohort_label = "production 0" if realization == 0 else f"realization {realization}"
    _text(draw, (35, 108),
          "All participants and observations are fictional", 20)
    _text(draw, (35, 145), "Each row uses participants with both a usable ACE10 score and that historical COI level.", 21)
    for i, (label, color) in enumerate(zip(band_labels, COLORS)):
        x = 35 + i*365
        draw.rectangle((x, 196, x+25, 221), fill=color)
        _text(draw, (x+36, 208), f"{label} ACE categories", 21, anchor="lm")
    left, right = 240, 920
    count_centers = [1025, 1160, 1295, 1430]
    _text(draw, (35, 254), "Historical COI", 20, True)
    _text(draw, ((left+right)/2, 250), "Percentage within each COI level", 21, True, anchor="mt")
    _text(draw, ((count_centers[0]+count_centers[-1])/2, 244), "Count (percentage) in each ACE10 band", 20, True, anchor="mt")
    for x, band in zip(count_centers, band_labels):
        _text(draw, (x, 275), band, 20, True, anchor="mt")
    for tick in [0, 20, 40, 60, 80, 100]:
        x = left + tick/100*(right-left)
        draw.line((x, 310, x, 736), fill=GRID)
    descriptions = []
    for i, level in enumerate(range(1, 6)):
        y = 341 + i*91
        row = rows.loc[level]
        n = int(row["n"])
        _text(draw, (35, y-18), COI_LABELS[level], 23, True)
        _text(draw, (35, y+12), f"usable n={n:,}" + ("*" if 0 < n < 20 else ""), 19, fill=MUTED)
        if n == 0:
            draw.rectangle((left, y-27, right, y+27), outline=GRID, width=2)
            _text(draw, ((left+right)/2, y), "No usable observations — percentage undefined", 20, anchor="mm", fill=MUTED)
            for x in count_centers:
                _text(draw, (x, y-10), "0", 21, anchor="mm")
                _text(draw, (x, y+16), "—", 19, anchor="mm", fill=MUTED)
            descriptions.append(f"{COI_LABELS[level]}: n=0; percentages undefined.")
            continue
        cumulative = 0.0
        bands_description = []
        for key, label, color, count_x in zip(band_keys, band_labels, COLORS, count_centers):
            count, percentage = int(row[f"n_{key}"]), float(row[f"pct_{key}"])
            start = left + cumulative/100*(right-left)
            cumulative += percentage
            end = left + cumulative/100*(right-left)
            if count:
                draw.rectangle((start, y-27, end, y+27), fill=color)
                if start > left:
                    draw.line((start, y-27, start, y+27), fill="white", width=2)
                # Tiny bands remain visible without forcing overlapping labels.
                # Their exact counts and percentages are always printed at right.
                if end-start >= draw.textlength(label, font=_font(21, True))+18:
                    _text(draw, ((start+end)/2, y), label, 21, True, fill="white", anchor="mm")
            _text(draw, (count_x, y-10), f"{count:,}", 22, True, anchor="mm")
            _text(draw, (count_x, y+16), f"({percentage:.1f}%)", 19, anchor="mm", fill=MUTED)
            bands_description.append(f"{label}: {count} ({percentage:.1f}%)")
        descriptions.append(f"{COI_LABELS[level]}: n={n}; " + ", ".join(bands_description) + ".")
    _axis(draw, left, right, 747, 100, [0, 20, 40, 60, 80, 100], "Participants in each ACE10 band (%)")
    _text(draw, (35, 831), "Bars sum to 100% within each usable group. Fixed ACE10 bands: 0, 1, 2–3, 4+; no pooling.", 20)
    _text(draw, (35, 865), "Descriptive sample proportions, not confidence intervals. * Fewer than 20 observations; interpret cautiously.", 19)
    image.info["description"] = (
        f"Sample {sample}: 100% stacked ACE10 bands across all five historical COI levels. "
        f"Fictional data; COI 2.0, national, 2015, 2010 geography. "
        "Each denominator includes usable ACE10 and COI values. No pooling or resampling. "
        + " ".join(descriptions))
    return image
