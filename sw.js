// MiniTool Service Worker
const CACHE_NAME = 'minitool-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/privacy.html',
  '/terms.html'
];

// Install: cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS).catch(() => {
        // Don't fail if assets aren't available during install
      });
    })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: network first, fallback to cache
self.addEventListener('fetch', event => {
  // Skip non-GET and cross-origin requests (except CDN)
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  const isSameOrigin = url.origin === location.origin;
  const isCDN = ['unpkg.com', 'cdnjs.cloudflare.com', 'cdn.jsdelivr.net', 'fonts.googleapis.com', 'fonts.gstatic.com'].includes(url.hostname);

  if (isSameOrigin || isCDN) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        const fetchPromise = fetch(event.request).then(response => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        }).catch(() => cached);
        return cached || fetchPromise;
      })
    );
  }
});
