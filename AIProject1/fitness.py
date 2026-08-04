from dataset import ENROLLMENTS, get_day, PREFERRED_MAX_DAYS

SAME_SLOT = 1000
SAME_DAY = 50
TOO_MANY = 800
FOUR_IN_TWO_DAYS = 500
EXTRA_DAYS = 100

def compute_penalty(schedule):

    penalty = 0
    student_slots = {}
    for student, courses in ENROLLMENTS.items():

        slots = []
        for c in courses:
            if c in schedule:
                slots.append(schedule[c])
        student_slots[student] = slots

    # 1. same slot conflict (HARD)
    for slots in student_slots.values():
        counts = {}
        for s in slots:
            counts[s] = counts.get(s, 0) + 1

        for v in counts.values():
            if v > 1:
                penalty += (v * (v - 1) // 2) * SAME_SLOT

    # 2. same day / too many exams
    for slots in student_slots.values():
        day_count = {}
        for s in slots:
            d = get_day(s)
            day_count[d] = day_count.get(d, 0) + 1

        for v in day_count.values():

            if v >= 2:
                penalty += (v * (v - 1) // 2) * SAME_DAY

            if v > 2:
                penalty += (v - 2) * TOO_MANY

    # 3. 4 exams in 2 consecutive days
    for slots in student_slots.values():

        day_count = {}

        for s in slots:
            d = get_day(s)
            day_count[d] = day_count.get(d, 0) + 1

        days = sorted(day_count.keys())

        for i in range(len(days) - 1):
            if days[i + 1] == days[i] + 1:
                total = day_count[days[i]] + day_count[days[i + 1]]
                if total >= 4:
                    penalty += FOUR_IN_TWO_DAYS

    used_days = set(get_day(s) for s in schedule.values())
    extra = max(0, len(used_days) - PREFERRED_MAX_DAYS)
    penalty += extra * EXTRA_DAYS
    return penalty

def fitness(schedule):
    return -compute_penalty(schedule)