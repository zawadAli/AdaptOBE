import { apiFetch } from './client'

export const getCurriculum = (programId) => apiFetch(`/api/v1/curriculum/${programId}`)
