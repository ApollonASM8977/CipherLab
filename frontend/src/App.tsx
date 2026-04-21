// Â© 2026 Aboubacar Sidick Meite (ApollonASM8977) â€” All Rights Reserved
import { useState, useEffect } from 'react'
import axios from 'axios'
import { FlaskConical } from 'lucide-react'
import Sidebar from './components/Sidebar'
import CipherPanel from './components/CipherPanel'
import { CipherDef } from './types'

export default function App() {
  const [ciphers, setCiphers] = useState<CipherDef[]>([])
  const [selectedId, setSelectedId] = useState('caesar')

  useEffect(() => {
    axios.get('/api/ciphers').then(r => {
      setCiphers(r.data.ciphers)
    }).catch(() => {})
  }, [])

  const selected = ciphers.find(c => c.id === selectedId)

  return (
    <div className="relative flex flex-col h-screen bg-lab-bg overflow-hidden">
      <div className="scanline" />

      {/* Top bar */}
      <header className="relative z-10 flex items-center gap-3 px-5 py-3 border-b border-lab-border bg-lab-surface shrink-0">
        <FlaskConical size={20} className="text-lab-green" />
        <h1 className="text-sm font-bold tracking-widest uppercase text-lab-green glow-green">CipherLab</h1>
        <span className="text-lab-muted text-xs">â€”</span>
        <span className="text-lab-muted text-xs">Full Cryptography Toolkit Â· Classical Â· Modern Â· Asymmetric Â· Encoders</span>
        <div className="ml-auto flex items-center gap-3">
          <span className="text-lab-muted/40 text-xs font-mono">Â© ASM</span>
          {ciphers.length === 0 && (
            <span className="text-xs text-lab-amber">âš  Backend offline â€” start uvicorn on port 8000</span>
          )}
          {ciphers.length > 0 && (
            <span className="text-xs text-lab-green">â— {ciphers.length} ciphers loaded</span>
          )}
        </div>
      </header>

      {/* Body */}
      <div className="relative z-10 flex flex-1 overflow-hidden">
        <Sidebar ciphers={ciphers} selected={selectedId} onSelect={setSelectedId} />
        <main className="flex-1 overflow-hidden">
          {selected
            ? <CipherPanel key={selected.id} cipher={selected} />
            : (
              <div className="flex items-center justify-center h-full text-lab-muted text-sm">
                {ciphers.length === 0 ? 'Connecting to backend...' : 'Select a cipher from the sidebar'}
              </div>
            )
          }
        </main>
      </div>
    </div>
  )
}

