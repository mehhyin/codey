# Pyroom

A personal, local Python learning workspace. No accounts, paid APIs, hosted services, or internet connection are needed on this computer.

## Open it later

1. Open this folder in File Explorer.
2. Double-click **Start Pyroom.cmd**. Your default browser will open automatically.
3. Bookmark **http://127.0.0.1:8765**. Run the launcher again after restarting your computer.

Double-click **Stop Pyroom.cmd** to stop the local server when finished. Closing the browser alone leaves the server running. You can create a Windows shortcut to Start Pyroom.cmd using File Explorer.

The launcher uses the Python runtime already present on this computer. If moving the app to another computer, install Python 3.12 or later and pandas (`python -m pip install pandas`), then run `python server.py --open` from this folder. All modules except the pandas module use only Python's standard library.

## Learn

- Pick any lesson in the course outline. All lessons are available immediately.
- Edit main.py. Tab inserts four spaces, and Enter preserves indentation.
- **Run code** executes your Python. **Submit answer** runs the exercise checks and marks the exercise complete if every check passes.
- **Ctrl+Enter** runs code; **Ctrl+Shift+Enter** submits it.
- Reveal hints one at a time. Worked solutions have a separate confirmation and do not automatically complete an exercise.
- Each project consists of independent steps with supplied starting inputs. Earlier projects provide more guidance; later projects use broader briefs.

The course has 9 modules and 118 exercises/project steps: essentials, decisions and loops, collections, functions, files/CSV/JSON, data analysis, pandas, automation, and introductory web concepts. The 72 added exercises include focused practice, debugging tasks, and nine review checkpoints. New exercises have example walkthroughs and common-mistake notes; every exercise has a module reference panel. Existing lesson IDs, drafts, and completions are preserved. The web module teaches HTML generation, query parsing, and response structure; it is an introduction, not a full framework course.

## Your work

Drafts, completion, and revealed hints are saved in this browser's local storage. Use the same browser and the exact same address to resume. Codex's embedded browser and your normal browser have separate storage. Clearing browser data removes this progress. Private browsing does not provide durable progress after its private session ends.

Each Python attempt gets fresh sample files in a disposable practice folder. File-writing exercises are checked before their files are removed. Practice output files are not exported to your personal folders. Use print() to inspect data and generated text.

Python runs on your computer in a separate process with an 8-second time limit and capped captured output. This is **not a security sandbox**: Python code can access local files and system resources permitted to your account. The app is intended for your own learning code, and binds only to 127.0.0.1. It is not designed to host other users or run untrusted programs. input() is not interactive in this version; exercises use named variables and supplied files.

## Troubleshooting

- If the page cannot connect, run Start Pyroom.cmd and refresh it.
- After a server restart, refresh the page before running code.
- If a program times out, check for an endless loop or a long-running operation.
- If pandas is missing on another machine, install it using that machine's Python interpreter.
- Server logs are stored in `../../work/pyroom-runtime/` relative to this folder.

## Source

`server.py` serves the app and runs attempts. `worker.py` executes Python and checks behavior. `course.py` and `course_extra.py` contain editable lessons, checks, and worked solutions. `dist/` contains the interface. There are no JavaScript dependencies or build steps.

## Expanded learning sequence

Each module now has 13 exercises (Python essentials has 14). Work through the short concept lesson, practise its individual parts, fix or combine those ideas, complete the checkpoint, and then try the guided project. The minutes shown are rough activity estimates, not deadlines. Revisit difficult practice before moving on; revealing a solution does not mean the skill has been mastered.

The new curriculum is original. Public curriculum outlines informed the progression and emphasis on repeated coding practice:

- DataCamp Introduction to Python: https://www.datacamp.com/courses/intro-to-python-for-data-science
- DataCamp Intermediate Python: https://www.datacamp.com/courses/intermediate-python
- Dataquest Learn Python path: https://www.dataquest.io/path/learn-python/

No proprietary lesson text, exercises, or solutions were copied. This is a local practice course, not an equivalent replacement for every course offered by those platforms. Additional content lives in course_practice.py, course_practice_more.py, course_practice_applied.py, and course_reference.py.
