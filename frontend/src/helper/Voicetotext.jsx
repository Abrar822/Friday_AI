import React, {
  useState,
  useRef,
  useCallback,
  useEffect,
} from 'react';

const ACCENT = '#E8A33D';

// Change this if your FastAPI server uses another port.
const API_URL = 'http://127.0.0.1:8000';

export default function VoiceToText() {
  const [listening, setListening] = useState(false);
  const [processing, setProcessing] = useState(false);

  const [finalText, setFinalText] = useState('');
  const [copied, setCopied] = useState(false);

  const [error, setError] = useState('');

  const [levels, setLevels] = useState(
    new Array(24).fill(2)
  );

  // ============================================================
  // REFS
  // ============================================================

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const streamRef = useRef(null);

  const audioCtxRef = useRef(null);
  const analyserRef = useRef(null);

  const rafRef = useRef(null);

  const textEndRef = useRef(null);

  const listeningRef = useRef(false);

  // ============================================================
  // STOP AUDIO LEVEL METER
  // ============================================================

  const stopLevelMeter = useCallback(() => {
    if (rafRef.current) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current
        .getTracks()
        .forEach((track) => track.stop());

      streamRef.current = null;
    }

    if (audioCtxRef.current) {
      audioCtxRef.current
        .close()
        .catch(() => {});

      audioCtxRef.current = null;
    }

    analyserRef.current = null;

    setLevels(new Array(24).fill(2));
  }, []);

  // ============================================================
  // START AUDIO LEVEL METER
  // ============================================================

  const startLevelMeter = useCallback(
    async (stream) => {
      try {
        const AudioContextClass =
          window['AudioContext'] ||
          window['webkitAudioContext'];

        if (!AudioContextClass) {
          return;
        }

        const audioCtx =
          new AudioContextClass();

        audioCtxRef.current = audioCtx;

        const source =
          audioCtx.createMediaStreamSource(stream);

        const analyser =
          audioCtx.createAnalyser();

        analyser.fftSize = 64;

        source.connect(analyser);

        analyserRef.current = analyser;

        const data = new Uint8Array(
          analyser.frequencyBinCount
        );

        const bars = 24;

        const step = Math.max(
          1,
          Math.floor(data.length / bars)
        );

        const updateMeter = () => {
          if (!analyserRef.current) {
            return;
          }

          analyser.getByteFrequencyData(data);

          const nextLevels = new Array(bars)
            .fill(0)
            .map((_, index) => {
              const value =
                data[index * step] || 0;

              return Math.max(
                2,
                Math.round(
                  (value / 255) * 32
                )
              );
            });

          setLevels(nextLevels);

          rafRef.current =
            requestAnimationFrame(
              updateMeter
            );
        };

        updateMeter();

      } catch (err) {
        console.error(
          'Audio meter error:',
          err
        );
      }
    },
    []
  );

  // ============================================================
  // GET MICROPHONE STREAM
  // ============================================================

  const getMicrophone = useCallback(
    async () => {
      try {
        const stream =
          await navigator.mediaDevices.getUserMedia(
            {
              audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,              },
            }
          );

        streamRef.current = stream;

        return stream;

      } catch (err) {
        console.error(
          'Microphone error:',
          err
        );

        setError(
          'Microphone access was denied or unavailable.'
        );

        return null;
      }
    },
    []
  );

  // ============================================================
  // FIND SUPPORTED AUDIO FORMAT
  // ============================================================

  const getMimeType = () => {
    const formats = [
      'audio/webm;codecs=opus',
      'audio/webm',
      'audio/ogg;codecs=opus',
      'audio/mp4',
    ];

    for (const format of formats) {
      if (
        MediaRecorder.isTypeSupported(format)
      ) {
        return format;
      }
    }

    return '';
  };

  // ============================================================
  // SEND AUDIO TO FASTAPI
  // ============================================================

  const sendAudioToBackend = async (
    audioBlob
  ) => {
    try {
      setProcessing(true);
      setError('');

      const formData = new FormData();

      const extension =
        audioBlob.type.includes('ogg')
          ? 'ogg'
          : audioBlob.type.includes('mp4')
          ? 'mp4'
          : 'webm';

      formData.append(
        'file',
        audioBlob,
        `recording.${extension}`
      );

      const response = await fetch(
        `${API_URL}/transcribe`,
        {
          method: 'POST',
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(
          `Server returned ${response.status}`
        );
      }

      const data =
        await response.json();

      console.log(
        'Transcription response:',
        data
      );

      /*
        Expected FastAPI response:

        {
          "text": "hello world"
        }
      */

      if (data.text) {
        setFinalText(
          (previous) => {
            if (!previous.trim()) {
              return data.text.trim() + ' ';
            }

            return (
              previous.trim() +
              ' ' +
              data.text.trim() +
              ' '
            );
          }
        );
      }

    } catch (err) {
      console.error(
        'Transcription error:',
        err
      );

      setError(
        'Could not connect to the transcription server.'
      );

    } finally {
      setProcessing(false);
    }
  };

  // ============================================================
  // START RECORDING
  // ============================================================

  const start = useCallback(
    async () => {
      if (
        listeningRef.current ||
        processing
      ) {
        return;
      }

      setError('');

      const stream =
        await getMicrophone();

      if (!stream) {
        return;
      }

      audioChunksRef.current = [];

      const mimeType =
        getMimeType();

      let recorder;

      try {
        recorder = mimeType
          ? new MediaRecorder(
              stream,
              {
                mimeType,
              }
            )
          : new MediaRecorder(stream);

      } catch (err) {
        console.error(
          'MediaRecorder error:',
          err
        );

        setError(
          'Audio recording is not supported.'
        );

        stopLevelMeter();

        return;
      }

      mediaRecorderRef.current =
        recorder;

      // ========================================================
      // AUDIO DATA
      // ========================================================

      recorder.ondataavailable = (
        event
      ) => {
        if (
          event.data &&
          event.data.size > 0
        ) {
          audioChunksRef.current.push(
            event.data
          );
        }
      };

      // ========================================================
      // RECORDING STOPPED
      // ========================================================

      recorder.onstop = async () => {
        const audioBlob =
          new Blob(
            audioChunksRef.current,
            {
              type:
                recorder.mimeType ||
                'audio/webm',
            }
          );

        audioChunksRef.current = [];

        stopLevelMeter();

        if (audioBlob.size === 0) {
          setError(
            'No audio was recorded.'
          );

          return;
        }

        await sendAudioToBackend(
          audioBlob
        );
      };

      // ========================================================
      // START
      // ========================================================

      recorder.start(250);

      listeningRef.current = true;

      setListening(true);

      await startLevelMeter(stream);
    },
    [
      getMicrophone,
      processing,
      sendAudioToBackend,
      startLevelMeter,
      stopLevelMeter,
    ]
  );

  // ============================================================
  // STOP RECORDING
  // ============================================================

  const stop = useCallback(() => {
    if (!listeningRef.current) {
      return;
    }

    listeningRef.current = false;

    setListening(false);

    const recorder =
      mediaRecorderRef.current;

    if (
      recorder &&
      recorder.state !== 'inactive'
    ) {
      recorder.stop();
    } else {
      stopLevelMeter();
    }
  }, [stopLevelMeter]);

  // ============================================================
  // TOGGLE
  // ============================================================

  const toggle = useCallback(() => {
    if (listeningRef.current) {
      stop();
    } else {
      start();
    }
  }, [start, stop]);

  // ============================================================
  // SHIFT + .
  // ============================================================

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (
        event.shiftKey &&
        (
          event.code === 'Period' ||
          event.key === '.'
        )
      ) {
        event.preventDefault();

        toggle();
      }
    };

    window.addEventListener(
      'keydown',
      handleKeyDown
    );

    return () => {
      window.removeEventListener(
        'keydown',
        handleKeyDown
      );
    };
  }, [toggle]);

  // ============================================================
  // AUTO SCROLL
  // ============================================================

  useEffect(() => {
    textEndRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'end',
    });
  }, [finalText]);

  // ============================================================
  // CLEANUP
  // ============================================================

  useEffect(() => {
    return () => {
      listeningRef.current = false;

      const recorder =
        mediaRecorderRef.current;

      if (
        recorder &&
        recorder.state !== 'inactive'
      ) {
        try {
          recorder.stop();
        } catch (err) {}
      }

      stopLevelMeter();
    };
  }, [stopLevelMeter]);

  // ============================================================
  // COPY
  // ============================================================

  const handleCopy = async () => {
    if (!finalText.trim()) {
      return;
    }

    try {
      await navigator.clipboard.writeText(
        finalText.trim()
      );

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 1500);

    } catch (err) {
      console.error(
        'Copy error:',
        err
      );
    }
  };

  // ============================================================
  // CLEAR
  // ============================================================

  const handleClear = () => {
    setFinalText('');
    setError('');
  };

  // ============================================================
  // WORD COUNT
  // ============================================================

  const wordCount =
    finalText.trim()
      ? finalText
          .trim()
          .split(/\s+/)
          .length
      : 0;

  // ============================================================
  // UI
  // ============================================================

  return (
    <div
      style={{
        background: '#16171A',
        color: '#E8E6E1',
        fontFamily:
          'ui-sans-serif, -apple-system, sans-serif',
        borderRadius: 14,
        maxWidth: 640,
        margin: '0 auto',
        overflow: 'hidden',
        border:
          '1px solid #262830',
      }}
    >

      {/* ======================================================
          HEADER
      ======================================================= */}

      <div
        style={{
          padding: '20px 24px',
          borderBottom:
            '1px solid #262830',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 16,
        }}
      >

        {/* MIC */}

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
          }}
        >

          <button
            onClick={toggle}
            disabled={processing}
            aria-label={
              listening
                ? 'Stop listening'
                : 'Start listening'
            }
            style={{
              width: 44,
              height: 44,
              borderRadius: '50%',
              border: 'none',
              cursor:
                processing
                  ? 'not-allowed'
                  : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background:
                listening
                  ? ACCENT
                  : '#232529',
              color:
                listening
                  ? '#16171A'
                  : '#8B8D91',
              opacity:
                processing ? 0.5 : 1,
              transition:
                'background 120ms ease',
              flexShrink: 0,
            }}
          >

            <i
              className={
                processing
                  ? 'fa-solid fa-spinner fa-spin'
                  : listening
                  ? 'fa-solid fa-stop'
                  : 'fa-solid fa-microphone'
              }
              style={{
                fontSize: 17,
              }}
            />

          </button>

          <div>

            <div
              style={{
                fontSize: 14,
                fontWeight: 500,
              }}
            >
              {processing
                ? 'Transcribing'
                : listening
                ? 'Listening'
                : 'Idle'}
            </div>

            <div
              style={{
                fontFamily:
                  'ui-monospace, monospace',
                fontSize: 11,
                color: '#6B6E75',
                letterSpacing: 0.2,
              }}
            >
              shift + . to toggle
            </div>

          </div>

        </div>

        {/* ==================================================
            LEVEL METER
        =================================================== */}

        <div
          style={{
            display: 'flex',
            alignItems: 'flex-end',
            gap: 2,
            height: 32,
          }}
        >

          {levels.map(
            (height, index) => (
              <div
                key={index}
                style={{
                  width: 3,
                  height,
                  borderRadius: 1,
                  background:
                    listening
                      ? ACCENT
                      : '#2A2C32',
                  transition:
                    'height 60ms ease',
                }}
              />
            )
          )}

        </div>

      </div>

      {/* ======================================================
          TRANSCRIPT
      ======================================================= */}

      <div
        style={{
          padding: 24,
          minHeight: 260,
          maxHeight: 400,
          overflowY: 'auto',
        }}
      >

        {finalText ? (

          <p
            style={{
              fontSize: 16,
              lineHeight: 1.7,
              whiteSpace: 'pre-wrap',
              margin: 0,
            }}
          >
            {finalText}
          </p>

        ) : (

          <p
            style={{
              fontSize: 14,
              color: '#5B5D63',
              margin: 0,
            }}
          >
            Press{' '}

            <span
              style={{
                fontFamily:
                  'ui-monospace, monospace',
                background:
                  '#232529',
                padding:
                  '2px 6px',
                borderRadius: 4,
              }}
            >
              Shift + .
            </span>

            {' '}or the mic button
            to start dictating.
          </p>

        )}

        {/* ==================================================
            PROCESSING
        =================================================== */}

        {processing && (
          <div
            style={{
              marginTop: 16,
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              color: '#6B6E75',
              fontSize: 13,
            }}
          >

            <i
              className="fa-solid fa-spinner fa-spin"
            />

            Transcribing audio...

          </div>
        )}

        {/* ==================================================
            ERROR
        =================================================== */}

        {error && (
          <div
            style={{
              marginTop: 16,
              padding: 10,
              borderRadius: 6,
              background: '#241C16',
              border:
                '1px solid #4A3320',
              color: ACCENT,
              fontSize: 12,
            }}
          >
            <i
              className="fa-solid fa-triangle-exclamation"
              style={{
                marginRight: 7,
              }}
            />

            {error}
          </div>
        )}

        <div ref={textEndRef} />

      </div>

      {/* ======================================================
          FOOTER
      ======================================================= */}

      <div
        style={{
          padding:
            '14px 24px',
          borderTop:
            '1px solid #262830',
          display: 'flex',
          alignItems: 'center',
          justifyContent:
            'space-between',
        }}
      >

        {/* WORD COUNT */}

        <span
          style={{
            fontFamily:
              'ui-monospace, monospace',
            fontSize: 12,
            color: '#6B6E75',
          }}
        >
          {wordCount}{' '}
          {wordCount === 1
            ? 'word'
            : 'words'}
        </span>

        {/* BUTTONS */}

        <div
          style={{
            display: 'flex',
            gap: 8,
          }}
        >

          {/* CLEAR */}

          <button
            onClick={handleClear}
            style={btnStyle}
          >

            <i
              className="fa-solid fa-trash"
              style={{
                fontSize: 12,
              }}
            />

            Clear

          </button>

          {/* COPY */}

          <button
            onClick={handleCopy}
            disabled={!finalText.trim()}
            style={{
              ...btnStyle,
              opacity:
                finalText.trim()
                  ? 1
                  : 0.4,
              color:
                copied
                  ? ACCENT
                  : '#8B8D91',
            }}
          >

            <i
              className={
                copied
                  ? 'fa-solid fa-check'
                  : 'fa-regular fa-copy'
              }
              style={{
                fontSize: 12,
              }}
            />

            {copied
              ? 'Copied'
              : 'Copy'}

          </button>

        </div>

      </div>

    </div>
  );
}

// ============================================================
// BUTTON STYLE
// ============================================================

const btnStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 6,
  fontSize: 12,
  color: '#8B8D91',
  background: '#1D1F23',
  border:
    '1px solid #262830',
  borderRadius: 6,
  padding: '6px 10px',
  cursor: 'pointer',
};