const http = require('http');

const PORT = 3000;

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');
  
  // CORS headers so it can be called from browser if needed across origins
  res.setHeader('Access-Control-Allow-Origin', '*');

  if (req.url === '/hello' && req.method === 'GET') {
    res.writeHead(200);
    res.end(JSON.stringify({ message: 'Hello, World!' }));
  } else if (req.url === '/time' && req.method === 'GET') {
    res.writeHead(200);
    res.end(JSON.stringify({ time: new Date().toISOString() }));
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
