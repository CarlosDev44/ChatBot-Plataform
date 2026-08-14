"use client";

import {
  Bot,
  CheckCircle2,
  FileText,
  Loader2,
  MessageSquarePlus,
  PanelLeft,
  RefreshCcw,
  Send,
  Sparkles,
  Trash2,
  Upload,
  UserRound,
  Wifi,
  WifiOff,
} from "lucide-react";
import { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";

type Role = "user" | "assistant";

type Message = {
  id: string | number;
  role: Role;
  content: string;
};

type Conversation = {
  id: number;
  title: string;
  messages: Message[];
};

type StreamEvent =
  | { type: "meta"; conversation_id: number }
  | { type: "delta"; content: string }
  | { type: "done" };

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const quickPrompts = [
  "Resume el documento cargado en 5 puntos.",
  "Que temas principales aparecen en la base de conocimiento?",
  "Dame una respuesta breve y cita solo lo que sepas por el contexto.",
];

export default function Home() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const activeConversation = useMemo(
    () => conversations.find((conversation) => conversation.id === activeConversationId),
    [activeConversationId, conversations],
  );

  const refreshConversations = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/conversations`);

      if (!response.ok) {
        throw new Error("No se pudieron cargar las conversaciones.");
      }

      const data = (await response.json()) as Conversation[];
      setConversations(data);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Error inesperado.");
    }
  }, []);

  useEffect(() => {
    refreshConversations();
  }, [refreshConversations]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isSending]);

  function startNewChat() {
    setActiveConversationId(null);
    setMessages([]);
    setInput("");
    setError(null);
  }

  async function openConversation(conversation: Conversation) {
    setActiveConversationId(conversation.id);
    setMessages(conversation.messages);
    setError(null);
  }

  async function deleteConversation(conversationId: number) {
    try {
      const response = await fetch(`${API_URL}/conversations/${conversationId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("No se pudo eliminar la conversación.");
      }

      if (activeConversationId === conversationId) {
        startNewChat();
      }

      await refreshConversations();
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Error inesperado.");
    }
  }

  async function uploadDocument(file: File) {
    const formData = new FormData();
    formData.append("file", file);

    setIsUploading(true);
    setUploadStatus(null);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/documents`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("No se pudo subir el documento.");
      }

      const data = (await response.json()) as { filename: string };
      setUploadStatus(`${data.filename} listo para consultar.`);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Error inesperado.");
    } finally {
      setIsUploading(false);
    }
  }

  async function sendMessage(event?: FormEvent<HTMLFormElement>, forcedMessage?: string) {
    event?.preventDefault();

    const message = (forcedMessage ?? input).trim();
    if (!message || isSending) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: message,
    };
    const assistantId = `assistant-${Date.now()}`;

    setMessages((current) => [
      ...current,
      userMessage,
      { id: assistantId, role: "assistant", content: "" },
    ]);
    setInput("");
    setIsSending(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
          conversation_id: activeConversationId,
        }),
      });

      if (!response.ok || !response.body) {
        throw new Error("No se pudo iniciar el streaming de la respuesta.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const events = buffer.split("\n\n");
        buffer = events.pop() ?? "";

        for (const rawEvent of events) {
          const line = rawEvent
            .split("\n")
            .find((item) => item.startsWith("data: "));

          if (!line) continue;

          const parsed = JSON.parse(line.replace("data: ", "")) as StreamEvent;

          if (parsed.type === "meta") {
            setActiveConversationId(parsed.conversation_id);
          }

          if (parsed.type === "delta") {
            setMessages((current) =>
              current.map((item) =>
                item.id === assistantId
                  ? { ...item, content: `${item.content}${parsed.content}` }
                  : item,
              ),
            );
          }
        }
      }

      await refreshConversations();
    } catch (caughtError) {
      setMessages((current) =>
        current.map((item) =>
          item.id === assistantId
            ? {
                ...item,
                content:
                  "No pude conectar con el streaming. Revisa que el backend esté corriendo y vuelve a intentar.",
              }
            : item,
        ),
      );
      setError(caughtError instanceof Error ? caughtError.message : "Error inesperado.");
    } finally {
      setIsSending(false);
    }
  }

  return (
    <main className="shell">
      <aside className={`sidebar ${isSidebarOpen ? "is-open" : "is-closed"}`}>
        <div className="brand">
          <div className="brand-mark">
            <Sparkles size={20} />
          </div>
          <div>
            <strong>RAG Chat</strong>
            <span>Plataforma IA</span>
          </div>
        </div>

        <button className="primary-action" onClick={startNewChat} type="button">
          <MessageSquarePlus size={18} />
          Nueva conversación
        </button>

        <label className="upload-zone">
          <input
            accept="application/pdf"
            disabled={isUploading}
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) uploadDocument(file);
              event.target.value = "";
            }}
            type="file"
          />
          {isUploading ? <Loader2 className="spin" size={20} /> : <Upload size={20} />}
          <span>{isUploading ? "Procesando PDF..." : "Subir PDF"}</span>
        </label>

        {uploadStatus && (
          <div className="status-pill success">
            <CheckCircle2 size={16} />
            {uploadStatus}
          </div>
        )}

        <div className="sidebar-section">
          <div className="section-title">
            <span>Conversaciones</span>
            <button aria-label="Actualizar conversaciones" onClick={refreshConversations} type="button">
              <RefreshCcw size={16} />
            </button>
          </div>

          <div className="conversation-list">
            {conversations.map((conversation) => (
              <button
                className={`conversation-item ${
                  conversation.id === activeConversationId ? "active" : ""
                }`}
                key={conversation.id}
                onClick={() => openConversation(conversation)}
                type="button"
              >
                <FileText size={17} />
                <span>{conversation.title}</span>
                <Trash2
                  aria-label="Eliminar conversación"
                  onClick={(event) => {
                    event.stopPropagation();
                    deleteConversation(conversation.id);
                  }}
                  role="button"
                  size={16}
                  tabIndex={0}
                />
              </button>
            ))}
          </div>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <button
            aria-label="Mostrar u ocultar panel"
            className="icon-button"
            onClick={() => setIsSidebarOpen((current) => !current)}
            type="button"
          >
            <PanelLeft size={19} />
          </button>
          <div>
            <p>Chat con documentos</p>
            <h1>{activeConversation?.title ?? "Nueva consulta"}</h1>
          </div>
          <div className={`connection ${error ? "offline" : "online"}`}>
            {error ? <WifiOff size={16} /> : <Wifi size={16} />}
            {error ? "Revisar API" : "Streaming listo"}
          </div>
        </header>

        {error && <div className="error-banner">{error}</div>}

        <div className="chat-panel">
          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-orbit">
                <Bot size={34} />
              </div>
              <h2>Haz preguntas sobre tus documentos</h2>
              <p>
                Sube un PDF, inicia una conversación y recibe respuestas en streaming con el
                contexto recuperado por el backend.
              </p>
              <div className="prompt-grid">
                {quickPrompts.map((prompt) => (
                  <button key={prompt} onClick={() => sendMessage(undefined, prompt)} type="button">
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message) => (
                <article className={`message ${message.role}`} key={message.id}>
                  <div className="avatar">
                    {message.role === "assistant" ? <Bot size={18} /> : <UserRound size={18} />}
                  </div>
                  <div className="bubble">
                    <span>{message.role === "assistant" ? "Asistente" : "Tú"}</span>
                    <p>
                      {message.content ||
                        (message.role === "assistant" && isSending ? "Pensando..." : "")}
                    </p>
                  </div>
                </article>
              ))}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        <form className="composer" onSubmit={sendMessage}>
          <textarea
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
              }
            }}
            placeholder="Pregunta algo sobre el documento..."
            value={input}
          />
          <button disabled={isSending || !input.trim()} type="submit">
            {isSending ? <Loader2 className="spin" size={20} /> : <Send size={20} />}
          </button>
        </form>
      </section>
    </main>
  );
}
