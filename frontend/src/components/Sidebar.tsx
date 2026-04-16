import { CipherDef } from '../types'

const CATEGORIES = [
  { id: 'classical',  label: '⚙️  Classical',   color: 'text-lab-amber' },
  { id: 'modern',     label: '🔒  Modern',       color: 'text-lab-green' },
  { id: 'asymmetric', label: '🔑  Asymmetric',   color: 'text-lab-blue' },
  { id: 'encoder',    label: '🔡  Encoders',     color: 'text-lab-purple' },
]

interface Props {
  ciphers: CipherDef[]
  selected: string
  onSelect: (id: string) => void
}

export default function Sidebar({ ciphers, selected, onSelect }: Props) {
  return (
    <aside className="w-52 shrink-0 border-r border-lab-border bg-lab-surface flex flex-col">
      <div className="px-4 py-4 border-b border-lab-border">
        <p className="text-xs text-lab-muted uppercase tracking-widest">Select Cipher</p>
      </div>
      <div className="flex-1 overflow-y-auto py-2">
        {CATEGORIES.map(cat => {
          const items = ciphers.filter(c => c.category === cat.id)
          if (!items.length) return null
          return (
            <div key={cat.id} className="mb-2">
              <p className={`px-4 py-1.5 text-xs uppercase tracking-widest font-bold ${cat.color}`}>
                {cat.label}
              </p>
              {items.map(cipher => (
                <button
                  key={cipher.id}
                  onClick={() => onSelect(cipher.id)}
                  className={`w-full text-left px-4 py-2 text-xs font-mono transition-all
                    ${selected === cipher.id
                      ? 'bg-lab-green/10 text-lab-green border-r-2 border-lab-green'
                      : 'text-lab-muted hover:text-lab-text hover:bg-lab-card'
                    }`}
                >
                  {cipher.name}
                </button>
              ))}
            </div>
          )
        })}
      </div>
    </aside>
  )
}
