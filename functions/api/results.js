export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const pw = url.searchParams.get('pw');

  if (pw !== env.RESULTS_PASSWORD) {
    return new Response(JSON.stringify({ error: 'unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  const resp = await fetch(
    `${env.SUPABASE_URL}/rest/v1/responses?select=*&order=created_at.desc`,
    {
      headers: {
        'apikey': env.SUPABASE_SERVICE_KEY,
        'Authorization': `Bearer ${env.SUPABASE_SERVICE_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );

  const data = await resp.json();
  return new Response(JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
}
