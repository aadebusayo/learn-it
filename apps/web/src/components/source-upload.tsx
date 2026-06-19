"use client";

import { getApiUrl } from "@/lib/api";
import { FileUp, Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useRef, useState } from "react";

export function SourceUpload() {
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function upload(file: File) {
    setIsUploading(true);
    setMessage(null);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${getApiUrl()}/sources`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail ?? "Upload failed");
      }
      const result = await response.json();
      setMessage(`Ingested ${result.concepts_created} concepts from ${result.source.title}.`);
      router.refresh();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Upload failed");
    } finally {
      setIsUploading(false);
      if (inputRef.current) {
        inputRef.current.value = "";
      }
    }
  }

  return (
    <div className="flex flex-col items-start gap-2">
      <input
        ref={inputRef}
        className="hidden"
        type="file"
        accept=".md,.markdown,.txt,.pdf,text/markdown,text/plain,application/pdf"
        onChange={(event) => {
          const file = event.target.files?.[0];
          if (file) {
            void upload(file);
          }
        }}
      />
      <button
        className="inline-flex items-center gap-2 rounded-md bg-ink px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-70"
        type="button"
        disabled={isUploading}
        onClick={() => inputRef.current?.click()}
      >
        {isUploading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <FileUp className="h-4 w-4" aria-hidden="true" />}
        Upload source
      </button>
      {message ? <p className="max-w-72 text-sm leading-5 text-ink/70" role="status">{message}</p> : null}
    </div>
  );
}
