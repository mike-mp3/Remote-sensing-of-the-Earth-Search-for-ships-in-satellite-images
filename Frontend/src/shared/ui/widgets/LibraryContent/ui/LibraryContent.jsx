import { useEffect, useState } from "react";
import * as classes from "./LibraryContent.module.scss";
import { ModelCard } from "@/shared/ui/entities/ModelCard";
import { ImageUploader } from "@/shared/ui/entities/ImageUploader";

const LibraryContent = () => {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    const fetchPrompts = async () => {
      try {
        console.log("Fetching prompts...");
        const response = await fetch("/models.json");
        console.log("Response status:", response.status);
        console.log("Response headers:", Object.fromEntries(response.headers.entries()));

        if (!response.ok) {
          // обработка статус-кодов
          if (response.status === 404) {
            const errorData = await response.json();
            const detail = errorData?.detail?.[0] || "Prompts not found";
            console.error("Error 404:", detail);
            throw new Error(detail);
          }

          if (response.status === 422) {
            const errorData = await response.json();
            const messages = errorData?.detail?.map(err => err.msg).join(", ") || "Validation error";
            console.error("Error 422:", messages);
            throw new Error(messages);
          }

          throw new Error(`Unexpected error: ${response.status}`);
        }

        // Проверяем тип контента
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          console.error("Invalid content type:", contentType);
          throw new Error("Server returned non-JSON response");
        }

        // Обработка пустого тела
        const text = await response.text();
        console.log("Response text:", text);

        if (!text) {
          console.error("Empty response from server");
          throw new Error("Empty response from server");
        }

        let data;
        try {
          data = JSON.parse(text);
          console.log("Parsed data:", data);
        } catch (jsonErr) {
          console.error("Failed to parse JSON:", jsonErr.message);
          console.error("Raw text:", text);
          throw new Error("Invalid JSON format");
        }

        if (!Array.isArray(data)) {
          console.error("Data is not an array:", data);
          throw new Error("Expected array of prompts");
        }

        setPrompts(data);
      } catch (err) {
        console.error("Fetch error:", err.message);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPrompts();
  }, []);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    // TODO: Здесь будет логика отправки файла на сервер
    console.log('Selected image:', file);
  };

  if (loading) {
    return <div className={classes.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={classes.error}>{error}</div>;
  }

  if (prompts.length === 0) {
    return (
      <div className={classes.emptyState}>
        <h2 className={classes.emptyStateTitle}>Create your first prompt!</h2>
        <div className={classes.uploaderContainer}>
          <ImageUploader onImageSelect={handleImageSelect} />
        </div>
      </div>
    );
  }

  return (
    <div className={classes.container}>
      <div className={classes.header}>
        <ImageUploader onImageSelect={handleImageSelect} />
      </div>
      <div className={classes.grid}>
        {prompts.map((prompt) => (
          <ModelCard
            key={prompt.id}
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
