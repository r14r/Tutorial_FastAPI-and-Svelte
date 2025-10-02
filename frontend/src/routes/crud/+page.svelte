<script>
  import { onDestroy } from "svelte";
  import { get } from "svelte/store";
  import { createItem, deleteItem, getItems, updateItem } from "$lib/api";
  import { token, currentUser } from "$stores/auth";

  let items = [];
  let total = 0;
  let listLoading = false;
  let formLoading = false;
  let errorMessage = "";
  let successMessage = "";
  let itemForm = { id: null, title: "", description: "" };

  function resetFeedback() {
    errorMessage = "";
    successMessage = "";
  }

  async function loadItems() {
    if (!get(token)) {
      items = [];
      total = 0;
      return;
    }
    listLoading = true;
    resetFeedback();
    try {
      const response = await getItems();
      items = response.items;
      total = response.total;
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Could not load items";
    } finally {
      listLoading = false;
    }
  }

  function startCreate() {
    itemForm = { id: null, title: "", description: "" };
  }

  function startEdit(item) {
    itemForm = {
      id: item.id,
      title: item.title,
      description: item.description ?? ""
    };
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!itemForm.title.trim()) {
      return;
    }
    formLoading = true;
    resetFeedback();
    try {
      if (itemForm.id) {
        await updateItem(itemForm.id, {
          title: itemForm.title,
          description: itemForm.description
        });
        successMessage = "Item updated";
      } else {
        await createItem({
          title: itemForm.title,
          description: itemForm.description
        });
        successMessage = "Item created";
      }
      startCreate();
      await loadItems();
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Could not save item";
    } finally {
      formLoading = false;
    }
  }

  async function handleDelete(id) {
    formLoading = true;
    resetFeedback();
    try {
      await deleteItem(id);
      successMessage = "Item deleted";
      if (itemForm.id === id) {
        startCreate();
      }
      await loadItems();
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Could not delete item";
    } finally {
      formLoading = false;
    }
  }

  const unsubscribe = token.subscribe((value) => {
    if (!value) {
      items = [];
      total = 0;
      startCreate();
    } else {
      loadItems();
    }
  });

  onDestroy(unsubscribe);

  $: isEditing = Boolean(itemForm.id);
</script>

{#if !$currentUser}
  <div class="card empty-state">
    <h2>Sign in to manage items</h2>
    <p>Once authenticated you can create, edit, and delete notes persisted in SQLite.</p>
  </div>
{:else}
  <div class="crud-layout">
    <section class="card form-card">
      <header>
        <div>
          <h2>{isEditing ? "Update item" : "Create item"}</h2>
          <p>Fields are fully two-way bound to component state.</p>
        </div>
        {#if isEditing}
          <button type="button" class="secondary" on:click={startCreate} disabled={formLoading}>
            Cancel edit
          </button>
        {/if}
      </header>

      <form on:submit={handleSubmit}>
        <label>
          Title
          <input type="text" bind:value={itemForm.title} placeholder="What are you working on?" required />
        </label>
        <label>
          Description
          <textarea rows="4" bind:value={itemForm.description} placeholder="Add a few more details"></textarea>
        </label>
        <div class="actions">
          <button type="submit" disabled={formLoading}>{isEditing ? "Save changes" : "Add item"}</button>
          <button type="button" class="secondary" on:click={loadItems} disabled={formLoading || listLoading}>
            Refresh
          </button>
        </div>
      </form>
    </section>

    <section class="card list-card">
      <header>
        <div>
          <h2>Your items</h2>
          <p>{listLoading ? "Fetching items…" : `${total} total records`}</p>
        </div>
        <button type="button" class="secondary" on:click={loadItems} disabled={listLoading}>
          Reload
        </button>
      </header>

      {#if items.length === 0}
        <p class="empty">No items yet. Create your first one!</p>
      {:else}
        <ul>
          {#each items as item}
            <li>
              <div class="item-copy">
                <h3>{item.title}</h3>
                {#if item.description}
                  <p>{item.description}</p>
                {/if}
              </div>
              <div class="item-actions">
                <button type="button" class="secondary" on:click={() => startEdit(item)} disabled={formLoading}>
                  Edit
                </button>
                <button type="button" class="danger" on:click={() => handleDelete(item.id)} disabled={formLoading}>
                  Delete
                </button>
              </div>
            </li>
          {/each}
        </ul>
      {/if}
    </section>
  </div>
{/if}

{#if errorMessage}
  <div class="feedback error">{errorMessage}</div>
{/if}
{#if successMessage}
  <div class="feedback success">{successMessage}</div>
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

  .crud-layout {
    display: grid;
    gap: 1.5rem;
  }

  @media (min-width: 960px) {
    .crud-layout {
      grid-template-columns: 360px 1fr;
      align-items: start;
    }
  }

  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.25rem;
  }

  header h2 {
    margin: 0;
  }

  header p {
    margin: 0.35rem 0 0;
    color: #4a5568;
  }

  form {
    display: grid;
    gap: 1rem;
  }

  label {
    display: grid;
    gap: 0.45rem;
    font-weight: 600;
  }

  input,
  textarea {
    border: 1px solid #cbd5e0;
    border-radius: 0.85rem;
    padding: 0.75rem 0.9rem;
    font-size: 1rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
  }

  textarea {
    resize: vertical;
  }

  .actions {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }

  button {
    border: none;
    border-radius: 999px;
    padding: 0.65rem 1.4rem;
    font-weight: 600;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: white;
  }

  button.secondary {
    background: rgba(79, 70, 229, 0.12);
    color: #3730a3;
  }

  button.danger {
    background: linear-gradient(135deg, #f97316, #ef4444);
    color: white;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 1rem;
  }

  li {
    display: grid;
    gap: 0.75rem;
    padding: 1rem;
    border-radius: 1rem;
    background: rgba(99, 102, 241, 0.06);
  }

  .item-copy h3 {
    margin: 0 0 0.35rem;
  }

  .item-copy p {
    margin: 0;
    color: #4a5568;
  }

  .item-actions {
    display: flex;
    gap: 0.75rem;
  }

  .feedback {
    margin-top: 1.5rem;
    padding: 0.85rem 1rem;
    border-radius: 1rem;
    font-weight: 600;
    box-shadow: 0 18px 36px rgba(15, 23, 42, 0.12);
  }

  .feedback.error {
    background: #fee2e2;
    color: #991b1b;
  }

  .feedback.success {
    background: #c6f6d5;
    color: #22543d;
  }
</style>
