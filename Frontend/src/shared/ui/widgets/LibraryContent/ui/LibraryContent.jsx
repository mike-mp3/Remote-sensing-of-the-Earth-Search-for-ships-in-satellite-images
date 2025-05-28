import { useEffect, useState, useRef } from "react";
import * as classes from "./LibraryContent.module.scss";
import { ModelCard } from "@/shared/ui/entities/ModelCard";
import { ImageUploader } from "@/shared/ui/entities/ImageUploader";

const LibraryContent = () => {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  const URL = import.meta.env.VITE_API_BASE_URL;
  const WS_URL = import.meta.env.VITE_API_WS_URL;
  const URLLLLLL = URL + "/s3";

  const handleImageSelect = (newPrompt) => {
  if (!newPrompt) return; // ← Защита от null/undefined
  setSelectedImage(newPrompt);
  setPrompts((prev) => [newPrompt, ...prev]);
};

  const wsRef = useRef(null);

  // Открываем/закрываем WS при изменении списка prompts
  useEffect(() => {
    const hasPending = prompts.some(p => p.status === 'pending');
    console.log('WS effect triggered, hasPending =', hasPending, wsRef.current);
    console.log(WS_URL);

    if (hasPending && !wsRef.current) {
      const ws = new WebSocket(WS_URL);
      ws.onopen = () => console.log('WS opened:', WS_URL);
      ws.onmessage = async (e) => {
        try {
          const raw = e.data;
          let msg = JSON.parse(raw);
          if (typeof msg === 'string') {
            msg = JSON.parse(msg);
          }

          console.log("STSTSTT, idididi", msg.status, msg.prompt_id);
          
          const body = { prompts: [{ prompt_id: msg.prompt_id, status: msg.status }] };

          const res = await fetch(`${URL}/core/prompt/s3/presigned-get`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
            credentials: 'include',
          });
          if (!res.ok) throw new Error(`Presigned-get failed: ${res.status}`);
          const urls = await res.json();
          const match = urls.find(u => u.prompt_id === msg.prompt_id);
          console.log(match);
          const newUrl = match ? match.url.replace("http://ship-minio:9000", URLLLLLL) : null;
          console.log(newUrl);
          setPrompts(prev => {
          const next = prev.map(p =>
            p.prompt_id === msg.prompt_id
              ? { ...p, status: msg.status, url: newUrl }
              : p
          );
          console.log("New prompts after update:", next);
          return next;
        });
          
          console.log("ahahh", prompts);
        } catch (err) {
          console.error('WS message handling error:', err);
        }
      };
      ws.onerror = e => console.error('WS error:', e);
      ws.onclose = () => console.log('WS closed');
      wsRef.current = ws;
    }

    if (!hasPending && wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [prompts, URL, WS_URL]);

  const fetchPromptsWithUrls = async () => {
    try {
      const response = await fetch(`${URL}/core/prompt?size=50`, {
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true"
        },
        credentials: "include",
      });

      if (!response.ok) {
        if (response.status === 404) {
          console.warn("No prompts found");
          setPrompts([]);
          return;
        }
        if (response.status === 422) {
          throw new Error("Error try again later");
        }
        throw new Error(`Unexpected error: ${response.status}`);
      }

      const promptData = await response.json();
      if (!Array.isArray(promptData)) {
        throw new Error("Expected an array of prompts");
      }

      if (promptData.length === 0) {
        setPrompts([]);
        return;
      }

      const body = {
        prompts: promptData.map((p) => ({
          prompt_id: p.prompt_id,
          status: p.status,
        })),
      };

      const urlResponse = await fetch(`${URL}/core/prompt/s3/presigned-get`, {
        method: "POST",
        headers: {
          "ngrok-skip-browser-warning": "1",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
        credentials: "include",
      });

      if (!urlResponse.ok) {
        if (urlResponse.status === 422) {
          throw new Error("Error downloading data");
        }
        throw new Error(`Unexpected error: ${urlResponse.status}`);
      }

      const urls = await urlResponse.json();

      const promptsWithUrls = promptData
      .filter(p => p != null) // Фильтруем null и undefined
      .map((p) => {
      const match = urls.find((u) => u.prompt_id === (p.prompt_id || p.id));
        return {
          ...p,
          url: match ? match.url.replace("http://ship-minio:9000", URLLLLLL) : null,
          id: p.id,
          prompt_id: p.prompt_id
        };
      });


      setPrompts(promptsWithUrls);
    } catch (err) {
      console.error("Ошибка при получении промптов:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPromptsWithUrls();
  }, []);

  const handleUploadStart = () => {
    console.log("Загрузка началась. Ждём завершения через WebSocket...");
  };


  if (loading) {
    return <div className={classes.loading}>Loading...</div>;
  }

  console.log('Prompts before render:', prompts);

  return (
    <div className={classes.container}>
      {prompts.length === 0 ? (
        <div className={classes.emptyState}>
          <h2 className={classes.emptyStateTitle}>Create your first prompt</h2>
          {error && <div className={classes.error}>Ошибка: {error}</div>}
          <div className={classes.uploaderContainer}>
            <ImageUploader
              onImageSelect={handleImageSelect}
              onUploadStart={handleUploadStart}
            />
          </div>
        </div>
      ) : (
        <>
          <div className={classes.header}>
            <ImageUploader
              onImageSelect={handleImageSelect}
              onUploadStart={handleUploadStart}
            />
          </div>
          <div className={classes.grid}>
            {prompts.map((prompt) => (
        
              <ModelCard
                key={`${prompt.id}-${prompt.status}`} // Using id as key
                id={prompt.id}
                user_id={prompt.user_id}
                prompt_id={prompt.prompt_id}
                raw_key={prompt.raw_key}
                result_key={prompt.result_key}
                status={prompt.status}
                created_at={prompt.created_at}
                updated_at={prompt.updated_at}
                url={prompt.url}
              />
            ))
            }
          </div>
        </>
      )}
    </div>
  );
};

export default LibraryContent;