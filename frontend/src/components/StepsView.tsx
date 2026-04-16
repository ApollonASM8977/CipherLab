interface Props {
  steps: Record<string, unknown>[]
  cipher: string
}

export default function StepsView({ steps, cipher }: Props) {
  if (!steps?.length) return null
  const isClassical = ['caesar','rot13','atbash','vigenere','polysubcipher'].includes(cipher)

  if (isClassical && steps[0] && 'input' in steps[0]) {
    const letters = steps.filter(s => s.input !== s.output || (s as {note?:string}).note !== 'pass')
    return (
      <div className="space-y-2">
        <p className="text-xs text-lab-muted uppercase tracking-widest">Step-by-step trace</p>
        <div className="rounded border border-lab-border overflow-hidden text-xs font-mono">
          <div className="grid grid-cols-4 bg-lab-card px-3 py-1.5 text-lab-muted uppercase tracking-widest border-b border-lab-border">
            <span>Pos</span><span>In</span><span>Key/Note</span><span>Out</span>
          </div>
          <div className="max-h-48 overflow-y-auto">
            {steps.map((s, i) => {
              const isPass = (s as {note?:string}).note === 'pass' || (s as {type?:string}).type === 'passthrough'
              return (
                <div key={i} className={`grid grid-cols-4 px-3 py-1 border-b border-lab-border/40 ${isPass ? 'opacity-40' : ''}`}>
                  <span className="text-lab-muted">{(s as {position?:number}).position ?? (i+1)}</span>
                  <span className="text-lab-text">{String((s as {input?:unknown}).input ?? '')}</span>
                  <span className="text-lab-amber text-xs">{
                    (s as {key_char?:string}).key_char
                    ?? (s as {key?:string}).key
                    ?? (s as {note?:string}).note
                    ?? `shift ${(s as {shift?:number}).shift ?? ''}`
                  }</span>
                  <span className="text-lab-green font-bold">{String((s as {output?:unknown}).output ?? '')}</span>
                </div>
              )
            })}
          </div>
        </div>
        <p className="text-xs text-lab-muted">{letters.length} substitutions applied</p>
      </div>
    )
  }

  // Generic steps for modern/encoders
  return (
    <div className="space-y-2">
      <p className="text-xs text-lab-muted uppercase tracking-widest">Operation details</p>
      <div className="space-y-1">
        {steps.slice(0, 30).map((s, i) => (
          <div key={i} className="flex gap-3 text-xs font-mono px-3 py-1.5 rounded bg-lab-card border border-lab-border/50">
            {Object.entries(s).map(([k, v]) => (
              <span key={k}><span className="text-lab-muted">{k}: </span><span className="text-lab-green">{String(v)}</span></span>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
