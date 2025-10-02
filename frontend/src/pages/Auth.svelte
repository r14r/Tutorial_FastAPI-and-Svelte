<script>
  import { goto } from "$app/navigation";
  import { registerUser, loginUser, getProfile } from "$lib/api";
  import { token, currentUser } from "$stores/auth";

  let registerForm = { email: "", password: "" };
  let loginForm = { email: "", password: "" };
  let loading = false;
  let errorMessage = "";
  let successMessage = "";

  function resetFeedback() {
    errorMessage = "";
    successMessage = "";
  }

  async function handleRegister(event) {
    event.preventDefault();
    resetFeedback();
    loading = true;
    try {
      await registerUser(registerForm);
      successMessage = "Registration successful! You can sign in right away.";
      registerForm = { email: "", password: "" };
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Registration failed";
    } finally {
      loading = false;
    }
  }

  async function handleLogin(event) {
    event.preventDefault();
    resetFeedback();
    loading = true;
    try {
      const { access_token } = await loginUser(loginForm);
      token.set(access_token);
      const profile = await getProfile();
      currentUser.set(profile);
      successMessage = `Welcome back, ${profile.email}!`;
      loginForm = { email: "", password: "" };
      await goto("/crud");
    } catch (error) {
      errorMessage = error.response?.data?.detail ?? "Login failed";
    } finally {
      loading = false;
    }
  }
</script>

<div class="auth-grid">
  <section class="panel">
    <header>
      <h2>Register</h2>
      <p>Create a new account backed by the FastAPI users table.</p>
    </header>
    <form on:submit={handleRegister}>
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
  </section>

  <section class="panel">
    <header>
      <h2>Sign in</h2>
      <p>Receive a bearer token and persist it in local storage.</p>
    </header>
    <form on:submit={handleLogin}>
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
  </section>
</div>

{#if errorMessage}
  <div class="feedback error">{errorMessage}</div>
{/if}
{#if successMessage}
  <div class="feedback success">{successMessage}</div>
{/if}

<style>
  .auth-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
  }

  .panel {
    background: white;
    padding: 1.75rem;
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

  form {
    display: grid;
    gap: 1rem;
  }

  label {
    display: grid;
    gap: 0.4rem;
    font-weight: 600;
  }

  input {
    border: 1px solid #cbd5e0;
    border-radius: 0.85rem;
    padding: 0.7rem 0.85rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    font-size: 1rem;
  }

  input:focus {
    outline: none;
    border-color: #4299e1;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.25);
  }

  button {
    border: none;
    border-radius: 999px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    background: linear-gradient(135deg, #4299e1, #667eea);
    color: white;
    transition: filter 0.2s ease;
  }

  button:hover {
    filter: brightness(1.05);
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .feedback {
    margin-top: 1.5rem;
    padding: 0.85rem 1rem;
    border-radius: 1rem;
    font-weight: 600;
    box-shadow: 0 15px 35px rgba(15, 23, 42, 0.12);
  }

  .feedback.error {
    background: #fed7d7;
    color: #742a2a;
  }

  .feedback.success {
    background: #c6f6d5;
    color: #22543d;
  }
</style>
