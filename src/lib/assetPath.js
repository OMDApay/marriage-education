/**
 * Resolve public and built asset URLs relative to the Vite deployment base.
 * This keeps local development at `/` while supporting GitHub Pages project URLs.
 */
export function assetPath(path) {
  if (!path || typeof path !== 'string') return path
  if (/^(?:https?:|data:|blob:|#)/i.test(path)) return path

  const base = import.meta.env.BASE_URL || '/'
  if (path.startsWith(base)) return path
  if (!path.startsWith('/')) return path

  return `${base.replace(/\/$/, '')}${path}`
}
