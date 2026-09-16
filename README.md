# Pyroom

A personal, local Python learning workspace. No accounts, paid APIs, hosted services, or internet connection are needed on this computer.

## Open it later

1. Open this folder in File Explorer.
2. Double-click **Start Pyroom.cmd**. Your default browser will open automatically.
3. Bookmark **http://127.0.0.1:8765**. Run the launcher again after restarting your computer.

Double-click **Stop Pyroom.cmd** to stop the local server when finished. Closing the browser alone leaves the server running. You can create a Windows shortcut to Start Pyroom.cmd using File Explorer.

The launcher uses the Python runtime already present on this computer. NumPy, pandas, Matplotlib, openpyxl, and Flask are installed locally. On another computer, install Python 3.12 or later, run `python -m pip install -r requirements.txt` from this folder, then run `python server.py --open`. Dependency installation needs internet access once; the lessons run offline afterwards. On this computer, additional libraries are in `../../work/pyroom-packages`, loaded by `learning_runtime.py`.

## Learn

- Pick any lesson in the course outline. All lessons are available immediately.
- Every exercise starts with a **blank editor**, including companion Python files. Required values appear under **Exercise inputs** in the instructions; debugging exercises show the broken program separately. Code you wrote stays saved. Untouched drafts matching the old prefilled code are cleared once during this update.
- Write main.py from scratch. Tab inserts four spaces, and Enter preserves indentation. Click a filename above the editor to edit companion files. Reset code clears all code files for that exercise.
- **Run code** executes your Python. **Submit answer** runs the exercise checks and marks the exercise complete if every check passes.
- **Ctrl+Enter** runs code; **Ctrl+Shift+Enter** submits it.
- Reveal hints one at a time. Worked solutions have a separate confirmation and do not automatically complete an exercise.
- Each project consists of independent steps with supplied starting inputs. Earlier projects provide more guidance; later projects use broader briefs.

Use the **Learning track** selector to choose Foundations or Intermediate. All modules are available immediately. Progress is shown for the selected track.

The course has **19 modules and 173 exercises/project steps**:

| Track | Modules | Exercises | Content |
| --- | ---: | ---: | --- |
| Foundations | 9 | 118 | Essentials, decisions and loops, collections, functions, files/CSV/JSON, analysis, pandas, automation, web concepts |
| Intermediate | 10 | 55 | Mixed review, NumPy, Matplotlib, deeper pandas, Excel, SQLite, APIs, reliable programs, Flask, independent projects |

Intermediate projects include a sensor audit, chart dashboard, monthly data report, Excel workbook, SQL export, API report, reusable reporting tool, and local task tracker. Three independent projects combine these skills into a sales reporting pack, batch file audit, and inventory notebook. Recall links revisit relevant earlier exercises. There is no advanced track yet.

## Your work

Drafts, completion, and revealed hints are saved in this browser's local storage. Use the same browser and the exact same address to resume. Codex's embedded browser and your normal browser have separate storage. Clearing browser data removes this progress. Private browsing does not provide durable progress after its private session ends.

Each Python attempt gets fresh sample files in a disposable practice folder. Files are checked before that folder is removed. Charts and declared exports appear under **Output files**, where you can download them to your browser's normal download location. Pyroom does not automatically write reports into personal folders. Up to four open figures are captured; exports are limited to 2 MB each and 6 MB total per attempt. Run again after refreshing to regenerate outputs.

Flask exercises have a **Preview app** button. Start a preview, then click **Open local app** to use it in a browser. Define `app`; do not call `app.run()`. Use `url_for` for form actions and redirects. A preview keeps its database between requests. Starting another preview resets the previous one, and stopping Pyroom closes it. Previews expire after about an hour. API lessons use a local practice server and require no third-party credentials.

Python runs in a separate process with an 8-second limit for Foundations or 20 seconds for Intermediate, and capped captured output. This is **not a security sandbox**: code can access local files and system resources permitted to your account. The app is for your own learning code and binds only to 127.0.0.1. It is not designed to host other users or run untrusted programs. input() is not interactive; exercises use named variables and supplied files.

## Troubleshooting

- If the page cannot connect, run Start Pyroom.cmd and refresh it.
- After a server restart, refresh the page before running code.
- If a program times out, check for an endless loop or a long-running operation.
- If a library is missing on another machine, run `python -m pip install -r requirements.txt` with the Python interpreter used to start Pyroom.
- Server logs are stored in `../../work/pyroom-runtime/` relative to this folder.

## Source

`server.py` serves the app and runs attempts. `worker.py` executes Python and checks behavior. `course.py` and `course_extra.py` contain editable lessons, checks, and worked solutions. `dist/` contains the interface. There are no JavaScript dependencies or build steps.

## Expanded learning sequence

Foundations modules have 13 exercises each (Python essentials has 14). Intermediate starts with four mixed reviews, followed by eight modules of six exercises each and three independent projects. Work through concepts, practise individual parts, and combine them in projects. The minutes shown are estimates, not deadlines. Revisit difficult exercises; revealing a solution does not mean the skill has been mastered.

The new curriculum is original. Public curriculum outlines informed the progression and emphasis on repeated coding practice:

- DataCamp Introduction to Python: https://www.datacamp.com/courses/intro-to-python-for-data-science
- DataCamp Intermediate Python: https://www.datacamp.com/courses/intermediate-python
- Dataquest Learn Python path: https://www.dataquest.io/path/learn-python/

No proprietary lesson text, exercises, or solutions were copied. This is a local practice course, not an equivalent replacement for every course offered by those platforms. Additional content lives in course_practice.py, course_practice_more.py, course_practice_applied.py, and course_reference.py.

Intermediate content lives in `intermediate.py`, `intermediate_data.py`, and `intermediate_apps.py`. Run `python tests/test_course.py` to check all 173 solutions, empty submissions, and runtime errors. Run `python tests/test_workspace.py` to check blank-editor metadata, downloads, multiple files, local previews, and HTTP validation. Neither test changes your browser progress.
