import { apiFetch } from './client'

export const getCurriculum = (programId) => apiFetch(`/api/v1/curriculum/${programId}`)

// CLOs the curriculum document lists for one course (flags ones already added).
export const getCourseCurriculumClos = (courseId) =>
  apiFetch(`/api/v1/courses/${courseId}/curriculum-clos`)

// Add curriculum CLOs to the course; omit `indices` to add every one not yet added.
// Never creates CLO->PLO mappings -- those stay a manual step.
export const importCourseCurriculumClos = (courseId, indices) =>
  apiFetch(`/api/v1/courses/${courseId}/curriculum-clos/import`, {
    method: 'POST',
    body: indices ? { indices } : {},
  })
