// Renders the assistant's reply. Supports exactly the small subset the backend
// prompt allows -- **bold**, "-" bullet lists and "1." numbered lists -- by
// building React elements. Model output is never injected as HTML, so a reply
// containing <script> or similar just shows up as harmless text.

function renderInline(text, keyPrefix) {
  return text.split(/(\*\*[^*]+\*\*)/g).map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
      return <strong key={`${keyPrefix}-${i}`}>{part.slice(2, -2)}</strong>
    }
    return part
  })
}

function toBlocks(text) {
  const blocks = []
  for (const rawLine of text.split('\n')) {
    const line = rawLine.trim()
    const bullet = line.match(/^[-*•]\s+(.*)$/)
    const numbered = line.match(/^\d+[.)]\s+(.*)$/)
    const listType = bullet ? 'ul' : numbered ? 'ol' : null
    const last = blocks[blocks.length - 1]

    if (listType) {
      const item = (bullet || numbered)[1]
      if (last && last.type === listType) last.items.push(item)
      else blocks.push({ type: listType, items: [item] })
    } else if (line === '') {
      blocks.push({ type: 'break' })
    } else if (last && last.type === 'p') {
      last.lines.push(line)
    } else {
      blocks.push({ type: 'p', lines: [line] })
    }
  }
  return blocks.filter((b) => b.type !== 'break')
}

export default function ChatText({ text }) {
  return (
    <div className="flex flex-col gap-2">
      {toBlocks(text).map((block, i) => {
        if (block.type === 'p') {
          return <p key={i}>{renderInline(block.lines.join(' '), `p${i}`)}</p>
        }
        const ListTag = block.type
        return (
          <ListTag
            key={i}
            className={`pl-5 flex flex-col gap-0.5 ${ListTag === 'ul' ? 'list-disc' : 'list-decimal'}`}
          >
            {block.items.map((item, j) => (
              <li key={j}>{renderInline(item, `l${i}-${j}`)}</li>
            ))}
          </ListTag>
        )
      })}
    </div>
  )
}
