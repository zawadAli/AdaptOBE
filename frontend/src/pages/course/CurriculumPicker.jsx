import { useEffect, useMemo, useState } from 'react'
import { getCurriculum } from '../../api/curriculum'
import Badge from '../../components/ui/Badge'
import Input from '../../components/ui/Input'
import Select from '../../components/ui/Select'
import Spinner from '../../components/ui/Spinner'

const SEMESTERS = [1, 2, 3, 4, 5, 6, 7, 8]

// The existing offering (by anyone in the programme) of `course` in semester `s`.
// Comes from the server, which matches codes the same way its duplicate check
// does, so a taken slot here is exactly one the server would reject.
const takenIn = (course, s) => course.offerings.find((o) => o.semester === s)
const offeringLabel = (o) => (o.is_mine ? 'Already added' : `Taught by ${o.owner_name}`)
const freeSemesters = (course) => course.semesters.filter((s) => !takenIn(course, s))

// Pick a course from the programme's hardcoded curriculum (app/core/curriculum.py).
// `value` / `onChange` carry `{ course, semester }` -- the catalog entry plus the
// semester it will be offered in (electives can sit in more than one semester).
export default function CurriculumPicker({ programId, value, onChange, onUseManual }) {
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

  // In semester view a row is about that one semester; in search view it's
  // available while any of its catalog semesters is still free.
  function rowState(course) {
    if (!query) {
      const offering = takenIn(course, semester)
      return { disabled: !!offering, sem: semester, notes: offering ? [offeringLabel(offering)] : [] }
    }
    const free = freeSemesters(course)
    const notes = course.semesters
      .map((s) => takenIn(course, s))
      .filter(Boolean)
      .map((o) => `Sem ${o.semester}: ${offeringLabel(o)}`)
    return { disabled: free.length === 0, sem: free[0], notes }
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
          const { disabled, sem, notes } = rowState(course)
          const isSelected = selected?.code === course.code
          return (
            <label
              key={course.code}
              className={`flex items-start gap-3 px-3 py-2.5 text-sm ${
                disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:bg-slate-50'
              } ${isSelected ? 'bg-brand-50' : ''}`}
            >
              <input
                type="radio"
                name="catalog-course"
                className="mt-0.5 h-4 w-4 text-brand-600 focus:ring-brand-500"
                checked={isSelected}
                disabled={disabled}
                onChange={() => onChange({ course, semester: sem })}
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
                  {course.clo_count > 0 && (
                    <span className="text-xs text-ink-500">
                      {course.clo_count} CLO{course.clo_count === 1 ? '' : 's'}
                    </span>
                  )}
                  {notes.map((note) => (
                    <span key={note} className="text-xs text-ink-500">
                      {note}
                    </span>
                  ))}
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
            {selected.semesters.map((s) => {
              const offering = takenIn(selected, s)
              return (
                <option key={s} value={s} disabled={!!offering}>
                  Semester {s}
                  {offering ? ` (${offeringLabel(offering)})` : ''}
                </option>
              )
            })}
          </Select>
        </div>
      )}
    </div>
  )
}
