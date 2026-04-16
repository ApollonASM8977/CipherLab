import { useState, useEffect } from 'react'
import axios from 'axios'
import { Lock, Unlock, Copy, Check, RefreshCw, ChevronDown, ChevronUp, AlertCircle, Loader2, ArrowLeftRight, Key } from 'lucide-react'
import { CipherDef, ProcessResult } from '../types'
import StepsView from './StepsView'

interface Props { cipher: CipherDef }

export default function CipherPanel({ cipher }: Props) {
  const [mode, setMode] = useState(cipher.modes[0])
  const [input, setInput] = useState('')
  const [params, setParams] = useState<Record<string, string>>({})
  const [result, setResult] = useState<ProcessResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [genLoading, setGenLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)
  const [showSteps, setShowSteps] = useState(false)

  // Reset on cipher change
  useEffect(() => {
    setMode(cipher.modes[0])
    setInput('')
    setParams({})
    setResult(null)
    setError('')
    setShowSteps(false)
  }, [cipher.id])

  const setParam = (k: string, v: string) => setParams(p => ({ ...p, [k]: v }))

  const handleProcess = async () => {
    if (!input.trim()) return
    setLoading(true); setError(''); setResult(null)
    try {
      const { data } = await axios.post<ProcessResult>('/api/process', { cipher: cipher.id, mode, text: input, params })
      setResult(data)
    } catch (e: unknown) {
      if (axios.isAxiosError(e)) {
        setError(e.response?.data?.detail ?? (!e.response ? 'Cannot reach server — start the backend on port 8000.' : `Server error ${e.response.status}`))
      } else setError('Unexpected error.')
    } finally { setLoading(false) }
  }

  const generateKey = async () => {
    setGenLoading(true)
    try {
      const { data } = await axios.post('/api/generate-key', { cipher: cipher.id })
      if (data.key) setParam('key', data.key)
      if (data.private_key) { setParam('private_key', data.private_key); setParam('public_key', data.public_key) }
    } catch { /* ignore */ }
    finally { setGenLoading(false) }
  }

  const copy = () => {
    if (!result) return
    navigator.clipboard.writeText(result.output)
    setCopied(true); setTimeout(() => setCopied(false), 2000)
  }

  const swap = () => {
    if (!result) return
    setInput(result.output)
    setResult(null)
    const opp = mode === 'encrypt' ? 'decrypt' : mode === 'encode' ? 'decode' : mode === 'decrypt' ? 'encrypt' : 'encode'
    if (cipher.modes.includes(opp)) setMode(opp)
  }

  const isEncoder = cipher.category === 'encoder'
  const canGenKey = cipher.params.some(p => p.generate) || cipher.generateKeypair
  const visibleParams = cipher.params.filter(p => !p.forMode || p.forMode === mode)
  const modeColor = (m: string) => {
    if (m === 'encrypt' || m === 'encode') return 'border-lab-green text-lab-green bg-lab-green/5'
    return 'border-lab-amber text-lab-amber bg-lab-amber/5'
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-6 py-4 border-b border-lab-border flex items-center justify-between">
        <div>
          <h2 className="text-sm font-bold text-lab-text uppercase tracking-wider">{cipher.name}</h2>
          <p className="text-xs text-lab-muted capitalize">{cipher.category} cipher</p>
        </div>
        {/* Mode tabs */}
        <div className="flex rounded overflow-hidden border border-lab-border">
          {cipher.modes.map(m => (
            <button key={m} onClick={() => { setMode(m); setResult(null) }}
              className={`px-4 py-1.5 text-xs font-mono uppercase tracking-wider transition-all border-b-2 -mb-px
                ${mode === m ? modeColor(m) : 'text-lab-muted hover:text-lab-text border-transparent'}`}
            >
              {m === 'encrypt' ? <><Lock size={11} className="inline mr-1" />Encrypt</> :
               m === 'decrypt' ? <><Unlock size={11} className="inline mr-1" />Decrypt</> :
               m === 'encode'  ? <>Encode</> : <>Decode</>}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        {/* Params */}
        {visibleParams.length > 0 && (
          <div className="space-y-3">
            {visibleParams.map(param => (
              <div key={param.key}>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-xs text-lab-muted uppercase tracking-widest">{param.label}</label>
                  {param.warning && <span className="text-xs text-lab-amber">⚠ {param.warning}</span>}
                </div>
                {param.type === 'textarea' ? (
                  <textarea rows={4} className="lab-input w-full px-3 py-2 rounded text-xs resize-y"
                    placeholder={param.label} value={params[param.key] ?? ''}
                    onChange={e => setParam(param.key, e.target.value)} />
                ) : param.type === 'number' ? (
                  <input type="number" min={param.min} max={param.max}
                    className="lab-input w-24 px-3 py-2 rounded text-sm text-center"
                    value={params[param.key] ?? String(param.default ?? '')}
                    onChange={e => setParam(param.key, e.target.value)} />
                ) : (
                  <div className="flex gap-2">
                    <input className="lab-input flex-1 px-3 py-2 rounded text-xs"
                      placeholder={param.label}
                      value={params[param.key] ?? String(param.default ?? '')}
                      onChange={e => setParam(param.key, e.target.value)} />
                  </div>
                )}
              </div>
            ))}
            {canGenKey && (
              <button onClick={generateKey} disabled={genLoading}
                className="flex items-center gap-2 px-3 py-1.5 rounded border border-lab-blue/40 text-lab-blue text-xs hover:bg-lab-blue/10 transition-colors disabled:opacity-50">
                {genLoading ? <Loader2 size={12} className="animate-spin" /> : <Key size={12} />}
                Generate {cipher.generateKeypair ? 'Key Pair' : 'Key'}
              </button>
            )}
          </div>
        )}

        {/* Input */}
        <div className="space-y-1.5">
          <label className="text-xs text-lab-muted uppercase tracking-widest">
            {isEncoder ? 'Input' : mode === 'encrypt' ? 'Plaintext' : 'Ciphertext'}
          </label>
          <textarea rows={5} className="lab-input w-full px-4 py-3 rounded-lg text-sm resize-y"
            placeholder="Enter text..."
            value={input}
            onChange={e => { setInput(e.target.value); setResult(null); setError('') }} />
        </div>

        {/* Process button */}
        <div className="flex gap-2">
          <button onClick={handleProcess} disabled={!input.trim() || loading}
            className={`flex-1 py-2.5 rounded font-mono text-sm font-bold uppercase tracking-widest transition-all
              disabled:opacity-30 disabled:cursor-not-allowed
              ${mode === 'encrypt' || mode === 'encode'
                ? 'bg-lab-green text-lab-bg hover:shadow-[0_0_16px_#00ff4140]'
                : 'bg-lab-amber text-lab-bg hover:shadow-[0_0_16px_#ffb30040]'}`}
          >
            {loading ? <span className="flex items-center justify-center gap-2"><Loader2 size={14} className="animate-spin" />Processing...</span>
              : mode === 'encrypt' ? '🔒 Encrypt' : mode === 'decrypt' ? '🔓 Decrypt'
              : mode === 'encode'  ? '⬆ Encode'  : '⬇ Decode'}
          </button>
          {result && (
            <button onClick={swap} title="Swap input/output" className="px-3 py-2.5 rounded border border-lab-border text-lab-muted hover:text-lab-text hover:border-lab-green/40 transition-colors">
              <ArrowLeftRight size={14} />
            </button>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="flex items-start gap-2 px-4 py-3 rounded bg-red-950/30 border border-red-800/40">
            <AlertCircle size={14} className="text-red-400 mt-0.5 shrink-0" />
            <p className="text-xs text-red-400 font-mono">{error}</p>
          </div>
        )}

        {/* Output */}
        {result && (
          <div className="space-y-4">
            <div className="rounded-lg border border-lab-border bg-lab-card p-4 space-y-3">
              <div className="flex items-center justify-between">
                <p className="text-xs text-lab-muted uppercase tracking-widest">
                  {isEncoder ? 'Output' : mode === 'encrypt' ? 'Ciphertext' : 'Plaintext'}
                </p>
                <div className="flex gap-2">
                  <button onClick={copy} className="flex items-center gap-1 px-2 py-1 rounded text-xs border border-lab-border text-lab-muted hover:text-lab-green hover:border-lab-green/40 transition-colors">
                    {copied ? <Check size={11} className="text-lab-green" /> : <Copy size={11} />}
                    {copied ? 'Copied!' : 'Copy'}
                  </button>
                </div>
              </div>
              <p className={`font-mono text-sm break-all leading-relaxed
                ${mode === 'encrypt' || mode === 'encode' ? 'text-lab-green' : 'text-lab-amber'}`}>
                {result.output}
              </p>
            </div>

            {/* Steps toggle */}
            {result.steps?.length > 0 && (
              <div>
                <button onClick={() => setShowSteps(s => !s)}
                  className="flex items-center gap-2 text-xs text-lab-muted hover:text-lab-text transition-colors w-full mb-2">
                  {showSteps ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                  <span className="uppercase tracking-widest">Step-by-step trace</span>
                  <span className="text-lab-muted/50">({result.steps.length} steps)</span>
                </button>
                {showSteps && <StepsView steps={result.steps} cipher={cipher.id} />}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
