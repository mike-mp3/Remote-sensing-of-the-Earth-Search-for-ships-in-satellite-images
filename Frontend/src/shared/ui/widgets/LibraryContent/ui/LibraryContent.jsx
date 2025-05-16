import { useEffect, useState, useRef } from "react";
import * as classes from "./LibraryContent.module.scss";
import { ModelCard } from "@/shared/ui/entities/ModelCard";
import { ImageUploader } from "@/shared/ui/entities/ImageUploader";




const LibraryContent = () => {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const wsRef = useRef(null);
  const URL = import.meta.env.VITE_API_BASE_URL;

  const URLLLLLL = URL + "/s3";


  const fetchPromptsWithUrls = async () => {
    try {
      const response = await fetch(`${URL}/core/prompt`, {
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true"
        },
        credentials: "include",
      });

      if (!response.ok) {
        if (response.status === 404) {
          console.warn("No prompts found");
          setPrompts([]); // устанавливаем пустой список
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

      const urlResponse = await fetch(`${URL}/core/prompt/s3/presigned-get`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
          credentials: "include",
        }
      );

      if (!urlResponse.ok) {
        if (urlResponse.status === 422) {
          throw new Error("Error downloading data");
        }
        throw new Error(`Unexpected error: ${urlResponse.status}`);
      }

      const urls = await urlResponse.json();
      console.log(urls);
      
      const promptsWithUrls = promptData.map((p) => {
        const match = urls.find((u) => u.prompt_id === p.prompt_id);
        return {
          ...p,
          url: match ? match.url.replace("http://ship-minio:9000", URLLLLLL) : null,
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

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    console.log("Selected image:", file);
  };

  const handleUploadStart = () => {
    console.log("Загрузка началась. Открываем WebSocket...");

    if (wsRef.current) {
      wsRef.current.close();
    }
    const WS_API = URL.replace("https", "wss");
    const ws = new WebSocket(`${WS_API}/ws/prompt`);

    ws.onopen = () => {
      console.log("✅ WebSocket соединение открыто");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("Сообщение из WebSocket:", message);
      if (message.status === "success") {
        fetchPromptsWithUrls();
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket ошибка:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket соединение закрыто");
    };

    wsRef.current = ws;
  };

  if (loading) {
    return <div className={classes.loading}>Loading...</div>;
  }

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
                key={prompt.prompt_id}
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
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default LibraryContent;
