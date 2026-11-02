import { useEffect, useState } from 'react'
import { importCourseCurriculumClos } from '../../api/curriculum'
import { ApiError } from '../../api/client'
import Modal, { ModalFooter } from '../../components/ui/Modal'
import Button from '../../components/ui/Button'
import Badge from '../../components/ui/Badge'

// Pick which of the curriculum document's CLOs to add to this course. Adding
// them never maps them to PLOs -- the faculty does that afterwards with
// "Map to PLOs", same as for manually written CLOs.
export default function CurriculumClosModal({ isOpen, onClose, course, curriculum, onImported }) {
  const [selected, setSelected] = useState(new Set())
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const clos = curriculum?.clos ?? []

  useEffect(() => {
    if (isOpen) {
      setSelected(new Set(clos.filter((c) => !c.already_added).map((c) => c.index)))
      setError('')
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen])

  function toggle(index) {
    setSelected((current) => {
      const next = new Set(current)
      if (next.has(index)) next.delete(index)
      else next.add(index)
      return next
    })
  }

  async function handleAdd() {
    setError('')
    setIsSubmitting(true)
    try {
      await importCourseCurriculumClos(course.id, [...selected])
      onClose()
      onImported()
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : 'Something went wrong.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Add CLOs from curriculum"
      description={`The outcomes the curriculum document lists for ${course.code}. You can edit them after adding.`}
      width="max-w-2xl"
    >
      <div className="flex flex-col gap-3">
        <div className="border border-border rounded-lg divide-y divide-border max-h-96 overflow-y-auto">
          {clos.map((clo) => (
            <label
              key={clo.index}
              className={`flex items-start gap-3 px-3 py-2.5 text-sm ${
                clo.already_added ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer hover:bg-slate-50'
              }`}
            >
              <input
                type="checkbox"
                className="mt-0.5 h-4 w-4 rounded border-border-strong text-brand-600 focus:ring-brand-500"
                checked={clo.already_added || selected.has(clo.index)}
                disabled={clo.already_added}
                onChange={() => toggle(clo.index)}
              />
              <span className="flex-1 min-w-0">
                <span className="flex flex-wrap items-center gap-2">
                  <span className="font-medium text-ink-900">{clo.title}</span>
                  <Badge tone="neutral">{clo.bloom_level}</Badge>
                  {clo.already_added && <Badge tone="success">Added</Badge>}
                </span>
                <span className="block text-xs text-ink-500 mt-0.5">{clo.description}</span>
              </span>
            </label>
          ))}
        </div>
        <p className="text-xs text-ink-500">
          CLOs are not mapped to PLOs automatically. Use &quot;Map to PLOs&quot; on each one afterwards.
        </p>
        {error && <p className="text-sm text-danger-600 bg-danger-50 rounded-lg px-3 py-2">{error}</p>}
      </div>
      <ModalFooter>
        <Button variant="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button onClick={handleAdd} isLoading={isSubmitting} disabled={selected.size === 0}>
          Add {selected.size > 0 ? `${selected.size} CLO${selected.size === 1 ? '' : 's'}` : 'CLOs'}
        </Button>
      </ModalFooter>
    </Modal>
  )
}
