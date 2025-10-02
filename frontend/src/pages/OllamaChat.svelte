<script>
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import { token } from "$stores/auth";

  const TEMPERATURE_MIN = 0;
  const TEMPERATURE_MAX = 2;
  const TEMPERATURE_STEP = 0.1;

  let prompt = "";
  let temperature = 0.8;
  let models = [];
  let selectedModel = "";
  let messages = [];
  let isLoading = false;
  let errorMessage = "";
  let controller;

  $: formattedTemperature = Number(temperature ?? 0).toFixed(1);
  $: requestTemperature = Number.isFinite(Number(temperature))
    ? Number(temperature)
    : 0.8;

  onMount(() => {
    loadModels();
  });

  async function loadModels() {
    errorMessage = "";
    try {
      const headers = {};
      const authToken = get(token);
      if (authToken) {
        headers.Authorization = `Bearer ${authToken}`;
      }

      const response = await fetch("/api/ollama/models", { headers });
      if (!response.ok) {
        throw new Error(`Fehler beim Laden der Modelle (${response.status})`);
      }
      const data = await response.json();
      models = data?.models ?? [];
      if (!selectedModel && models.length > 0) {
        selectedModel = models[0]?.model ?? models[0]?.name ?? "";
      }
    } catch (error) {
      console.error(error);
      errorMessage = error?.message ?? "Modelle konnten nicht geladen werden.";
    }
  }

  function resetConversation() {
    messages = [];
    errorMessage = "";
  }

  async function sendPrompt() {
    const trimmedPrompt = prompt.trim();
    if (!trimmedPrompt || !selectedModel || isLoading) {
      return;
    }

    const conversation = [...messages, { role: "user", content: trimmedPrompt }];
    messages = conversation;
    prompt = "";

    const assistantIndex = conversation.length;
    messages = [...conversation, { role: "assistant", content: "" }];

    const payload = {
      model: selectedModel,
      messages: conversation.map(({ role, content }) => ({ role, content })),
      options: {
        temperature: requestTemperature
      }
    };

    const headers = {
      "Content-Type": "application/json"
    };
    const authToken = get(token);
    if (authToken) {
      headers.Authorization = `Bearer ${authToken}`;
    }

    isLoading = true;
    errorMessage = "";
    controller = new AbortController();

    try {
      const response = await fetch("/api/ollama/chat/stream", {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
        signal: controller.signal
      });

      if (!response.ok) {
        const bodyText = await response.text();
        throw new Error(bodyText || `Abfrage fehlgeschlagen (${response.status})`);
      }

      if (!response.body) {
        throw new Error("Antwort enthielt keinen Stream");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let done = false;

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          buffer += decoder.decode(value, { stream: !done });
          buffer = await processBuffer(buffer, assistantIndex);
        }
      }

      if (buffer.trim()) {
        await processBuffer(buffer + "\n", assistantIndex);
      }
    } catch (error) {
      if (error?.name === "AbortError") {
        errorMessage = "Abfrage abgebrochen.";
      } else {
        console.error(error);
        errorMessage = error?.message ?? "Während der Abfrage ist ein Fehler aufgetreten.";
      }
    } finally {
      isLoading = false;
      controller = undefined;
    }
  }

  async function processBuffer(buffer, assistantIndex) {
    const parts = buffer.split("\n");
    const remainder = parts.pop() ?? "";

    for (const part of parts) {
      const trimmed = part.trim();
      if (!trimmed) {
        continue;
      }

      let payload;
      try {
        payload = JSON.parse(trimmed);
      } catch (error) {
        console.warn("Konnte Chunk nicht verarbeiten", error, trimmed);
        continue;
      }

      const content = payload?.message?.content ?? "";
      if (content) {
        messages = messages.map((message, index) =>
          index === assistantIndex
            ? { ...message, content: `${message.content}${content}` }
            : message
        );
      }

      if (payload?.error) {
        throw new Error(payload.error);
      }
    }

    return remainder;
  }

  function stopStreaming() {
    if (controller) {
      controller.abort();
    }
  }
</script>

<section class="chat">
  <header class="chat__header">
    <div>
      <h1>Ollama Chat</h1>
      <p>Stelle Fragen an ein lokal installiertes Modell und beobachte die Live-Antwort.</p>
    </div>
    <div class="chat__actions">
      <button type="button" on:click={resetConversation} class="button button--ghost">
        Verlauf löschen
      </button>
      {#if isLoading}
        <button type="button" on:click={stopStreaming} class="button button--warning">
          Stoppen
        </button>
      {/if}
    </div>
  </header>

  <section class="chat__controls">
    <div class="field">
      <label for="model">Modell</label>
      <select id="model" bind:value={selectedModel} disabled={isLoading || models.length === 0}>
        {#if models.length === 0}
          <option value="" disabled>Keine Modelle verfügbar</option>
        {:else}
          {#each models as model}
            {#if model?.model || model?.name}
              <option value={model.model ?? model.name}>
                {model.model ?? model.name}
              </option>
            {/if}
          {/each}
        {/if}
      </select>
    </div>

    <div class="field">
      <label for="temperature">
        Temperatur
        <span class="field__hint">({formattedTemperature})</span>
      </label>
      <input
        id="temperature"
        type="range"
        min={TEMPERATURE_MIN}
        max={TEMPERATURE_MAX}
        step={TEMPERATURE_STEP}
        bind:value={temperature}
        disabled={isLoading}
      />
    </div>
  </section>

  <section class="chat__conversation" aria-live="polite">
    {#if messages.length === 0}
      <p class="chat__placeholder">Noch keine Nachrichten – starte den Dialog mit einem Prompt.</p>
    {:else}
      {#each messages as message, index}
        <article class:message--assistant={message.role === "assistant"} class="message">
          <header>
            <span class="message__role">
              {message.role === "assistant" ? "Assistent" : "Du"}
            </span>
            {#if message.role === "assistant" && index === messages.length - 1 && isLoading}
              <span class="message__status">schreibt …</span>
            {/if}
          </header>
          <p>{message.content}</p>
        </article>
      {/each}
    {/if}
  </section>

  <form class="chat__prompt" on:submit|preventDefault={sendPrompt}>
    <label class="sr-only" for="prompt">Prompt</label>
    <textarea
      id="prompt"
      rows="4"
      placeholder="Beschreibe deine Frage oder Aufgabe"
      bind:value={prompt}
      required
      disabled={isLoading || !selectedModel}
    ></textarea>
    <div class="chat__prompt-actions">
      <button type="submit" class="button" disabled={isLoading || !selectedModel}>
        Senden
      </button>
    </div>
  </form>

  {#if errorMessage}
    <p class="chat__error" role="alert">{errorMessage}</p>
  {/if}
</section>

<style>
  :global(body) {
    background: #f5f7fb;
  }

  .chat {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: clamp(1.5rem, 2vw, 2.5rem);
    max-width: 960px;
    margin: 0 auto;
    color: #111827;
  }

  .chat__header {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
  }

  .chat__header h1 {
    margin: 0;
    font-size: clamp(1.8rem, 2.6vw, 2.3rem);
  }

  .chat__header p {
    margin: 0.25rem 0 0;
    color: #4b5563;
  }

  .chat__actions {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }

  .chat__controls {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    background: white;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    font-size: 0.95rem;
  }

  .field label {
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .field select,
  .chat textarea {
    border: 1px solid #cbd5f5;
    border-radius: 10px;
    padding: 0.75rem;
    font-size: 1rem;
    font-family: inherit;
    color: inherit;
    background: white;
    transition: border-color 0.2s ease;
  }

  .field select:focus,
  .chat textarea:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
  }

  .field__hint {
    font-weight: 500;
    font-size: 0.85rem;
    color: #6b7280;
  }

  .chat__conversation {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
    min-height: 240px;
  }

  .chat__placeholder {
    margin: 0;
    color: #6b7280;
    font-style: italic;
  }

  .message {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    padding: 1rem;
    border-radius: 10px;
    background: #eef2ff;
  }

  .message--assistant {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
  }

  .message__role {
    font-weight: 600;
    color: #4338ca;
  }

  .message--assistant .message__role {
    color: #2563eb;
  }

  .message__status {
    font-size: 0.85rem;
    color: #6b7280;
  }

  .message p {
    margin: 0;
    white-space: pre-wrap;
    line-height: 1.5;
  }

  .chat__prompt {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .chat__prompt textarea {
    resize: vertical;
    min-height: 140px;
  }

  .chat__prompt-actions {
    display: flex;
    justify-content: flex-end;
  }

  .button {
    appearance: none;
    border: none;
    border-radius: 999px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    transition: transform 0.1s ease, box-shadow 0.2s ease;
  }

  .button:hover,
  .button:focus-visible {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(99, 102, 241, 0.35);
  }

  .button:disabled {
    opacity: 0.65;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .button--ghost {
    background: transparent;
    color: #1f2937;
    border: 1px solid rgba(99, 102, 241, 0.4);
  }

  .button--warning {
    background: linear-gradient(135deg, #f97316, #f59e0b);
    color: #111827;
  }

  .chat__error {
    margin: 0;
    padding: 0.85rem 1rem;
    border-radius: 10px;
    background: rgba(239, 68, 68, 0.12);
    color: #b91c1c;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }

  @media (max-width: 640px) {
    .chat {
      padding: 1rem;
    }

    .chat__controls {
      grid-template-columns: 1fr;
    }

    .chat__actions {
      width: 100%;
      justify-content: flex-end;
    }
  }
</style>
