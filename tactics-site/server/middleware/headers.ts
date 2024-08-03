export default defineEventHandler((event) => {
  // Set headers for all routes
  setHeader(event, 'Cache-Control', 'public, max-age=0, must-revalidate')

  // Check if the request is for a file in the public folder
  if (event.node.req.url?.startsWith('/')) {
    // Generate an ETag based on the file path and current time
    // In a real-world scenario, you might want to use a more robust method
    const etag = `"${event.node.req.url}-${Date.now()}"`
    setHeader(event, 'ETag', etag)

    // Set Last-Modified header
    setHeader(event, 'Last-Modified', new Date().toUTCString())
  }

  // If you need to send a response, you can do so here
  // For middleware that just sets headers, you can omit the return or return undefined
})
