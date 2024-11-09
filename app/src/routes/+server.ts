import { Composer } from '@chord-ts/rpc'
import { sveltekitMiddleware } from '@chord-ts/rpc/middlewares'
import { json, RequestEvent } from '@sveltejs/kit'
import { Client as GradioClient } from "@gradio/client";


const gradio = await GradioClient.connect()


const composer = Composer.init({
  
})
export type Client = typeof composer.clientType
composer.use(sveltekitMiddleware())

export async function POST(event: RequestEvent) {
  return json(await composer.exec(event as unknown as Record<string, unknown>))
}
