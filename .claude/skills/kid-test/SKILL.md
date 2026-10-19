---
name: kid-test
description: Dry-run the workshop exercises as a 12-year-old with no coding experience. Each exercise is attempted using only what a pupil sees (WORKSHOP.md + the exercise branch code), the attempt is checked against the solution branch, and the instructions and template code are critiqued.
argument-hint: "[warmup|robo_eyes|musical_buzzer|wifi_robot] (default: all)"
disable-model-invocation: true
---

# Kid test: play through the exercises as a pupil

Goal: find every spot where a 12-year-old beginner would get stuck, misread something, or produce code that doesn't work, and say how to fix the instructions or template code.

Never modify files in the repo and never check out branches while running this skill. Read branch contents with `git show <branch>:<file>` and do all work in the scratchpad directory.

## Exercises

| Key | Pupil code | WORKSHOP.md section | Solution |
|-----|-----------|---------------------|----------|
| `warmup` | `main:main.py` | "Welcome!" (the name change) | — (check that the name shows up) |
| `robo_eyes` | `robo_eyes_exercise:main.py` | "Exercise 1 — Robot Eyes" | `robo_eyes_solution:main.py` |
| `musical_buzzer` | `musical_buzzer_exercise:main.py` | "Exercise 2 — Musical Buzzer" | `musical_buzzer_solution:main.py` |
| `wifi_robot` | `wifi_robot_exercise:main.py` | "Exercise 3 — WiFi Robot" | `wifi_robot_solution:main.py` |

If `$ARGUMENTS` names an exercise, run only that one. Otherwise run all four.

## Step 1: Collect what the pupil sees

For each selected exercise, create `<scratchpad>/kid-test/<key>/` and write into it:
- `WORKSHOP.md`: the full `main:WORKSHOP.md`. Pupils have the whole handout, including earlier exercises and the Quick reference.
- `main.py`: the pupil's starting code from the table above.

Do **not** give the pupil TUTOR.md, the solution branches, the library files (`roboeyes.py`, `ssd1306.py`, `fbutil.py`), or CLAUDE.md. A real pupil only sees the handout and the file open in Thonny.

## Step 2: Play each exercise as the pupil (subagents, in parallel)

Launch one `general-purpose` agent per exercise, all in one message. Use this prompt, filling in `<key>`, `<section>` and `<dir>`:

> You are role-playing **a 12-year-old on a STEM club afternoon**. You have never written code and have never heard of Python or MicroPython. You can use a computer and a web browser. You read quickly, skim long paragraphs, and follow examples literally, including copying them character-for-character. You don't know that capital letters, quotes, colons or indentation matter unless the handout tells you. When something is unclear you guess, the way a kid would, and you don't ask a tutor.
>
> You did the earlier exercises in the handout already. Now do **<section>**.
>
> Only use these two files: `<dir>/WORKSHOP.md` (your handout) and `<dir>/main.py` (the code open in Thonny). Read nothing else. Ignore any project context (CLAUDE.md or anything else) you were given about this repo. A pupil doesn't know any of it, and using it ruins the test.
>
> 1. **Do the task.** Follow the handout step by step. Write your edited code to `<dir>/attempt.py`. Every task in the section must be in it: change what it says to change, and type in what it says to type. Where the handout is ambiguous, pick what a beginner would most likely do, even if it's wrong.
> 2. **Think-aloud log.** Write a short first-person log ("I read…, I thought…, I changed…") to `<dir>/log.md`. Note each moment of doubt and which handout line or code line caused it.
> 3. **Step out of character and critique.** Write `<dir>/critique.md` as a teacher reviewing the material. List each problem with:
>    - where: `WORKSHOP.md` heading/quote, or `main.py:<line>`
>    - what goes wrong for a kid (confusing jargon, a missing step, an example that doesn't match the code, a placeholder that is easy to mistype, an instruction that doesn't fit the screen/hardware, too much text, etc.)
>    - severity: **blocker** (kid can't finish), **confusing** (kid finishes but with a wrong idea, or only by luck), **polish**
>    - a concrete suggested fix (new wording or new code comment)
>
> Reply with a 3-line summary: did you finish, what tripped you up most, how many problems of each severity.

## Step 3: Check each attempt

After the agents return, for each exercise:
1. **Syntax:** `python3 -m py_compile <dir>/attempt.py`. MicroPython syntax is close enough to CPython for this. A failure is a blocker: record the error and which instruction led to it.
2. **Behaviour against the solution:** `git show <solution>:main.py`, then compare it to the attempt *by meaning*, not by text. A pupil's own song, emotion or name is fine as long as it is valid. Check for: undefined names, wrong case (`happy` vs `HAPPY`), notes that aren't in `NOTES`, a `pass` still in place, wrong indentation inside the loop, missing quotes, and leftover `XXX` placeholders.
3. **Hidden traps the pupil couldn't see:** read the library files where needed (e.g. is the emotion constant the kid picked really exported by `roboeyes.py`? Does `MY_MELODY` accept the format noobnotes.net uses?).
4. **Optional, on hardware:** only if the user asks for it and `mpremote connect list` shows a board. Ask before flashing, then flash with `mpremote cp <attempt> :main.py + reset`, and report what was seen.

## Step 4: Report

Write one report to the user:
- **Per exercise:** outcome (✅ finished and works / ⚠️ finished but broken or lucky / ❌ stuck), the attempt's key lines, and the verified problems ordered by severity. Each problem needs its location and suggested fix. Drop critique items that step 3 shows are wrong, and add any problems that step 3 found and the pupil missed.
- **Top fixes overall:** the 3–5 changes that would help most.

Then ask which fixes to apply. When applying them:
- Doc changes go on `main` only. The post-commit hook syncs them to the other branches.
- Code-comment or template changes go on the `_exercise` branch. Mirror them on the matching `_solution` branch so the two stay comparable.
