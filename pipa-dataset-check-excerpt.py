import os

import soundfile as sf


BASE_DIR = "/Users/qvqyx/PipaPianoData"
SPLITS = {
    "train": range(1, 107),
    "valid": range(107, 123),
    "test": range(123, 133),
}
REQUIRED_STEMS = ["mixture.wav", "pipa.wav", "other.wav"]


def check_stem(track_path, stem):
    stem_path = os.path.join(track_path, stem)

    if not os.path.exists(stem_path):
        return f"Missing: {stem_path}"

    try:
        info = sf.info(stem_path)
    except Exception as error:
        return f"Unreadable: {stem_path} ({error})"

    if info.frames == 0:
        return f"Empty: {stem_path}"

    return None


total_issues = 0

for split, track_range in SPLITS.items():
    split_path = os.path.join(BASE_DIR, split)
    expected = {f"track_{i:04d}" for i in track_range}
    existing = set(os.listdir(split_path)) if os.path.exists(split_path) else set()
    existing = {name for name in existing if not name.startswith(".")}

    issues = []
    issues.extend(f"Missing directory: {name}" for name in expected - existing)
    issues.extend(f"Unexpected directory: {name}" for name in existing - expected)

    for track in sorted(expected & existing):
        track_path = os.path.join(split_path, track)
        for stem in REQUIRED_STEMS:
            issue = check_stem(track_path, stem)
            if issue:
                issues.append(issue)

    total_issues += len(issues)
    print(f"{split}: {len(expected)} expected tracks, {len(issues)} issue(s)")


print(f"Total dataset issues: {total_issues}")
