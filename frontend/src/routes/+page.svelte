<script>
  const highlights = [
    {
      title: "Authentication",
      copy: "Register users, issue bearer tokens, and persist credentials securely in the browser.",
      href: "/auth"
    },
    {
      title: "CRUD dashboard",
      copy: "Create, update, and delete notes that are stored in SQLite via FastAPI endpoints.",
      href: "/crud"
    },
    {
      title: "Database queries",
      copy: "Experiment with pagination parameters and inspect derived analytics from API responses.",
      href: "/database"
    },
    {
      title: "Core Svelte features",
      copy: "Playground showcasing reactivity, bindings, and store-driven state management.",
      href: "/core"
    }
  ];
</script>

<section class="welcome">
  <article class="hero">
    <h2>Build a modern full-stack app</h2>
    <p>
      This tutorial pairs a FastAPI backend with a freshly upgraded SvelteKit front-end. Use the sidebar to
      navigate through each feature and dive into real examples that you can adapt to your own projects.
    </p>
  </article>

  <div class="grid">
    {#each highlights as highlight}
      <a class="card" href={highlight.href}>
        <h3>{highlight.title}</h3>
        <p>{highlight.copy}</p>
        <span aria-hidden="true">→</span>
      </a>
    {/each}
  </div>
</section>

<style>
  .welcome {
    display: grid;
    gap: 1.75rem;
  }

  .hero {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.85), rgba(14, 165, 233, 0.85));
    color: white;
    padding: clamp(1.75rem, 3vw, 2.5rem);
    border-radius: 1.5rem;
    box-shadow: 0 25px 50px rgba(79, 70, 229, 0.35);
    display: grid;
    gap: 1rem;
  }

  .hero h2 {
    margin: 0;
    font-size: clamp(1.8rem, 3vw, 2.4rem);
  }

  .hero p {
    margin: 0;
    line-height: 1.6;
  }

  .grid {
    display: grid;
    gap: 1rem;
  }

  @media (min-width: 880px) {
    .grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  .card {
    text-decoration: none;
    padding: 1.5rem;
    border-radius: 1.25rem;
    background: white;
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
    display: grid;
    gap: 0.75rem;
    color: inherit;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .card span {
    font-size: 1.5rem;
    justify-self: flex-end;
  }

  .card:hover,
  .card:focus-visible {
    transform: translateY(-4px);
    box-shadow: 0 25px 55px rgba(15, 23, 42, 0.18);
  }
</style>
