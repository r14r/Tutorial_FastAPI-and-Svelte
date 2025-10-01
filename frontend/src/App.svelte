<script>
  import { onMount } from "svelte";
  import {
    registerUser,
    loginUser,
    getItems,
    getProfile,
    createItem,
    updateItem,
    deleteItem
  } from "./lib/api";
  import { token, currentUser } from "./stores/auth";
  import { get } from "svelte/store";

  let registerForm = { email: "", password: "" };
  let loginForm = { email: "", password: "" };
  let itemForm = { id: null, title: "", description: "" };
  let items = [];
  let total = 0;
  let loading = false;
  let errorMessage = "";
  let successMessage = "";

  async function handleRegister(event) {
    event.preventDefault();
    loading = true;
    errorMessage = "";
    successMessage = "";
    try {
      await registerUser(registerForm);
      successMessage = "Registration successful! Please sign in.";
      registerForm = { email: "", password: "" };
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Registration failed";
    } finally {
      loading = false;
    }
  }

  async function handleLogin(event) {
    event.preventDefault();
    loading = true;
    errorMessage = "";
    successMessage = "";
    try {
      const { access_token } = await loginUser(loginForm);
      token.set(access_token);
      await loadProfile();
      await loadItems();
      loginForm = { email: "", password: "" };
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Login failed";
    } finally {
      loading = false;
    }
  }

  async function loadProfile() {
    try {
      const profile = await getProfile();
      currentUser.set(profile);
    } catch (error) {
      token.set(null);
      currentUser.set(null);
    }
  }

  async function loadItems() {
    if (!get(token)) {
      items = [];
      total = 0;
      return;
    }
    loading = true;
    try {
      const response = await getItems();
      items = response.items;
      total = response.total;
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Could not load items";
    } finally {
      loading = false;
    }
  }

  async function handleItemSubmit(event) {
    event.preventDefault();
    loading = true;
    errorMessage = "";
    successMessage = "";
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
      itemForm = { id: null, title: "", description: "" };
      await loadItems();
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Could not save item";
    } finally {
      loading = false;
    }
  }

  function startEdit(item) {
    itemForm = { id: item.id, title: item.title, description: item.description ?? "" };
  }

  async function handleDelete(id) {
    loading = true;
    try {
      await deleteItem(id);
      await loadItems();
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Could not delete item";
    } finally {
      loading = false;
    }
  }

  function handleLogout() {
    token.set(null);
    currentUser.set(null);
    items = [];
    total = 0;
  }

  onMount(async () => {
    if (get(token)) {
      await loadProfile();
      await loadItems();
    }
  });
</script>

<main class="layout">
  <section class="hero">
    <h1>FastAPI + Svelte productivity board</h1>
    <p>
      This demo showcases authentication, database-backed CRUD operations, and reactive UI powered by
      FastAPI and Svelte.
    </p>
  </section>

  {#if errorMessage}
    <div class="alert error">{errorMessage}</div>
  {/if}
  {#if successMessage}
    <div class="alert success">{successMessage}</div>
  {/if}

  <section class="auth-grid">
    <div class="card">
      <h2>Register</h2>
      <form on:submit|preventDefault={handleRegister}>
        <label>
          Email
          <input type="email" bind:value={registerForm.email} required />
        </label>
        <label>
          Password
          <input type="password" bind:value={registerForm.password} minlength="6" required />
        </label>
        <button type="submit" disabled={loading}>Create account</button>
      </form>
    </div>

    <div class="card">
      <h2>Sign in</h2>
      <form on:submit|preventDefault={handleLogin}>
        <label>
          Email
          <input type="email" bind:value={loginForm.email} required />
        </label>
        <label>
          Password
          <input type="password" bind:value={loginForm.password} required />
        </label>
        <button type="submit" disabled={loading}>Sign in</button>
      </form>
    </div>
  </section>

  {#if $currentUser}
    <section class="card user-card">
      <div class="user-details">
        <h2>Welcome back, {$currentUser.email}</h2>
        <p>You're authenticated. Create, update or delete notes that are persisted in SQLite.</p>
      </div>
      <button class="logout" on:click={handleLogout}>Log out</button>
    </section>

    <section class="card">
      <h2>{itemForm.id ? "Update" : "Create"} item</h2>
      <form on:submit|preventDefault={handleItemSubmit}>
        <label>
          Title
          <input type="text" bind:value={itemForm.title} required />
        </label>
        <label>
          Description
          <textarea rows="3" bind:value={itemForm.description} placeholder="What are you working on?"></textarea>
        </label>
        <div class="actions">
          <button type="submit" disabled={loading}>
            {itemForm.id ? "Save changes" : "Add item"}
          </button>
          {#if itemForm.id}
            <button type="button" class="secondary" on:click={() => (itemForm = { id: null, title: "", description: "" })}>
              Cancel
            </button>
          {/if}
        </div>
      </form>
    </section>

    <section class="card">
      <div class="items-header">
        <h2>Your items ({total})</h2>
        <button class="secondary" on:click={loadItems} disabled={loading}>Refresh</button>
      </div>
      {#if items.length === 0}
        <p class="empty">No items yet. Create your first one!</p>
      {:else}
        <ul class="items">
          {#each items as item}
            <li>
              <div>
                <h3>{item.title}</h3>
                {#if item.description}
                  <p>{item.description}</p>
                {/if}
              </div>
              <div class="item-actions">
                <button class="secondary" on:click={() => startEdit(item)}>Edit</button>
                <button class="danger" on:click={() => handleDelete(item.id)}>Delete</button>
              </div>
            </li>
          {/each}
        </ul>
      {/if}
    </section>
  {/if}
</main>

<style>
  .layout {
    max-width: 960px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .hero {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  }

  .hero h1 {
    margin-top: 0;
    margin-bottom: 0.75rem;
  }

  .auth-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
  }

  .card {
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .actions {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    align-items: center;
  }

  label {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    font-weight: 600;
  }

  input,
  textarea {
    border: 1px solid #cbd5e0;
    border-radius: 0.75rem;
    padding: 0.65rem 0.85rem;
    font-size: 0.95rem;
    transition: border-color 0.2s ease;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: #4299e1;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.3);
  }

  button {
    border: none;
    border-radius: 999px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    background: linear-gradient(135deg, #4299e1, #667eea);
    color: white;
    transition: filter 0.2s ease;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  button:not(:disabled):hover {
    filter: brightness(1.05);
  }

  .secondary {
    background: #edf2f7;
    color: #2d3748;
  }

  .danger {
    background: #f56565;
  }

  .items {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .items li {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    border: 1px solid #e2e8f0;
    border-radius: 1rem;
    padding: 1rem;
  }

  .items li h3 {
    margin: 0 0 0.35rem;
  }

  .item-actions {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .alert {
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
    font-weight: 600;
  }

  .alert.error {
    background: #fed7d7;
    color: #742a2a;
  }

  .alert.success {
    background: #c6f6d5;
    color: #22543d;
  }

  .user-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }

  .logout {
    background: #f56565;
  }

  .items-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .empty {
    color: #718096;
    margin: 0;
  }

  @media (max-width: 640px) {
    .items li {
      flex-direction: column;
      align-items: stretch;
    }

    .item-actions {
      justify-content: flex-end;
    }
  }
</style>
