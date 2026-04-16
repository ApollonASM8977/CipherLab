export interface CipherParam {
  key: string
  type: 'number' | 'text' | 'key' | 'textarea'
  label: string
  default?: string | number
  min?: number
  max?: number
  generate?: boolean
  warning?: string
  forMode?: string
}

export interface CipherDef {
  id: string
  name: string
  category: 'classical' | 'modern' | 'asymmetric' | 'encoder'
  modes: string[]
  params: CipherParam[]
  generateKeypair?: boolean
}

export interface ProcessResult {
  cipher: string
  mode: string
  input: string
  output: string
  steps: Record<string, unknown>[]
}
