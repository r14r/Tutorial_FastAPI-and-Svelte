<script>
  import { onDestroy } from "svelte";
  import { get } from "svelte/store";
  import { getItems } from "$lib/api";
  import { token } from "$stores/auth";

  let query = { skip: 0, limit: 5 };
  let autoRun = true;
  let loading = false;
  let items = [];
  let total = 0;
  let errorMessage = "";
  let debounceId;

  const MAX_LIMIT = 50;
  let sanitizedParams = sanitizeQuery();

  function sanitizeQuery() {
    return {
      skip: Math.max(0, Math.trunc(Number(query.skip) || 0)),
      limit: Math.min(MAX_LIMIT, Math.max(1, Math.trunc(Number(query.limit) || 1)))
    };
  }

  async function runQuery(params = sanitizedParams) {
    if (!get(token)) {
      items = [];
      total = 0;
      return;
    }
    loading = true;
    errorMessage = "";
    try {
      const response = await getItems(params);
      items = response.items;
      total = response.total;
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Could not execute query";
    } finally {
      loading = false;
    }
  }

  const unsubscribe = token.subscribe((value) => {
    if (!value) {
      items = [];
      total = 0;
    } else {
      runQuery();
    }
  });

  onDestroy(() => {
    unsubscribe();
    if (debounceId) {
      clearTimeout(debounceId);
    }
  });

  $: sanitizedParams = sanitizeQuery();
  $: if (autoRun && $token) {
    const params = sanitizedParams;
    clearTimeout(debounceId);
    debounceId = setTimeout(() => {
      runQuery(params);
    }, 300);
  }

  $: resultsAvailable = items.length > 0;
  $: totalTitleChars = items.reduce((acc, item) => acc + item.title.length, 0);
  $: averageTitleLength = resultsAvailable ? (totalTitleChars / items.length).toFixed(1) : "0";
  $: itemsWithDescription = items.filter((item) => (item.description ?? "").trim().length > 0).length;
  $: descriptionCoverage = resultsAvailable ? Math.round((itemsWithDescription / items.length) * 100) : 0;
  $: previewTitles = items.slice(0, 3).map((item) => item.title);
</script>

{#if !$token}
  <div class="card empty-state">
    <h2>Authentication required</h2>
    <p>Sign in to run database-backed queries against the FastAPI items endpoint.</p>
  </div>
{:else}
  <div class="query-grid">
    <section class="card controls">
      <header>
        <h2>Query builder</h2>
        <p>Adjust pagination parameters and optionally auto-run the request.</p>
      </header>
      <div class="control-row">
        <label>
          Skip
          <input type="number" min="0" bind:value={query.skip} />
        </label>
        <label>
          Limit
          <input type="number" min="1" max={MAX_LIMIT} bind:value={query.limit} />
        </label>
      </div>
      <label class="toggle">
        <input type="checkbox" bind:checked={autoRun} />
        <span>Automatically run when parameters change</span>
      </label>
      <button type="button" on:click={runQuery} disabled={loading}>
        {loading ? "Running query…" : "Run query"}
      </button>
      <p class="hint">Limit is capped at {MAX_LIMIT} items per request.</p>
    </section>

    <section class="card insights">
      <header>
        <h2>Derived insights</h2>
        <p>These metrics are computed client-side from the query response.</p>
      </header>
      <dl>
        <div>
          <dt>Total items in database</dt>
          <dd>{total}</dd>
        </div>
        <div>
          <dt>Items returned in this page</dt>
          <dd>{items.length}</dd>
        </div>
        <div>
          <dt>Average title length</dt>
          <dd>{averageTitleLength} characters</dd>
        </div>
        <div>
          <dt>Items with descriptions</dt>
          <dd>{itemsWithDescription} ({descriptionCoverage}%)</dd>
        </div>
        <div>
          <dt>Preview titles</dt>
          <dd>{#if resultsAvailable}{previewTitles.join(", ")}{:else}–{/if}</dd>
        </div>
      </dl>
    </section>
  </div>

  <section class="card results">
    <header>
      <h2>Raw results</h2>
      <p>{loading ? "Fetching data…" : resultsAvailable ? "Latest response payload" : "No data returned"}</p>
    </header>

    {#if errorMessage}
      <div class="feedback error">{errorMessage}</div>
    {/if}

    {#if resultsAvailable}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {#each items as item}
            <tr>
              <td>{item.id}</td>
              <td>{item.title}</td>
              <td>{item.description ?? "—"}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {:else if !loading}
      <p class="empty">No rows to display with the current pagination settings.</p>
    {/if}
  </section>
{/if}

<style>
  .card {
    background: white;
    padding: clamp(1.5rem, 2.5vw, 2rem);
    border-radius: 1.25rem;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  }

  .empty-state {
    text-align: center;
    display: grid;
    gap: 0.75rem;
  }

  .query-grid {
    display: grid;
    gap: 1.5rem;
  }

  @media (min-width: 960px) {
    .query-grid {
      grid-template-columns: 340px 1fr;
      align-items: start;
    }
  }

  header {
    display: grid;
    gap: 0.25rem;
    margin-bottom: 1.1rem;
  }

  header h2 {
    margin: 0;
  }

  header p {
    margin: 0;
    color: #4a5568;
  }

  .control-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
  }

  label {
    display: grid;
    gap: 0.45rem;
    font-weight: 600;
  }

  input[type="number"] {
    border: 1px solid #cbd5e0;
    border-radius: 0.85rem;
    padding: 0.65rem 0.85rem;
    font-size: 1rem;
  }

  input[type="number"]:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
  }

  .toggle {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 1rem;
  }

  button {
    border: none;
    border-radius: 999px;
    padding: 0.65rem 1.5rem;
    font-weight: 600;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: white;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .hint {
    margin: 0.75rem 0 0;
    color: #475569;
    font-size: 0.9rem;
  }

  dl {
    display: grid;
    gap: 0.85rem;
    margin: 0;
  }

  dt {
    font-weight: 600;
    color: #4a5568;
  }

  dd {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }

  th,
  td {
    text-align: left;
    padding: 0.65rem 0.75rem;
  }

  thead {
    background: rgba(99, 102, 241, 0.12);
  }

  tbody tr:nth-child(even) {
    background: rgba(148, 163, 184, 0.12);
  }

  .feedback {
    margin-bottom: 1rem;
    padding: 0.85rem 1rem;
    border-radius: 1rem;
    font-weight: 600;
    box-shadow: 0 18px 36px rgba(15, 23, 42, 0.12);
  }

  .feedback.error {
    background: #fee2e2;
    color: #991b1b;
  }

  .empty {
    margin: 0;
    color: #4a5568;
  }
</style>
