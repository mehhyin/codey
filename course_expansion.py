"""Original extension curriculum; reference outlines are documented in README."""
from textwrap import dedent


def code(text):
    return dedent(text).strip() + '\n' if text.strip() else ''


def extend_courses(module, task):
    def section(id, title, description, project, track, reference, review):
        m = module(id, title, description, project)
        m.update(track=track, reference=reference)
        m['_review'] = review
        return m

    def unit(m, slug, title, concept, example, goals, solution, checks, hints,
             explanation, *, starter='', files=None, setup='', exports=None,
             kind='lesson', minutes=20):
        task(m, slug, title, concept, code(example), goals, code(starter),
             code(solution), [(label, code(test)) for label, test in checks],
             hints, explanation, kind=kind, minutes=minutes, files=files)
        m['tasks'][-1].update(review=m['_review'], time_limit=25,
                              setup=code(setup), exports=exports or [],
                              editor_files={}, solution_files={})
        return m['tasks'][-1]

    from course_advanced import extend_advanced
    from course_analytics import extend_analytics
    extend_advanced(section, unit)
    extend_analytics(section, unit)
