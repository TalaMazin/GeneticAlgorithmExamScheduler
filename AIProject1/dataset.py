import os
import pandas as pd

_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "ga_exam_timetable_dataset.xlsx")
EXCEL_PATH = os.environ.get("GA_DATASET_PATH", _DEFAULT_PATH)

def _load_excel() -> dict:
    if not os.path.exists(EXCEL_PATH):
        raise FileNotFoundError(
            f"Dataset not found at: {EXCEL_PATH}\n"
            f"Copy ga_exam_timetable_dataset.xlsx next to dataset.py, "
            f"or set the GA_DATASET_PATH environment variable."
        )
    return pd.read_excel(EXCEL_PATH, sheet_name=None, dtype=str)


_sheets = _load_excel()

_cat = _sheets["Course_Catalog"]
COURSES: list[str] = _cat["Course_Code"].str.strip().tolist()
COURSE_ENROLLMENT: dict[str, int] = {
    row["Course_Code"].strip(): int(row["Enrollment"])
    for _, row in _cat.iterrows()
}

_slots_df = _sheets["Exam_Slots"]
EXAM_SLOTS: dict[str, dict] = {}
for _, row in _slots_df.iterrows():
    sid = str(row["Slot_ID"]).strip()
    if not sid or sid == "nan":
        continue
    EXAM_SLOTS[sid] = {
        "day":   int(row["Exam_Day"]),
        "slot":  int(row["Slot_Number"]),
        "time":  str(row["Time"]).strip(),
    }

ALL_SLOT_IDS: list[str] = list(EXAM_SLOTS.keys())   # D1S1 .. D6S3

_params_df = _slots_df[["Parameter", "Value"]].dropna(subset=["Parameter"])
_params: dict[str, float] = {}
for _, row in _params_df.iterrows():
    key = str(row["Parameter"]).strip()
    try:
        _params[key] = float(row["Value"])
    except (ValueError, TypeError):
        pass

PREFERRED_MAX_DAYS: int = int(_params.get("Preferred max used days", 5))
HARD_MAX_PER_DAY:   int = int(_params.get("Hard max exams/student/day", 2))


_pairs_df = _sheets["Enrollment_Pairs"]
ENROLLMENTS: dict[str, list[str]] = {}      # student_id -> [course, ...]
COURSE_STUDENTS: dict[str, list[str]] = {c: [] for c in COURSES}

for _, row in _pairs_df.iterrows():
    sid  = str(row["Student_ID"]).strip()
    code = str(row["Course_Code"]).strip()
    if sid == "nan" or code == "nan":
        continue
    ENROLLMENTS.setdefault(sid, []).append(code)
    if code in COURSE_STUDENTS:
        COURSE_STUDENTS[code].append(sid)

NUM_STUDENTS:             int = len(ENROLLMENTS)
TOTAL_ENROLLMENT_RECORDS: int = len(_pairs_df.dropna(subset=["Student_ID"]))

_bad_df = _sheets["Sample_Bad_Schedule"]
BAD_SCHEDULE: dict[str, str] = {
    str(row["Course_Code"]).strip(): str(row["Assigned_Slot_ID"]).strip()
    for _, row in _bad_df.iterrows()
    if str(row.get("Course_Code", "nan")).strip() not in ("nan", "")
}

def get_day(slot_id: str) -> int:
    return EXAM_SLOTS[slot_id]["day"]

def get_slot_number(slot_id: str) -> int:
    return EXAM_SLOTS[slot_id]["slot"]

def get_time(slot_id: str) -> str:
    return EXAM_SLOTS[slot_id]["time"]


if __name__ == "__main__":
    print(f"Excel file        : {EXCEL_PATH}")
    print(f"Courses           : {len(COURSES)}  -> {COURSES}")
    print(f"Students          : {NUM_STUDENTS}")
    print(f"Enrollment records: {TOTAL_ENROLLMENT_RECORDS}")
    print(f"Exam slots        : {len(EXAM_SLOTS)}  -> {ALL_SLOT_IDS}")
    print(f"Preferred max days: {PREFERRED_MAX_DAYS}")
    print(f"Hard max/day      : {HARD_MAX_PER_DAY}")
    print(f"Bad schedule keys : {list(BAD_SCHEDULE.keys())[:5]} ...")