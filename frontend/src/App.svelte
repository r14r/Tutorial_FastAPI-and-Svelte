<script>
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import AuthPage from "./pages/AuthPage.svelte";
  import CrudPage from "./pages/CrudPage.svelte";
  import DatabaseQueryPage from "./pages/DatabaseQueryPage.svelte";
  import CoreFeaturesPage from "./pages/CoreFeaturesPage.svelte";
  import { getProfile } from "./lib/api";
  import { token, currentUser } from "./stores/auth";

  const pages = [
    {
      id: "auth",
      title: "Authentication",
      description: "Create an account or sign in to obtain a bearer token from FastAPI.",
      component: AuthPage,
      requiresAuth: false
    },
    {
      id: "crud",
      title: "CRUD dashboard",
      description: "Manage notes that are stored in SQLite via FastAPI endpoints.",
      component: CrudPage,
      requiresAuth: true
    },
    {
      id: "database",
      title: "Database queries",
      description: "Explore pagination and derived metrics using the items API.",
      component: DatabaseQueryPage,
      requiresAuth: true
    },
    {
      id: "core",
      title: "Core Svelte features",
      description: "Play with reactivity, bindings, and stores in an isolated playground.",
      component: CoreFeaturesPage,
      requiresAuth: false
    }
  ];

  const pageMap = new Map(pages.map((page) => [page.id, page]));

  let activePage = pages[0].id;
  let activeDefinition = pages[0];
  let profileError = "";
  let loadingProfile = false;

  async function loadProfile() {
    if (!get(token)) {
      currentUser.set(null);
      return;
    }
    loadingProfile = true;
    profileError = "";
    try {
      const profile = await getProfile();
      currentUser.set(profile);
    } catch (error) {
      profileError = error.response?.data?.detail ?? "Could not load profile";
      token.set(null);
      currentUser.set(null);
    } finally {
      loadingProfile = false;
    }
  }

  onMount(async () => {
    if (get(token)) {
      await loadProfile();
      activePage = "crud";
    }
  });

  function handleLogout() {
    token.set(null);
    currentUser.set(null);
    activePage = "auth";
  }

  async function handleLoginSuccess() {
    await loadProfile();
    activePage = "crud";
  }

  $: {
    const definition = pageMap.get(activePage) ?? pages[0];
    if (!$token && definition.requiresAuth) {
      activePage = "auth";
      activeDefinition = pageMap.get("auth") ?? pages[0];
    } else {
      activeDefinition = definition;
    }
  }
</script>

<div class="app-shell">
  <header class="app-header">
    <div class="brand">
      <span class="brand-accent">FastAPI</span>
      <span>+</span>
      <span class="brand-accent">Svelte</span>
      <span>tutorial</span>
    </div>

    <nav class="main-nav">
      {#each pages as page}
        <button
          type="button"
          class:active={page.id === activePage}
          disabled={page.requiresAuth && !$token}
          on:click={() => (activePage = page.id)}
        >
          {page.title}
        </button>
      {/each}
    </nav>

    {#if $currentUser}
      <div class="user-chip">
        <span>{$currentUser.email}</span>
        <button type="button" class="logout" on:click={handleLogout}>Log out</button>
      </div>
    {/if}
  </header>

  <main class="content">
    <section class="intro">
      <h1>{activeDefinition.title}</h1>
      <p>{activeDefinition.description}</p>
    </section>

    {#if profileError}
      <div class="alert error">{profileError}</div>
    {/if}
    {#if loadingProfile}
      <div class="alert info">Loading profile…</div>
    {/if}

    <section class="page-container">
      <svelte:component
        this={activeDefinition.component}
        on:loginSuccess={handleLoginSuccess}
        on:requestProfileRefresh={loadProfile}
      />
    </section>
  </main>
</div>

<style>
  .app-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .app-header {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1.5rem clamp(1rem, 5vw, 3rem);
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-weight: 700;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }

  .brand-accent {
    color: #4c51bf;
  }

  .main-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .main-nav button {
    border: none;
    border-radius: 999px;
    padding: 0.45rem 1.1rem;
    background: rgba(66, 153, 225, 0.12);
    color: #2b2d42;
    font-weight: 600;
    transition: all 0.2s ease;
  }

  .main-nav button.active {
    background: linear-gradient(135deg, #4299e1, #667eea);
    color: white;
    box-shadow: 0 10px 20px rgba(76, 81, 191, 0.2);
  }

  .main-nav button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .user-chip {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: white;
    padding: 0.65rem 1rem;
    border-radius: 999px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  }

  .user-chip span {
    font-weight: 600;
  }

  .logout {
    background: #f56565;
    color: white;
    border: none;
    border-radius: 999px;
    padding: 0.35rem 0.9rem;
    font-weight: 600;
  }

  .content {
    flex: 1;
    max-width: 1100px;
    width: min(100%, 1100px);
    margin: 0 auto;
    padding: 0 1.5rem 3rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .intro {
    background: white;
    padding: clamp(1.5rem, 3vw, 2.5rem);
    border-radius: 1.25rem;
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08);
  }

  .intro h1 {
    margin: 0 0 0.5rem;
    font-size: clamp(1.5rem, 3vw, 2rem);
  }

  .intro p {
    margin: 0;
    color: #4a5568;
  }

  .alert {
    padding: 0.75rem 1rem;
    border-radius: 0.85rem;
    font-weight: 600;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  }

  .alert.error {
    background: #fed7d7;
    color: #742a2a;
  }

  .alert.info {
    background: #ebf8ff;
    color: #1a365d;
  }

  .page-container {
    background: transparent;
    display: grid;
  }

  @media (max-width: 640px) {
    .app-header {
      justify-content: center;
    }

    .user-chip {
      width: 100%;
      justify-content: space-between;
    }
  }
</style>
