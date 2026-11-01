import { useEffect, useMemo, useState } from 'react'
import { getCurriculum } from '../../api/curriculum'
import Badge from '../../components/ui/Badge'
import Input from '../../components/ui/Input'
import Select from '../../components/ui/Select'
import Spinner from '../../components/ui/Spinner'

const SEMESTERS = [1, 2, 3, 4, 5, 6, 7, 8]

// Pick a course from the programme's hardcoded curriculum (app/core/curriculum.py).
// `value` / `onChange` carry `{ course, semester }` -- the catalog entry plus the
// semester it will be offered in (electives can sit in more than one semester).
export default function CurriculumPicker({ programId, existingCourses, value, onChange, onUseManual }) {
  const [catalog, setCatalog] = useState(null)
  const [semester, setSemester] = useState(1)
  const [search, setSearch] = useState('')

  useEffect(() => {
    if (!programId) return
    setCatalog(null)
    onChange(null)
    getCurriculum(programId).then(setCatalog)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [programId])

  const courses = useMemo(() => catalog?.courses ?? [], [catalog])
  const query = search.trim().toLowerCase()
  const visible = useMemo(() => {
    const list = query
      ? courses.filter((c) => c.code.toLowerCase().includes(query) || c.name.toLowerCase().includes(query))
      : courses.filter((c) => c.semesters.includes(semester))
    // Core courses first, then electives grouped by pool.
    return [...list].sort((a, b) => (a.category === b.category ? 0 : a.category === 'core' ? -1 : 1))
  }, [courses, query, semester])

  const countFor = (s) => courses.filter((c) => c.semesters.includes(s)).length

  function alreadyAdded(course, sem) {
    return existingCourses.some(
      (c) =>
        String(c.program_id) === String(programId) &&
        c.code.trim().toLowerCase() === course.code.toLowerCase() &&
        c.semester === sem,
    )
  }

  function pick(course) {
    const sem = !query && course.semesters.includes(semester) ? semester : course.semesters[0]
    onChange({ course, semester: sem })
  }

  if (catalog === null) {
    return (
      <div className="flex justify-center py-10">
        <Spinner />
      </div>
    )
  }

  if (courses.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-border-strong px-4 py-6 text-center">
        <p className="text-sm text-ink-700">This programme has no curriculum on file yet.</p>
        <button
          type="button"
          onClick={onUseManual}
          className="mt-2 text-sm font-medium text-brand-600 hover:text-brand-700"
        >
          Enter the course manually →
        </button>
      </div>
    )
  }

  const selected = value?.course

  return (
    <div className="flex flex-col gap-3">
      {catalog.source_program_code && catalog.source_program_code !== catalog.program_code && (
        <p className="text-xs text-ink-500 bg-slate-50 rounded-lg px-3 py-2">
          {catalog.program_code} doesn&apos;t have its own curriculum yet, so these are the{' '}
          {catalog.source_program_code} courses.
        </p>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <Select
          label="Semester"
          value={semester}
          onChange={(e) => setSemester(Number(e.target.value))}
          disabled={!!query}
        >
          {SEMESTERS.map((s) => (
            <option key={s} value={s}>
              Semester {s} ({countFor(s)} courses)
            </option>
          ))}
        </Select>
        <Input
          label="Search all semesters"
          placeholder="e.g. Operating Systems"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="max-h-72 overflow-y-auto border border-border rounded-lg divide-y divide-border">
        {visible.length === 0 && (
          <p className="px-3 py-4 text-sm text-ink-500">No courses match that search.</p>
        )}
        {visible.map((course) => {
          const sem = !query && course.semesters.includes(semester) ? semester : course.semesters[0]
          const added = alreadyAdded(course, sem)
          const isSelected = selected?.code === course.code
          return (
            <label
              key={course.code}
              className={`flex items-start gap-3 px-3 py-2.5 text-sm ${
                added ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:bg-slate-50'
              } ${isSelected ? 'bg-brand-50' : ''}`}
            >
              <input
                type="radio"
                name="catalog-course"
                className="mt-0.5 h-4 w-4 text-brand-600 focus:ring-brand-500"
                checked={isSelected}
                disabled={added}
                onChange={() => pick(course)}
              />
              <span className="flex-1 min-w-0">
                <span className="flex flex-wrap items-center gap-x-2 gap-y-1">
                  <span className="font-medium text-brand-700">{course.code}</span>
                  <span className="text-ink-900">{course.name}</span>
                </span>
                <span className="flex flex-wrap items-center gap-1.5 mt-1">
                  {course.category === 'elective' && <Badge tone="brand">{course.group}</Badge>}
                  {course.alternative_to && <Badge tone="warning">Alternative to {course.alternative_to}</Badge>}
                  {query && (
                    <span className="text-xs text-ink-500">Semester {course.semesters.join(' / ')}</span>
                  )}
                  {added && <span className="text-xs text-ink-500">Already added</span>}
                </span>
              </span>
              <span className="text-xs text-ink-500 whitespace-nowrap">
                {course.credit_hours} cr ({course.breakdown})
              </span>
            </label>
          )
        })}
      </div>

      {selected && selected.semesters.length > 1 && (
        <div className="flex items-center gap-2 text-sm text-ink-700">
          <span>Offer {selected.code} in</span>
          <Select
            value={value.semester}
            onChange={(e) => onChange({ course: selected, semester: Number(e.target.value) })}
            className="w-32"
          >
            {selected.semesters.map((s) => (
              <option key={s} value={s}>
                Semester {s}
              </option>
            ))}
          </Select>
        </div>
      )}
    </div>
  )
}
