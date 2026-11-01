import { useEffect, useRef, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { sendChatMessage } from '../../api/chat'
import { ApiError } from '../../api/client'
import ChatText from './ChatText'

// Mirror the backend limits (app/services/chat_guard.py) so the user gets
// immediate feedback instead of a 422.
const MAX_MESSAGE_CHARS = 1000
const MAX_HISTORY_TURNS = 10
const MAX_HISTORY_TURN_CHARS = 4000

const SUGGESTIONS = {
  student: [
    'Which CLOs am I weak in?',
    'How does the practice quiz work?',
    'How is my CLO attainment calculated?',
  ],
  faculty: [
    'Which students are at risk in my courses?',
    'How much assessment weightage is left in my courses?',
    'How do I upload an assessment paper?',
  ],
  sub_admin: [
    'How do I add students from a file?',
    "How do I view a student's password?",
    'How do I add a faculty account?',
  ],
  super_admin: ['How do I add a Sub-Admin?', 'What can a Super Admin manage?'],
}

const TOOL_LABEL = {
  get_my_progress: 'your progress',
  get_my_scores: 'your scores',
  list_my_courses: 'your courses',
  get_course_attainment: 'course attainment',
  list_course_assessments: 'course assessments',
  get_course_risk: 'risk predictions',
}

// "Ms. Madiha Khurram" -> "Madiha", "Dr. Sarah Chen" -> "Sarah".
function firstName(fullName) {
  const parts = fullName.split(/\s+/).filter(Boolean)
  const name = parts.find((p) => !/^(mr|mrs|ms|miss|dr|prof|engr|sir)\.?$/i.test(p))
  return name ?? parts[0] ?? ''
}

function errorText(err) {
  if (err instanceof ApiError) {
    if (err.status === 429) return err.detail
    if (err.status === 502) return 'The assistant is unavailable right now. Please try again in a moment.'
    if (err.status === 422) return 'That message could not be sent. Try a shorter question.'
  }
  return 'Something went wrong. Please try again.'
}

function ChatIcon({ className }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M8 10h8M8 14h5m-7 6 3.5-3H18a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H6a3 3 0 0 0-3 3v7a3 3 0 0 0 3 3v3Z"
      />
    </svg>
  )
}

export default function ChatWidget() {
  const { user } = useAuth()
  const location = useLocation()
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const scrollRef = useRef(null)
  const inputRef = useRef(null)

  // A conversation belongs to one signed-in user; never carry it across accounts.
  useEffect(() => {
    setMessages([])
    setIsOpen(false)
  }, [user?.id])

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, isSending])

  useEffect(() => {
    if (isOpen) inputRef.current?.focus()
  }, [isOpen])

  if (!user || location.pathname === '/login') return null

  async function send(text) {
    const message = text.trim()
    if (!message || isSending || message.length > MAX_MESSAGE_CHARS) return

    const history = messages
      .filter((m) => !m.isError)
      .slice(-MAX_HISTORY_TURNS)
      .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_HISTORY_TURN_CHARS) }))

    setMessages((current) => [...current, { role: 'user', content: message }])
    setInput('')
    setIsSending(true)
    try {
      const response = await sendChatMessage(message, history)
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: response.reply,
          sources: response.sources,
          toolsUsed: response.tools_used,
          degraded: response.degraded,
        },
      ])
    } catch (err) {
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: errorText(err), isError: true },
      ])
    } finally {
      setIsSending(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send(input)
    }
  }

  const suggestions = SUGGESTIONS[user.role] ?? []
  const overLimit = input.length > MAX_MESSAGE_CHARS

  return (
    <>
      {!isOpen && (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          aria-label="Open AdaptOBE Assistant"
          className="fixed bottom-4 right-4 z-40 inline-flex h-12 w-12 items-center justify-center rounded-full
            bg-brand-600 text-white shadow-[var(--shadow-elevation-3)] hover:bg-brand-700 transition-colors"
        >
          <ChatIcon className="h-6 w-6" />
        </button>
      )}

      {isOpen && (
        <section
          role="dialog"
          aria-label="AdaptOBE Assistant"
          className="fixed z-40 inset-x-0 bottom-0 top-14 flex flex-col bg-surface-raised border-t border-border
            shadow-[var(--shadow-elevation-3)]
            sm:inset-x-auto sm:top-auto sm:bottom-4 sm:right-4 sm:h-[min(560px,calc(100vh-6rem))] sm:w-[380px]
            sm:rounded-xl sm:border"
        >
          <header className="flex items-start justify-between gap-3 px-4 py-3 border-b border-border shrink-0">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="h-8 w-8 shrink-0 rounded-lg bg-brand-600 text-white flex items-center justify-center">
                <ChatIcon className="h-4.5 w-4.5" />
              </div>
              <div className="min-w-0">
                <h2 className="text-sm font-semibold text-ink-900">AdaptOBE Assistant</h2>
                <p className="text-xs text-ink-500 truncate">Read-only · can't change your data</p>
              </div>
            </div>
            <div className="flex items-center gap-1 shrink-0">
              {messages.length > 0 && (
                <button
                  type="button"
                  onClick={() => setMessages([])}
                  className="text-xs font-medium text-ink-500 hover:text-ink-900 rounded-md px-2 py-1 hover:bg-slate-100"
                >
                  New chat
                </button>
              )}
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                aria-label="Close assistant"
                className="text-ink-400 hover:text-ink-700 rounded-md p-1.5 hover:bg-slate-100"
              >
                <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                </svg>
              </button>
            </div>
          </header>

          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-3">
            {messages.length === 0 && (
              <div className="flex flex-col gap-3">
                <p className="text-sm text-ink-700">
                  Hi {firstName(user.full_name)}! Ask me how to use AdaptOBE
                  {user.role === 'student' || user.role === 'faculty'
                    ? ', or about your own course data.'
                    : '.'}
                </p>
                <div className="flex flex-col gap-2">
                  {suggestions.map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => send(s)}
                      className="text-left text-sm text-brand-700 bg-brand-50 hover:bg-brand-100 rounded-lg px-3 py-2
                        transition-colors"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((m, i) =>
              m.role === 'user' ? (
                <div key={i} className="self-end max-w-[85%] rounded-2xl rounded-br-md bg-brand-600 text-white px-3.5 py-2 text-sm whitespace-pre-wrap break-words">
                  {m.content}
                </div>
              ) : (
                <div key={i} className="self-start max-w-[92%] flex flex-col gap-1">
                  <div
                    className={`rounded-2xl rounded-bl-md px-3.5 py-2.5 text-sm break-words ${
                      m.isError ? 'bg-danger-50 text-danger-700' : 'bg-slate-100 text-ink-900'
                    }`}
                  >
                    {m.isError ? m.content : <ChatText text={m.content} />}
                  </div>
                  {m.degraded && (
                    <p className="text-[11px] text-warning-700 px-1">AI offline: showing help articles</p>
                  )}
                  {m.toolsUsed?.length > 0 && (
                    <p className="text-[11px] text-ink-400 px-1">
                      Looked up: {m.toolsUsed.map((t) => TOOL_LABEL[t] ?? t).join(', ')}
                    </p>
                  )}
                  {m.sources?.length > 0 && !m.toolsUsed?.length && (
                    <p className="text-[11px] text-ink-400 px-1">Help: {m.sources.join(' · ')}</p>
                  )}
                </div>
              ),
            )}

            {isSending && (
              <div className="self-start rounded-2xl rounded-bl-md bg-slate-100 px-3.5 py-3 flex gap-1" aria-label="Assistant is typing">
                {[0, 150, 300].map((delay) => (
                  <span
                    key={delay}
                    className="h-1.5 w-1.5 rounded-full bg-ink-400 animate-bounce"
                    style={{ animationDelay: `${delay}ms` }}
                  />
                ))}
              </div>
            )}
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault()
              send(input)
            }}
            className="border-t border-border p-3 flex items-end gap-2 shrink-0"
          >
            <div className="flex-1 flex flex-col gap-1">
              <textarea
                ref={inputRef}
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a question…"
                aria-label="Message"
                className={`max-h-28 min-h-9 resize-none rounded-lg border px-3 py-2 text-sm text-ink-900
                  placeholder:text-ink-400 focus:border-brand-500 ${overLimit ? 'border-danger-500' : 'border-border-strong'}`}
              />
              {input.length > MAX_MESSAGE_CHARS * 0.8 && (
                <span className={`text-[11px] ${overLimit ? 'text-danger-600' : 'text-ink-400'}`}>
                  {input.length}/{MAX_MESSAGE_CHARS}
                </span>
              )}
            </div>
            <button
              type="submit"
              disabled={!input.trim() || isSending || overLimit}
              aria-label="Send message"
              className="h-9 w-9 shrink-0 inline-flex items-center justify-center rounded-lg bg-brand-600 text-white
                hover:bg-brand-700 disabled:opacity-50 disabled:pointer-events-none transition-colors"
            >
              <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path d="M3.105 2.288a.75.75 0 0 0-.826.95l1.414 4.926A1.5 1.5 0 0 0 5.135 9.25h6.115a.75.75 0 0 1 0 1.5H5.135a1.5 1.5 0 0 0-1.442 1.086l-1.414 4.926a.75.75 0 0 0 .826.95 28.897 28.897 0 0 0 15.293-7.155.75.75 0 0 0 0-1.114A28.897 28.897 0 0 0 3.105 2.288Z" />
              </svg>
            </button>
          </form>
        </section>
      )}
    </>
  )
}
