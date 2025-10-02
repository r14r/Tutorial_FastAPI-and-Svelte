<script>
  const gptMenu = {
    count: 88,
    items: [
      { label: "Erkunden" },
      { label: "Find Dances" },
      { label: "L Bollingstedt" },
      { label: "Codex" }
    ]
  };

  const projectMenu = [
    { label: "Neues Projekt", accent: "+" },
    { label: "Enrichment: AI" },
    { label: "Klage E 7" },
    { label: "Eindiane-community.de" },
    { label: "Ki-Tools" },
    { label: "Mehr anzeigen", muted: true }
  ];

  const quickPrompts = [
    "Skizziere einen Projektplan für dieses Quartal.",
    "Erstelle eine Executive Summary zum letzten Sprint.",
    "Welche Erkenntnisse liefern unsere Support-Tickets?",
    "Formuliere Ziele für das nächste Team-Meeting."
  ];

  let searchQuery = "";
  let promptDraft = "";
</script>

<section class="workspace">
  <aside class="sidebar">
    <button class="card card--cta" type="button">
      <span class="card__label">Neuer Chat</span>
      <span class="card__icon">＋</span>
    </button>

    <label class="card card--search">
      <span class="card__icon" aria-hidden="true">🔍</span>
      <input
        type="search"
        placeholder="Chats suchen"
        bind:value={searchQuery}
        aria-label="Chats suchen"
      />
    </label>

    <button class="card card--link" type="button">Bibliothek</button>

    <section class="card card--menu">
      <header class="card__header">
        <h2>GPTs</h2>
        <span class="chip">{gptMenu.count}</span>
      </header>
      <ul>
        {#each gptMenu.items as item}
          <li>
            <button class="menu-item" type="button">{item.label}</button>
          </li>
        {/each}
      </ul>
    </section>

    <section class="card card--menu">
      <header class="card__header">
        <h2>Projekte</h2>
      </header>
      <ul>
        {#each projectMenu as item}
          <li>
            <button
              class="menu-item"
              class:menu-item--muted={item.muted}
              type="button"
            >
              {#if item.accent}
                <span class="menu-item__accent">{item.accent}</span>
              {/if}
              {item.label}
            </button>
          </li>
        {/each}
      </ul>
    </section>
  </aside>

  <main class="content">
    <header class="content__hero">
      <h1>Was liegt heute an?</h1>
      <form class="prompt" on:submit|preventDefault={() => {}}>
        <input
          type="text"
          placeholder="Stelle irgendeine Frage"
          bind:value={promptDraft}
          aria-label="Prompt eingeben"
        />
        <button class="prompt__submit" type="submit" aria-label="Absenden">
          <span aria-hidden="true">⮞</span>
        </button>
      </form>
    </header>

    <section class="suggestions">
      <h2>Vorschläge für den Start</h2>
      <ul>
        {#each quickPrompts as prompt}
          <li>
            <button class="suggestion" type="button">{prompt}</button>
          </li>
        {/each}
      </ul>
    </section>
  </main>
</section>

<style>
  :global(body) {
    background-color: #0b0c10;
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }

  .workspace {
    display: grid;
    grid-template-columns: clamp(260px, 25vw, 320px) 1fr;
    gap: 1.75rem;
    padding: clamp(1.5rem, 3vw, 2.5rem);
    color: #f5f7fb;
    min-height: 100vh;
  }

  .sidebar {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    position: sticky;
    top: clamp(1.5rem, 3vw, 2.5rem);
    align-self: start;
  }

  .card {
    background: rgba(24, 27, 39, 0.92);
    border-radius: 18px;
    border: 1px solid rgba(88, 97, 127, 0.35);
    padding: 1.1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: inherit;
    text-align: left;
  }

  .card--cta {
    justify-content: space-between;
    font-size: 1rem;
    font-weight: 600;
    background: linear-gradient(135deg, rgba(79, 123, 255, 0.65), rgba(168, 85, 247, 0.6));
    border: none;
    cursor: pointer;
  }

  .card--cta .card__icon {
    font-size: 1.35rem;
  }

  .card--search {
    cursor: text;
  }

  .card--search input {
    border: none;
    outline: none;
    background: transparent;
    color: inherit;
    width: 100%;
    font-size: 0.95rem;
  }

  .card--link {
    justify-content: center;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .card--link:hover,
  .card--link:focus-visible,
  .menu-item:hover,
  .menu-item:focus-visible,
  .suggestion:hover,
  .suggestion:focus-visible {
    background: rgba(124, 136, 203, 0.16);
  }

  .card--menu {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }

  .card__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
  }

  .card__header h2 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.01em;
  }

  .chip {
    background: rgba(124, 136, 203, 0.2);
    border-radius: 999px;
    padding: 0.1rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #cbd2ff;
  }

  .card--menu ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .menu-item {
    width: 100%;
    background: rgba(47, 53, 75, 0.55);
    border: 1px solid rgba(88, 97, 127, 0.2);
    border-radius: 12px;
    padding: 0.75rem 0.9rem;
    color: inherit;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    justify-content: flex-start;
    font-size: 0.92rem;
    cursor: pointer;
    transition: background 0.2s ease, border 0.2s ease;
  }

  .menu-item--muted {
    color: #aab1c5;
  }

  .menu-item__accent {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(203, 210, 255, 0.16);
    border-radius: 8px;
    width: 1.5rem;
    height: 1.5rem;
    font-weight: 600;
    font-size: 0.85rem;
  }

  .content {
    background: rgba(24, 27, 39, 0.78);
    border-radius: 28px;
    border: 1px solid rgba(88, 97, 127, 0.25);
    padding: clamp(1.75rem, 4vw, 2.75rem);
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
    box-shadow: 0 40px 60px rgba(5, 7, 15, 0.45);
  }

  .content__hero h1 {
    font-size: clamp(2rem, 5vw, 2.9rem);
    margin: 0 0 1.75rem;
  }

  .prompt {
    background: rgba(12, 14, 24, 0.85);
    border-radius: 28px;
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem 0.75rem 1.25rem;
    border: 1px solid rgba(88, 97, 127, 0.35);
  }

  .prompt input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: inherit;
    font-size: 1.05rem;
  }

  .prompt__submit {
    border: none;
    background: rgba(76, 108, 255, 0.9);
    color: #fff;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    display: grid;
    place-items: center;
    cursor: pointer;
    font-size: 1.1rem;
    transition: transform 0.2s ease, background 0.2s ease;
  }

  .prompt__submit:hover,
  .prompt__submit:focus-visible {
    transform: translateX(2px);
    background: rgba(113, 93, 255, 0.95);
  }

  .suggestions h2 {
    margin: 0 0 1rem;
    font-size: 1rem;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    color: #aab1c5;
  }

  .suggestions ul {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 0.75rem;
    margin: 0;
    padding: 0;
  }

  .suggestion {
    background: rgba(47, 53, 75, 0.6);
    border: 1px solid rgba(88, 97, 127, 0.25);
    border-radius: 16px;
    color: inherit;
    padding: 1rem;
    text-align: left;
    font-size: 0.95rem;
    cursor: pointer;
    transition: background 0.2s ease, border 0.2s ease;
  }

  @media (max-width: 1024px) {
    .workspace {
      grid-template-columns: 1fr;
    }

    .sidebar {
      position: static;
      flex-direction: row;
      flex-wrap: wrap;
    }

    .card {
      flex: 1 1 calc(50% - 0.5rem);
    }

    .card--menu {
      flex: 1 1 100%;
    }
  }
</style>
