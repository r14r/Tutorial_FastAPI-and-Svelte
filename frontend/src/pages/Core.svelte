<script>
  import { derived, writable } from "svelte/store";

  let count = 1;
  let name = "Svelte enthusiast";
  let slider = 35;
  const tips = writable([
    "Props update automatically",
    "Stores make state global",
    "Bindings keep DOM and state in sync"
  ]);

  const tipCount = derived(tips, ($tips) => $tips.length);
  let newTip = "";

  $: double = count * 2;
  $: triple = count * 3;
  $: excitement = Math.round((slider / 100) * 10);
  $: greeting = name.trim() ? `Hello, ${name.trim()}!` : "Say hi with your name";

  function increment(step = 1) {
    count += step;
  }

  function decrement(step = 1) {
    count = Math.max(0, count - step);
  }

  function addTip() {
    const trimmed = newTip.trim();
    if (!trimmed) return;
    tips.update((current) => [...current, trimmed]);
    newTip = "";
  }

  function removeTip(index) {
    tips.update((current) => current.filter((_, i) => i !== index));
  }
</script>

<div class="features-grid">
  <section class="card">
    <header>
      <h2>Reactive calculations</h2>
      <p>Update a single value and watch dependent declarations update instantly.</p>
    </header>
    <div class="counter">
      <div class="value">{count}</div>
      <div class="actions">
        <button type="button" on:click={() => decrement(1)}>-1</button>
        <button type="button" on:click={() => increment(1)}>+1</button>
        <button type="button" on:click={() => increment(5)}>+5</button>
      </div>
      <dl>
        <div>
          <dt>Double</dt>
          <dd>{double}</dd>
        </div>
        <div>
          <dt>Triple</dt>
          <dd>{triple}</dd>
        </div>
      </dl>
    </div>
  </section>

  <section class="card">
    <header>
      <h2>Two-way bindings</h2>
      <p>Form controls stay in sync with component state through <code>bind:value</code>.</p>
    </header>
    <label class="field">
      Your name
      <input type="text" bind:value={name} placeholder="Add your name" />
    </label>
    <p class="greeting">{greeting}</p>

    <label class="field">
      Excitement level: {slider}%
      <input type="range" min="0" max="100" bind:value={slider} />
    </label>
    <p class="gauge">🔥 intensity: {"🔥".repeat(Math.max(1, excitement))}</p>
  </section>

  <section class="card">
    <header>
      <h2>Store-driven lists</h2>
      <p>Shared state lives in a writable store and is derived in real time.</p>
    </header>
    <label class="field add-tip">
      Add a tip
      <div class="input-row">
        <input type="text" bind:value={newTip} placeholder="Svelte is..." />
        <button type="button" on:click={addTip}>Add</button>
      </div>
    </label>
    <p class="hint">{#if $tipCount === 0}No tips yet — share one!{:else}{$tipCount} tips collected{/if}</p>

    <ul class="tips">
      {#each $tips as tip, index}
        <li>
          <span>{tip}</span>
          <button type="button" class="remove" on:click={() => removeTip(index)}>Remove</button>
        </li>
      {/each}
    </ul>
  </section>
</div>

<style>
  .features-grid {
    display: grid;
    gap: 1.5rem;
  }

  @media (min-width: 960px) {
    .features-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
  }

  .card {
    background: white;
    padding: clamp(1.5rem, 2.5vw, 2rem);
    border-radius: 1.25rem;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
    display: grid;
    gap: 1.25rem;
  }

  header h2 {
    margin: 0 0 0.35rem;
  }

  header p {
    margin: 0;
    color: #4a5568;
    font-size: 0.95rem;
  }

  .counter {
    display: grid;
    gap: 1rem;
    justify-items: start;
  }

  .value {
    font-size: clamp(2.5rem, 4vw, 3rem);
    font-weight: 700;
  }

  .actions {
    display: flex;
    gap: 0.75rem;
  }

  button {
    border: none;
    border-radius: 999px;
    padding: 0.55rem 1.3rem;
    font-weight: 600;
    background: linear-gradient(135deg, #4299e1, #667eea);
    color: white;
    transition: filter 0.2s ease;
  }

  button:hover {
    filter: brightness(1.05);
  }

  dl {
    display: grid;
    gap: 0.5rem;
    margin: 0;
  }

  dt {
    font-weight: 600;
    color: #4a5568;
  }

  dd {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 700;
  }

  .field {
    display: grid;
    gap: 0.45rem;
    font-weight: 600;
  }

  input[type="text"],
  input[type="range"] {
    border: 1px solid #cbd5e0;
    border-radius: 0.85rem;
    padding: 0.6rem 0.85rem;
    font-size: 1rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  input[type="text"]:focus,
  input[type="range"]:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.25);
  }

  input[type="range"] {
    padding: 0;
  }

  .greeting {
    margin: 0;
    font-weight: 600;
  }

  .gauge {
    margin: 0;
    color: #d97706;
    font-weight: 700;
  }

  .add-tip .input-row {
    display: flex;
    gap: 0.75rem;
  }

  .add-tip input[type="text"] {
    flex: 1;
  }

  .hint {
    margin: 0;
    color: #4a5568;
  }

  .tips {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 0.75rem;
  }

  .tips li {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: center;
    border: 1px solid #e2e8f0;
    border-radius: 0.9rem;
    padding: 0.75rem 1rem;
  }

  .tips span {
    font-weight: 600;
  }

  .remove {
    background: #f56565;
  }

  @media (max-width: 720px) {
    .features-grid {
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }
  }
</style>
