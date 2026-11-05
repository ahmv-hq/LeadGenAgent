export default {
  async fetch(request, env) {
    // Reverse proxy to active agent backend tunnel
    const backendOrigin = "https://expressions-breed-acre-sellers.trycloudflare.com";
    const url = new URL(request.url);
    const targetUrl = new URL(url.pathname + url.search, backendOrigin);

    const newRequest = new Request(targetUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: "follow"
    });

    return fetch(newRequest);
  }
};
