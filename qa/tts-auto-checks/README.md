# TTS Auto Checks

This folder stores public-safe QA summaries for TTS experiments.

Keep generated audio, reference audio, failed samples, raw ASR caches, and private packages in local/private storage such as:

```text
assets/tts-local-only/
.local/
~/Downloads/<project-specific-package>/
```

Public QA summaries may include:

- experiment ID
- source and output SHA-256
- ASR model
- CER / WER
- critical term accuracy
- `term_error_list.csv`
- audio quality status
- chunk consistency status
- final decision label
