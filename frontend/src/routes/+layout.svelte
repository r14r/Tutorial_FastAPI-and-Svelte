<script>
  import "../app.css";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { browser } from "$app/environment";
  import { getProfile } from "$lib/api";
  import { currentUser, token } from "$stores/auth";

  const sections = [
    {
      id: "overview",
      title: "Welcome to the FastAPI + SvelteKit tutorial",
      description:
        "Learn how the FastAPI backend and the SvelteKit front-end work together while exploring the demo application.",
      href: "/",
      icon: "🏠",
      requiresAuth: false
    },
    {
      id: "auth",
      title: "Authentication",
      description:
        "Create an account, sign in, and inspect how bearer tokens flow between the client and FastAPI.",
      href: "/auth",
      icon: "🔐",
      requiresAuth: false
    },
    {
      id: "crud",
      title: "CRUD dashboard",
      description:
        "Manage notes that are stored in SQLite through FastAPI endpoints and watch optimistic UI updates in action.",
      href: "/crud",
      icon: "📋",
      requiresAuth: true
    },
    {
      id: "database",
      title: "Database queries",
      description:
        "Experiment with pagination parameters and see how derived analytics are computed from API responses.",
      href: "/database",
      icon: "📊",
      requiresAuth: true
    },
    {
      id: "core",
      title: "Core Svelte features",
      description:
        "Play with reactivity, bindings, and stores in an isolated playground that mirrors the workshop exercises.",
      href: "/core",
      icon: "✨",
      requiresAuth: false
    }
  ];

  const sectionMap = new Map(sections.map((section) => [section.href, section]));

  const topMenus = [
    {
      id: "sections",
      label: "Tutorial sections",
      items: sections.map(({ href, title, description, requiresAuth }) => ({
        href,
        label: title,
        description,
        requiresAuth
      }))
    },
    {
      id: "resources",
      label: "Resources",
      items: [
        {
          href: "https://github.com/testdrivenio/FastAPI-and-Svelte",
          label: "Project repository",
          description: "View the source code and workshop instructions on GitHub.",
          external: true
        },
        {
          href: "https://fastapi.tiangolo.com/",
          label: "FastAPI documentation",
          description: "Deep dive into FastAPI features and best practices.",
          external: true
        },
        {
          href: "https://kit.svelte.dev/docs",
          label: "SvelteKit documentation",
          description: "Learn more about routing, data loading, and adapters in SvelteKit.",
          external: true
        }
      ]
    }
  ];

  let openMenu = null;
  let sidebarOpen = false;
  let loadingProfile = false;
  let profileError = "";
  let profileLoaded = false;
  let lastPath = null;

  function normalizePath(pathname) {
    if (!pathname) return "/";
    if (pathname !== "/" && pathname.endsWith("/")) {
      return pathname.slice(0, -1);
    }
    return pathname;
  }

  $: currentPath = normalizePath($page.url.pathname);
  $: activeDefinition = sectionMap.get(currentPath) ?? sectionMap.get("/");

  function requiresAuth(pathname) {
    return sectionMap.get(pathname)?.requiresAuth ?? false;
  }

  async function loadProfile(force = false) {
    if (!browser || !$token) {
      return;
    }
    if (loadingProfile || (profileLoaded && !force)) {
      return;
    }
    loadingProfile = true;
    profileError = "";
    try {
      const profile = await getProfile();
      currentUser.set(profile);
      profileLoaded = true;
    } catch (error) {
      profileLoaded = false;
      profileError = error.response?.data?.detail ?? "Could not load profile";
      token.set(null);
      currentUser.set(null);
    } finally {
      loadingProfile = false;
    }
  }

  function toggleMenu(id) {
    openMenu = openMenu === id ? null : id;
  }

  function closeMenu() {
    openMenu = null;
  }

  function toggleSidebar() {
    sidebarOpen = !sidebarOpen;
  }

  function handleNavigation(href, event) {
    if (event) {
      event.preventDefault();
    }
    closeMenu();
    sidebarOpen = false;
    goto(href);
  }

  function handleBrandKeydown(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      goto("/");
    }
  }

  function handleLogout() {
    token.set(null);
    currentUser.set(null);
    profileError = "";
    profileLoaded = false;
    sidebarOpen = false;
    goto("/auth");
  }

  $: if (browser && !$token && requiresAuth(currentPath)) {
    goto("/auth");
  }

  $: if (!$token) {
    profileLoaded = false;
  }

  $: if (currentPath !== lastPath) {
    if (lastPath !== null) {
      closeMenu();
      sidebarOpen = false;
    }
    lastPath = currentPath;
  }

  onMount(() => {
    if (!browser) return;

    const handleDocumentClick = () => closeMenu();
    const handleKeydown = (event) => {
      if (event.key === "Escape") {
        closeMenu();
        sidebarOpen = false;
      }
    };

    document.addEventListener("click", handleDocumentClick);
    window.addEventListener("keydown", handleKeydown);

    const unsubscribeToken = token.subscribe((value) => {
      if (value) {
        profileLoaded = false;
        loadProfile();
      } else {
        profileError = "";
        profileLoaded = false;
        currentUser.set(null);
      }
    });

    return () => {
      document.removeEventListener("click", handleDocumentClick);
      window.removeEventListener("keydown", handleKeydown);
      unsubscribeToken();
    };
  });

  $: if (browser && sidebarOpen) {
    document.body.style.overflow = "hidden";
  } else if (browser) {
    document.body.style.overflow = "";
  }
</script>

<div class="app-shell">
  <header class="top-nav">
    <div class="brand" on:click={() => goto("/")} on:keydown={handleBrandKeydown} role="button" tabindex="0">
      <span class="brand-accent">FastAPI</span>
      <span>+</span>
      <span class="brand-accent">SvelteKit</span>
      <span class="muted">tutorial</span>
    </div>

    <div class="nav-actions">
      <button
        class="sidebar-toggle"
        type="button"
        on:click|stopPropagation={toggleSidebar}
        aria-expanded={sidebarOpen}
      >
        ☰
        <span class="sr-only">Toggle sidebar navigation</span>
      </button>

      <nav class="menu-bar" on:click|stopPropagation>
        {#each topMenus as menu}
          <div class="menu" class:open={openMenu === menu.id}>
            <button
              type="button"
              class="menu-trigger"
              aria-haspopup="true"
              aria-expanded={openMenu === menu.id}
              on:click={() => toggleMenu(menu.id)}
            >
              {menu.label}
            </button>
            {#if openMenu === menu.id}
              <div class="submenu" role="menu">
                {#each menu.items as item}
                  {#if item.external}
                    <a
                      class="submenu-item"
                      role="menuitem"
                      href={item.href}
                      target="_blank"
                      rel="noreferrer"
                    >
                      <span>
                        <strong>{item.label}</strong>
                        <small>{item.description}</small>
                      </span>
                      <span aria-hidden="true">↗</span>
                    </a>
                  {:else}
                    <a
                      class="submenu-item"
                      role="menuitem"
                      href={item.href}
                      on:click={(event) => handleNavigation(item.href, event)}
                      class:disabled={item.requiresAuth && !$token}
                    >
                      <span>
                        <strong>{item.label}</strong>
                        <small>{item.description}</small>
                      </span>
                      {#if item.requiresAuth}
                        <span class="badge" aria-hidden="true">Auth</span>
                      {/if}
                    </a>
                  {/if}
                {/each}
              </div>
            {/if}
          </div>
        {/each}
      </nav>

      {#if $currentUser}
        <div class="user-chip">
          <span class="avatar">{$currentUser.email[0].toUpperCase()}</span>
          <div class="user-meta">
            <strong>{$currentUser.email}</strong>
            <button type="button" class="ghost" on:click={() => loadProfile(true)} disabled={loadingProfile}>
              {loadingProfile ? "Refreshing…" : "Refresh profile"}
            </button>
          </div>
          <button type="button" class="logout" on:click={handleLogout}>Log out</button>
        </div>
      {:else}
        <a class="sign-in" href="/auth" on:click={(event) => handleNavigation("/auth", event)}>
          Sign in
        </a>
      {/if}
    </div>
  </header>

  <div class:sidebar-open={sidebarOpen} class="layout">
    <aside class="sidebar" aria-label="Section navigation">
      <div class="sidebar-header">
        <h2>Sections</h2>
        <button type="button" class="close" on:click={toggleSidebar}>
          <span aria-hidden="true">×</span>
          <span class="sr-only">Close sidebar</span>
        </button>
      </div>
      <nav>
        {#each sections as section}
          <a
            href={section.href}
            class:active={section.href === currentPath}
            class:disabled={section.requiresAuth && !$token}
            on:click={(event) => handleNavigation(section.href, event)}
          >
            <span class="icon" aria-hidden="true">{section.icon}</span>
            <div class="copy">
              <strong>{section.title}</strong>
              <small>{section.description}</small>
            </div>
            {#if section.requiresAuth}
              <span class="badge" aria-hidden="true">Auth</span>
            {/if}
          </a>
        {/each}
      </nav>
    </aside>

    <main class="content" tabindex="-1">
      {#if activeDefinition}
        <section class="intro">
          <h1>{activeDefinition.title}</h1>
          <p>{activeDefinition.description}</p>
        </section>
      {/if}

      {#if profileError && $token}
        <div class="alert error">{profileError}</div>
      {/if}
      {#if loadingProfile}
        <div class="alert info">Loading profile…</div>
      {/if}

      <slot />
    </main>
  </div>

  {#if sidebarOpen}
    <div class="backdrop" on:click={toggleSidebar} aria-hidden="true"></div>
  {/if}
</div>

<style>
  .app-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
  }

  .top-nav {
    position: sticky;
    top: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: space-between;
    padding: 1rem clamp(1rem, 4vw, 2.5rem);
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.85);
    border-bottom: 1px solid rgba(148, 163, 184, 0.3);
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    cursor: pointer;
  }

  .brand:focus {
    outline: 2px solid #4c51bf;
    outline-offset: 4px;
  }

  .brand-accent {
    color: #4c51bf;
  }

  .muted {
    font-weight: 500;
    color: #475569;
  }

  .nav-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .sidebar-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    border-radius: 999px;
    width: 2.5rem;
    height: 2.5rem;
    font-size: 1.2rem;
    background: rgba(148, 163, 184, 0.2);
    color: #1f2933;
  }

  .menu-bar {
    display: flex;
    gap: 0.75rem;
  }

  .menu {
    position: relative;
  }

  .menu-trigger {
    border: none;
    border-radius: 999px;
    padding: 0.5rem 1.1rem;
    font-weight: 600;
    background: rgba(99, 102, 241, 0.12);
    color: #3730a3;
  }

  .menu.open .menu-trigger {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    box-shadow: 0 12px 30px rgba(99, 102, 241, 0.25);
  }

  .submenu {
    position: absolute;
    top: calc(100% + 0.5rem);
    right: 0;
    display: grid;
    gap: 0.35rem;
    width: min(320px, 80vw);
    padding: 0.75rem;
    border-radius: 1rem;
    background: white;
    box-shadow: 0 25px 60px rgba(15, 23, 42, 0.18);
  }

  .submenu-item {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    text-decoration: none;
    padding: 0.75rem;
    border-radius: 0.85rem;
    color: inherit;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .submenu-item:hover,
  .submenu-item:focus-visible {
    background: rgba(99, 102, 241, 0.12);
    transform: translateX(2px);
  }

  .submenu-item small {
    display: block;
    color: #475569;
    margin-top: 0.2rem;
  }

  .submenu-item.disabled {
    opacity: 0.45;
    pointer-events: none;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    padding: 0.15rem 0.6rem;
    font-size: 0.7rem;
    background: rgba(248, 113, 113, 0.15);
    color: #b91c1c;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .user-chip {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: white;
    padding: 0.5rem 0.85rem 0.5rem 0.6rem;
    border-radius: 999px;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.18);
  }

  .avatar {
    width: 2.1rem;
    height: 2.1rem;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: white;
    display: grid;
    place-items: center;
    font-weight: 700;
  }

  .user-meta {
    display: grid;
    gap: 0.2rem;
  }

  .ghost {
    border: none;
    background: transparent;
    color: #4c51bf;
    font-weight: 600;
    padding: 0;
    text-decoration: underline;
  }

  .logout {
    border: none;
    border-radius: 999px;
    padding: 0.45rem 0.9rem;
    font-weight: 600;
    background: linear-gradient(135deg, #f97316, #ef4444);
    color: white;
  }

  .sign-in {
    text-decoration: none;
    border-radius: 999px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: white;
  }

  .layout {
    flex: 1;
    display: grid;
    grid-template-columns: 280px 1fr;
    position: relative;
  }

  .sidebar {
    position: sticky;
    top: 0;
    align-self: flex-start;
    min-height: calc(100vh - 0px);
    padding: 1.5rem 1rem;
    display: grid;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(148, 163, 184, 0.3);
    z-index: 15;
  }

  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .sidebar nav {
    display: grid;
    gap: 0.75rem;
  }

  .sidebar a {
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 0.75rem;
    align-items: center;
    padding: 0.8rem;
    border-radius: 1rem;
    text-decoration: none;
    color: inherit;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .sidebar a:hover,
  .sidebar a:focus-visible {
    background: rgba(148, 163, 184, 0.2);
    transform: translateX(2px);
  }

  .sidebar a.active {
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: white;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.28);
  }

  .sidebar a.disabled {
    opacity: 0.45;
    pointer-events: none;
  }

  .icon {
    font-size: 1.25rem;
  }

  .copy small {
    display: block;
    margin-top: 0.15rem;
    color: rgba(15, 23, 42, 0.65);
  }

  .sidebar a.active .copy small {
    color: rgba(255, 255, 255, 0.8);
  }

  .content {
    padding: 2rem clamp(1.5rem, 4vw, 3rem) 3rem;
    display: grid;
    gap: 1.5rem;
    background: transparent;
  }

  .intro {
    background: white;
    padding: clamp(1.75rem, 3vw, 2.5rem);
    border-radius: 1.5rem;
    box-shadow: 0 25px 50px rgba(15, 23, 42, 0.12);
  }

  .intro h1 {
    margin: 0 0 0.75rem;
    font-size: clamp(1.75rem, 3vw, 2.3rem);
  }

  .intro p {
    margin: 0;
    color: #475569;
  }

  .alert {
    padding: 0.85rem 1rem;
    border-radius: 1rem;
    font-weight: 600;
    box-shadow: 0 18px 36px rgba(15, 23, 42, 0.12);
  }

  .alert.error {
    background: #fee2e2;
    color: #991b1b;
  }

  .alert.info {
    background: #e0f2fe;
    color: #1e40af;
  }

  .close {
    border: none;
    background: transparent;
    font-size: 1.5rem;
    line-height: 1;
    padding: 0;
  }

  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.45);
    z-index: 10;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  @media (max-width: 960px) {
    .layout {
      grid-template-columns: min(280px, 70vw) 1fr;
    }
  }

  @media (max-width: 820px) {
    .layout {
      grid-template-columns: 1fr;
    }

    .sidebar {
      position: fixed;
      top: 0;
      left: 0;
      bottom: 0;
      width: min(320px, 80vw);
      transform: translateX(-100%);
      transition: transform 0.3s ease;
      box-shadow: 0 25px 60px rgba(15, 23, 42, 0.35);
    }

    .layout.sidebar-open .sidebar {
      transform: translateX(0);
    }

    .content {
      padding-top: clamp(1.5rem, 5vw, 2.5rem);
    }

    .sidebar-toggle {
      display: inline-flex;
    }
  }

  @media (min-width: 821px) {
    .sidebar-toggle {
      display: none;
    }

    .backdrop {
      display: none;
    }
  }
</style>
