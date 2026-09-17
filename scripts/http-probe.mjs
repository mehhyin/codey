import { get } from 'node:http';

// Native fetch can discard an overridden Host header. These local probes must
// send the public host exactly as the reverse proxy does.
export function httpProbe(url, host, timeout = 4000) {
  return new Promise((resolve, reject) => {
    const request = get(url, { headers: { Host: host }, timeout }, response => {
      let body = '';
      response.setEncoding('utf8');
      response.on('data', chunk => { body += chunk; });
      response.on('error', reject);
      response.on('end', () => resolve({ status: response.statusCode, body }));
    });
    request.on('timeout', () => request.destroy(new Error('HTTP probe timed out.')));
    request.on('error', reject);
  });
}
