import { Composer, rpc } from '@chord-ts/rpc'
import { sveltekitMiddleware } from '@chord-ts/rpc/middlewares'
import { json, RequestEvent } from '@sveltejs/kit'



class FastApi {
  @rpc()
  async search(query: string) {
    return fetch('http://localhost:8000/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        accept: 'application/json'
      },
      body: JSON.stringify({query})
    }).then(r => r.json())
  }
}

const composer = Composer.init({
  FastApi: new FastApi()
})

export type Client = typeof composer.clientType
composer.use(sveltekitMiddleware())

export async function POST(event: RequestEvent) {
  return json(await composer.exec(event as unknown as Record<string, unknown>))
}
