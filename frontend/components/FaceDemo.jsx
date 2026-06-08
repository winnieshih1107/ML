'use client';
import { useRef, useEffect, useState, useCallback } from 'react';

export default function FaceDemo() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const rafRef = useRef(null);
  const [status, setStatus] = useState('idle'); // idle | loading | running | error
  const [faceCount, setFaceCount] = useState(0);
  const [faceapi, setFaceapi] = useState(null);

  const stopCamera = useCallback(() => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(t => t.stop());
      videoRef.current.srcObject = null;
    }
    setStatus('idle');
    setFaceCount(0);
  }, []);

  const startDemo = useCallback(async () => {
    setStatus('loading');
    try {
      // dynamic import to avoid SSR issues
      const fa = faceapi || await import('face-api.js').then(m => { setFaceapi(m); return m; });
      await fa.nets.tinyFaceDetector.loadFromUri('/models');

      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
      videoRef.current.srcObject = stream;
      await new Promise(r => (videoRef.current.onloadedmetadata = r));
      videoRef.current.play();

      setStatus('running');

      const detect = async () => {
        if (!videoRef.current || !canvasRef.current) return;
        const detections = await fa.detectAllFaces(
          videoRef.current,
          new fa.TinyFaceDetectorOptions({ inputSize: 224, scoreThreshold: 0.5 })
        );
        const dims = { width: videoRef.current.videoWidth, height: videoRef.current.videoHeight };
        const ctx = canvasRef.current.getContext('2d');
        canvasRef.current.width = dims.width;
        canvasRef.current.height = dims.height;
        ctx.clearRect(0, 0, dims.width, dims.height);

        const resized = fa.resizeResults(detections, dims);
        resized.forEach(d => {
          const { x, y, width, height } = d.box;
          ctx.strokeStyle = '#185FA5';
          ctx.lineWidth = 2;
          ctx.strokeRect(x, y, width, height);
          ctx.fillStyle = '#185FA5';
          ctx.fillRect(x, y - 18, 60, 18);
          ctx.fillStyle = '#fff';
          ctx.font = '11px sans-serif';
          ctx.fillText('Face ✓', x + 4, y - 4);
        });
        setFaceCount(resized.length);
        rafRef.current = requestAnimationFrame(detect);
      };
      detect();
    } catch (e) {
      console.error(e);
      setStatus('error');
    }
  }, [faceapi]);

  useEffect(() => () => stopCamera(), [stopCamera]);

  return (
    <div className="rounded-lg border border-[var(--border)] overflow-hidden bg-white">
      <div className="flex items-center gap-2 px-4 py-2.5 border-b border-[var(--border)] bg-[#E6F1FB]">
        <span className="text-xs font-semibold text-[#0C447C]">🧠 即時人臉偵測 Demo</span>
        <span className="text-[10px] text-[#185FA5]">— 這就是神經網路在做的事</span>
      </div>

      <div className="p-4 space-y-3">
        <p className="text-[11px] text-gray-500 leading-relaxed">
          本 Demo 在瀏覽器端以 <strong>TinyFaceDetector</strong>（輕量神經網路）即時偵測人臉，
          不上傳任何影像至伺服器。
        </p>

        {status === 'idle' && (
          <button
            onClick={startDemo}
            className="text-xs px-3 py-1.5 rounded bg-[#185FA5] text-white hover:bg-[#0C447C] transition-colors"
          >
            開啟鏡頭 Demo
          </button>
        )}

        {status === 'loading' && (
          <p className="text-xs text-gray-400">載入模型中…</p>
        )}

        {status === 'error' && (
          <p className="text-xs text-red-500">無法存取鏡頭，請確認瀏覽器允許攝影機權限。</p>
        )}

        {status === 'running' && (
          <div className="space-y-2">
            <div className="relative inline-block rounded overflow-hidden border border-[var(--border)]">
              <video ref={videoRef} className="block w-full max-w-xs" muted playsInline />
              <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
            </div>
            <div className="flex items-center gap-3">
              <span className="text-[11px] text-gray-600">
                偵測到 <strong className="text-[#185FA5]">{faceCount}</strong> 張人臉
              </span>
              <button
                onClick={stopCamera}
                className="text-[10px] px-2 py-1 rounded border border-[var(--border)] text-gray-500 hover:bg-gray-50"
              >
                關閉
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
