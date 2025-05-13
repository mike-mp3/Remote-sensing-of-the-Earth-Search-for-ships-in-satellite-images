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

  const fetchPromptsWithUrls = async () => {
    try {
      const response = await fetch("https://fd5c-89-191-234-252.ngrok-free.app/s3/prompt");

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("maybe there are no prompts");
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

      const urlResponse = await fetch(
        "https://fd5c-89-191-234-252.ngrok-free.app/s3/prompt/s3/presigned-get",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        }
      );

      if (!urlResponse.ok) {
        if (urlResponse.status === 422) {
          throw new Error("Error downloading data");
        }
        throw new Error(`Unexpected error: ${urlResponse.status}`);
      }

      const urls = await urlResponse.json();
      const promptsWithUrls = promptData.map((p) => {
        const match = urls.find((u) => u.prompt_id === p.prompt_id);
        return {
          ...p,
          url: match ? match.url : null,
        };
      });

      setPrompts(promptsWithUrls);
    } catch (err) {
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

    // Закрыть предыдущее соединение если есть
    if (wsRef.current) {
      wsRef.current.close();
    }

    // TODO: заменить на реальный адрес вашего WebSocket-сервера
    const ws = new WebSocket("wss://fd5c-89-191-234-252.ngrok-free.app/ws/prompt");

    ws.onopen = () => {
      console.log("✅ WebSocket соединение открыто");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("📨 Сообщение из WebSocket:", message);
      // TODO: required message =============================================>>>>>>>>>> блять 
      // if (message.status === 'done') fetchPromptsWithUrls();
    };

    ws.onerror = (error) => {
      console.error("❌ WebSocket ошибка:", error);
    };

    ws.onclose = () => {
      console.log("🔌 WebSocket соединение закрыто");
    };

    wsRef.current = ws;
  };

  if (loading) {
    return <div className={classes.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={classes.error}>{error}</div>;
  }

  if (!Array.isArray(prompts) || prompts.length === 0) {
    return (
      <div className={classes.emptyState}>
        <h2 className={classes.emptyStateTitle}>Create your first prompt!</h2>
        <div className={classes.uploaderContainer}>
          <ImageUploader
            onImageSelect={handleImageSelect}
            onUploadStart={handleUploadStart}
          />
        </div>
      </div>
    );
  }

  return (
    <div className={classes.container}>
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
    </div>
  );
};

export default LibraryContent;
