<script>
  const promptPresets = [
    {
      title: "Brainstorming",
      description: "Generate creative ideas, strategies, and outlines for any topic.",
      icon: "💡",
      suggestions: [
        "Help me plan a community hackathon weekend.",
        "Outline a whitepaper about privacy-first AI assistants.",
        "Brainstorm five marketing angles for a new note taking app."
      ]
    },
    {
      title: "Writing",
      description: "Draft blog posts, documentation, and long-form content collaboratively.",
      icon: "✍️",
      suggestions: [
        "Write a release announcement for our latest feature launch.",
        "Improve the tone of this executive summary and keep it concise.",
        "Create a welcome email sequence for first-time users."
      ]
    },
    {
      title: "Data analysis",
      description: "Interrogate datasets, debug queries, and translate results into insights.",
      icon: "📊",
      suggestions: [
        "Explain why yesterday's retention dropped by 3%.",
        "Summarize the anomalies in this SQL result.",
        "Suggest A/B test ideas based on these funnel metrics."
      ]
    }
  ];

  const projectWorkspaces = [
    {
      name: "Docs revamp",
      status: { label: "In review", variant: "in-review" },
      description:
        "A shared thread containing the draft documentation for the onboarding flow redesign.",
      collaborators: ["Alana", "Kai"],
      updatedAt: "2h ago"
    },
    {
      name: "Customer insights",
      status: { label: "Active", variant: "active" },
      description:
        "Research project that aggregates interview notes and converts them into actionable insights.",
      collaborators: ["Diego", "Morgan", "Priya"],
      updatedAt: "Yesterday"
    },
    {
      name: "Roadmap planning",
      status: { label: "Scheduled", variant: "scheduled" },
      description:
        "Workspace for quarterly planning with preloaded prompts and product requirement templates.",
      collaborators: ["Zara"],
      updatedAt: "Mon"
    }
  ];

  const customGPTs = [
    {
      name: "Release note polisher",
      description: "Specialized in translating technical changelogs into user-friendly release notes.",
      capabilities: ["Tone matching", "Localization", "Style guardrails"],
      accent: "🎉"
    },
    {
      name: "Data detective",
      description: "Inspects dashboards, SQL, and spreadsheets to draft concise analytic briefings.",
      capabilities: ["CSV parsing", "SQL reasoning", "Chart explanation"],
      accent: "🕵️"
    },
    {
      name: "Code reviewer",
      description: "Offers pull-request friendly reviews with actionable improvement suggestions.",
      capabilities: ["Lint awareness", "Complexity scoring", "Testing tips"],
      accent: "🧑‍💻"
    }
  ];

  const chatThreads = [
    {
      id: "product-sync",
      title: "Produkt-Sync",
      lastActive: "Assistant • vor 2 Stunden",
      messages: [
        {
          role: "user",
          content: "Summarize the last product sync and highlight next steps for the mobile team."
        },
        {
          role: "assistant",
          content:
            "Here is a concise recap of the sync along with the follow-up owners: \n\n• Ship beta build to TestFlight — Morgan\n• Prepare usability survey — Priya\n• Update crash monitoring alerts — Diego"
        }
      ]
    },
    {
      id: "marketing-ideas",
      title: "Marketingideen",
      lastActive: "Du • gestern",
      messages: [
        {
          role: "user",
          content: "Brainstorm five marketing angles for our new onboarding tutorial."
        },
        {
          role: "assistant",
          content:
            "Consider positioning around: \n\n1. Rapid setup in under 5 minutes\n2. Built-in analytics to prove ROI\n3. Collaborative reviews with inline feedback\n4. Enterprise-ready security defaults\n5. Seamless integrations with the current stack"
        }
      ]
    },
    {
      id: "support-update",
      title: "Support-Update",
      lastActive: "Assistant • Montag",
      messages: [
        {
          role: "user",
          content: "Draft a status message informing customers about the resolved outage from this morning."
        },
        {
          role: "assistant",
          content:
            "Here's a status message you can use: \n\n‘We identified and resolved the authentication outage from this morning. All services are operating normally again as of 10:24 CET. Thank you for your patience while we implemented the fix.’"
        }
      ]
    }
  ];

  const sidebarProjects = projectWorkspaces.map((project) => ({
    name: project.name,
    status: `${project.status.label} • Aktualisiert ${project.updatedAt}`,
    collaborators: project.collaborators
  }));

  let promptInput = "";
  let activeChatId = chatThreads[0]?.id ?? null;

  $: activeChat = chatThreads.find((thread) => thread.id === activeChatId) ?? chatThreads[0];

  function loadSuggestion(suggestion) {
    promptInput = suggestion;
  }
</script>

<section class="page">
  <header class="page__header">
    <div>
      <h1>Workspace</h1>
      <p>Design a ChatGPT-style surface for navigating prompts, projects, and custom GPTs.</p>
    </div>
    <button class="primary">New chat</button>
  </header>

  <div class="page__grid">
    <aside class="panel panel--sidebar">
      <section class="sidebar-section">
        <header>
          <h2>Chat</h2>
          <button class="secondary secondary--ghost" type="button">New Chat</button>
        </header>
        <ul class="sidebar-list">
          {#each chatThreads as thread}
            <li>
              <button
                type="button"
                class="sidebar-item"
                class:active={thread.id === activeChatId}
                on:click={() => (activeChatId = thread.id)}
              >
                <span class="sidebar-item__title">{thread.title}</span>
                <span class="sidebar-item__meta">{thread.lastActive}</span>
              </button>
            </li>
          {/each}
        </ul>
      </section>

      <section class="sidebar-section">
        <header>
          <h2>Projekte</h2>
          <button class="secondary secondary--ghost" type="button">New Project</button>
        </header>
        <ul class="sidebar-list sidebar-list--projects">
          {#each sidebarProjects as project}
            <li>
              <div class="sidebar-item sidebar-item--static">
                <span class="sidebar-item__title">{project.name}</span>
                <span class="sidebar-item__meta">{project.status}</span>
                {#if project.collaborators?.length}
                  <span class="sidebar-item__tags">
                    {#each project.collaborators as collaborator}
                      <span class="pill pill--tiny">{collaborator}</span>
                    {/each}
                  </span>
                {/if}
              </div>
            </li>
          {/each}
        </ul>
      </section>

      {#if activeChat}
        <section class="sidebar-section sidebar-section--active">
          <header>
            <h2>Aktiver Chat</h2>
          </header>
          <div class="message-log">
            {#each activeChat.messages as message}
              <article class={`message message--${message.role}`}>
                <span class="message__role">{message.role === "assistant" ? "GPT" : "Du"}</span>
                <p>{message.content}</p>
              </article>
            {/each}
          </div>
          <label class="message-input">
            <span>Compose</span>
            <textarea
              bind:value={promptInput}
              rows="4"
              placeholder="Ask a follow-up or paste a task"
            ></textarea>
          </label>
          <button class="primary" disabled={!promptInput.trim()}>Send</button>
        </section>
      {/if}
    </aside>

    <main class="panel panel--main">
      <section class="card-group">
        <header>
          <h2>Prompt library</h2>
          <p>Jumpstart conversations with reusable presets curated for your team.</p>
        </header>
        <div class="grid">
          {#each promptPresets as preset}
            <article class="card">
              <div class="card__icon">{preset.icon}</div>
              <div class="card__body">
                <h3>{preset.title}</h3>
                <p>{preset.description}</p>
                <button
                  class="secondary secondary--ghost"
                  type="button"
                  on:click={() => loadSuggestion(preset.suggestions[0])}
                >
                  Load starter prompt
                </button>
                <ul>
                  {#each preset.suggestions as suggestion}
                    <li>
                      <button type="button" on:click|stopPropagation={() => loadSuggestion(suggestion)}>
                        {suggestion}
                      </button>
                    </li>
                  {/each}
                </ul>
              </div>
            </article>
          {/each}
        </div>
      </section>

      <section class="card-group">
        <header>
          <h2>Project workspaces</h2>
          <p>Open collaborative threads and keep teammates aligned across initiatives.</p>
        </header>
        <div class="grid grid--projects">
          {#each projectWorkspaces as project}
            <article class="card card--project">
              <div class="card__header">
                <h3>{project.name}</h3>
                <span class={`status status--${project.status.variant}`}>{project.status.label}</span>
              </div>
              <p>{project.description}</p>
              <footer>
                <span class="pill-group">
                  {#each project.collaborators as collaborator}
                    <span class="pill">{collaborator}</span>
                  {/each}
                </span>
                <span class="muted">Updated {project.updatedAt}</span>
              </footer>
            </article>
          {/each}
        </div>
      </section>

      <section class="card-group">
        <header>
          <h2>Custom GPTs</h2>
          <p>Deploy specialized assistants with targeted knowledge and guardrails.</p>
        </header>
        <div class="grid grid--gpts">
          {#each customGPTs as gpt}
            <article class="card card--gpt">
              <div class="card__icon card__icon--gpt">{gpt.accent}</div>
              <div class="card__body">
                <h3>{gpt.name}</h3>
                <p>{gpt.description}</p>
                <div class="pill-group">
                  {#each gpt.capabilities as capability}
                    <span class="pill pill--outline">{capability}</span>
                  {/each}
                </div>
                <button class="secondary">Open</button>
              </div>
            </article>
          {/each}
        </div>
      </section>
    </main>
  </div>
</section>

<style>
  :global(body) {
    background-color: #0b0c10;
  }

  .page {
    padding: 2rem clamp(1rem, 4vw, 3rem);
    color: #f8f9fb;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .page__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }

  .page__header h1 {
    font-size: clamp(1.75rem, 3vw, 2.5rem);
    margin: 0;
  }

  .page__header p {
    margin: 0.35rem 0 0;
    color: #aab1c0;
  }

  .page__grid {
    display: grid;
    grid-template-columns: minmax(260px, 320px) 1fr;
    gap: 1.5rem;
  }

  .panel {
    background: rgba(26, 29, 40, 0.9);
    border-radius: 18px;
    padding: 1.5rem;
    box-shadow: 0 18px 48px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .panel--sidebar {
    position: sticky;
    top: 1.5rem;
    height: fit-content;
  }

  .panel h2 {
    margin: 0;
    font-size: 1.2rem;
  }

  .sidebar-section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .sidebar-section + .sidebar-section {
    padding-top: 1.25rem;
    border-top: 1px solid rgba(62, 70, 96, 0.6);
  }

  .sidebar-section header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
  }

  .sidebar-section header h2 {
    font-size: 1rem;
  }

  .sidebar-section--active {
    gap: 1rem;
  }

  .sidebar-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .sidebar-item {
    width: 100%;
    background: rgba(17, 19, 27, 0.9);
    border: 1px solid rgba(59, 67, 92, 0.6);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    text-align: left;
    color: inherit;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    transition: border-color 0.18s ease, background 0.18s ease, transform 0.18s ease;
  }

  .sidebar-item:hover {
    border-color: rgba(120, 131, 164, 0.9);
    transform: translateY(-1px);
  }

  .sidebar-item.active {
    border-color: rgba(99, 133, 255, 0.85);
    background: rgba(33, 40, 64, 0.9);
  }

  .sidebar-item--static {
    cursor: default;
  }

  .sidebar-item--static:hover {
    transform: none;
    border-color: rgba(59, 67, 92, 0.6);
  }

  .sidebar-item__title {
    font-weight: 600;
    font-size: 0.95rem;
  }

  .sidebar-item__meta {
    font-size: 0.8rem;
    color: #7d8bad;
  }

  .sidebar-item__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 0.35rem;
  }

  .sidebar-list--projects .sidebar-item {
    gap: 0.35rem;
  }

  .message-log {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-height: 320px;
    overflow-y: auto;
    padding-right: 0.5rem;
  }

  .message {
    background: rgba(18, 20, 28, 0.9);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    border: 1px solid transparent;
  }

  .message--assistant {
    border-color: rgba(101, 163, 255, 0.4);
  }

  .message__role {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #7d89a1;
  }

  .message p {
    margin: 0;
    line-height: 1.4;
    white-space: pre-wrap;
  }

  .message-input {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.9rem;
  }

  .message-input textarea {
    background: rgba(15, 16, 24, 0.9);
    border-radius: 12px;
    border: 1px solid rgba(84, 92, 112, 0.6);
    padding: 0.75rem 1rem;
    color: inherit;
    resize: vertical;
    min-height: 100px;
  }

  textarea::placeholder {
    color: #5d6780;
  }

  button {
    font: inherit;
    border: none;
    border-radius: 999px;
    padding: 0.65rem 1.5rem;
    cursor: pointer;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
  }

  button:disabled {
    cursor: not-allowed;
    opacity: 0.5;
    transform: none;
    box-shadow: none;
  }

  .primary {
    background: linear-gradient(135deg, #3d8bfd, #6f57ff);
    color: white;
    box-shadow: 0 12px 24px rgba(63, 140, 253, 0.25);
  }

  .primary:not(:disabled):hover {
    transform: translateY(-2px);
  }

  .secondary {
    background: rgba(24, 27, 38, 0.9);
    color: #d7deeb;
    border: 1px solid rgba(103, 116, 145, 0.4);
  }

  .card-group {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .card-group header h2 {
    margin: 0;
    font-size: 1.2rem;
  }

  .card-group header p {
    margin: 0.25rem 0 0;
    color: #8f9bb3;
  }

  .grid {
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }

  .grid--projects {
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  }

  .grid--gpts {
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  }

  .card {
    background: rgba(17, 19, 27, 0.95);
    border-radius: 16px;
    border: 1px solid rgba(84, 92, 112, 0.5);
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .card:hover {
    transform: translateY(-4px);
    border-color: rgba(120, 131, 164, 0.9);
  }

  .card__icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: rgba(61, 139, 253, 0.2);
    display: grid;
    place-items: center;
    font-size: 1.35rem;
  }

  .card__icon--gpt {
    background: rgba(157, 115, 255, 0.2);
  }

  .card__body h3 {
    margin: 0;
    font-size: 1.05rem;
  }

  .card__body p {
    margin: 0;
    color: #9ba7c1;
  }

  .card__body ul {
    list-style: none;
    padding: 0;
    margin: 0.75rem 0 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .secondary--ghost {
    align-self: flex-start;
    padding-inline: 1rem;
  }

  .card__body li button {
    width: 100%;
    text-align: left;
    background: rgba(26, 29, 40, 0.9);
    color: #c9d2e7;
    border-radius: 10px;
    padding: 0.5rem 0.75rem;
    border: 1px solid transparent;
  }

  .card__body li button:hover {
    border-color: rgba(99, 133, 255, 0.5);
  }

  .card--project {
    gap: 0.5rem;
  }

  .card__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
  }

  .status {
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: rgba(82, 91, 120, 0.3);
    color: #dfe6ff;
  }

  .status--active {
    background: rgba(66, 180, 104, 0.25);
    color: #a7f3c2;
  }

  .status--in-review {
    background: rgba(63, 140, 253, 0.25);
    color: #c7daff;
  }

  .status--scheduled {
    background: rgba(252, 211, 77, 0.25);
    color: #fcd34d;
  }

  .pill-group {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .pill {
    background: rgba(59, 64, 85, 0.7);
    color: #d0d7eb;
    border-radius: 999px;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
  }

  .pill--outline {
    background: transparent;
    border: 1px solid rgba(126, 140, 173, 0.6);
  }

  .pill--tiny {
    padding: 0.2rem 0.55rem;
    font-size: 0.7rem;
    background: rgba(46, 52, 72, 0.8);
  }

  .muted {
    color: #7d8bad;
    font-size: 0.8rem;
  }

  @media (max-width: 960px) {
    .page__grid {
      grid-template-columns: 1fr;
    }

    .panel--sidebar {
      position: static;
      order: 2;
    }

    .panel--main {
      order: 1;
    }
  }
</style>
