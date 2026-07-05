import { useCallback, useRef, useState } from 'react'

// Wraps Web Speech API TTS. Exposes isSpeaking + mouthLevel (0-1) so the
// avatar can drive lip animation without real audio analysis — pulses on
// each word boundary and decays between them.
export function useSpeech() {
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [mouthLevel, setMouthLevel] = useState(0)
  const decayTimer = useRef<number | null>(null)

  const speak = useCallback((text: string) => {
    if (!('speechSynthesis' in window)) return

    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.rate = 1
    utterance.pitch = 0.85
    utterance.volume = 1

    const voices = window.speechSynthesis.getVoices()
    const preferred = voices.find((v) => /male|david|daniel|google uk english male/i.test(v.name))
    if (preferred) utterance.voice = preferred

    utterance.onstart = () => setIsSpeaking(true)
    utterance.onend = () => {
      setIsSpeaking(false)
      setMouthLevel(0)
    }
    utterance.onerror = () => {
      setIsSpeaking(false)
      setMouthLevel(0)
    }
    utterance.onboundary = () => {
      setMouthLevel(0.4 + Math.random() * 0.6)
      if (decayTimer.current) window.clearTimeout(decayTimer.current)
      decayTimer.current = window.setTimeout(() => setMouthLevel(0.1), 90)
    }

    window.speechSynthesis.speak(utterance)
  }, [])

  return { speak, isSpeaking, mouthLevel }
}
