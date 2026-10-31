"""Executive board terms.

The first board was Spring 2026. After that, boards run for a full academic
year (Fall 2026 - Spring 2027, Fall 2027 - Spring 2028, ...). A term is stored
on TeamMember as a short key: 'spring-2026', 'fall-2026', 'fall-2027', ...
"""
import datetime

FIRST_FALL_YEAR = 2026
FIRST_TERM = 'spring-2026'


def term_label(key):
    season, _, year = key.partition('-')
    if season == 'spring':
        return f'Spring {year}'
    return f'Fall {year} – Spring {int(year) + 1}'


def current_term(today=None):
    """The board in office today. Fall terms start in August."""
    today = today or datetime.date.today()
    fall_year = today.year if today.month >= 8 else today.year - 1
    if fall_year < FIRST_FALL_YEAR:
        return FIRST_TERM
    return f'fall-{fall_year}'


def all_terms(today=None):
    """Every term from Spring 2026 through next year's board, oldest first."""
    last_fall = int(current_term(today).rpartition('-')[2])
    if current_term(today) == FIRST_TERM:
        last_fall = FIRST_FALL_YEAR - 1
    keys = [FIRST_TERM] + [f'fall-{y}' for y in range(FIRST_FALL_YEAR, last_fall + 2)]
    return [(key, term_label(key)) for key in keys]


def current_term_key():
    """Callable default for the model field."""
    return current_term()


def term_status(key, today=None):
    """'current', 'past' or 'upcoming' relative to the board in office."""
    keys = [k for k, _ in all_terms(today)]
    current = current_term(today)
    if key == current:
        return 'current'
    return 'past' if keys.index(key) < keys.index(current) else 'upcoming'
