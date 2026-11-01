import { apiFetch } from './client'

/**
 * Send one message to the AdaptOBE assistant.
 * @param {string} message
 * @param {{role: 'user'|'assistant', content: string}[]} history - prior turns, oldest first
 */
export function sendChatMessage(message, history) {
  return apiFetch('/api/v1/chat', { method: 'POST', body: { message, history } })
}
