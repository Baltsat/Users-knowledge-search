import { bot } from "./bot";

export async function POST({ request }) {
  const update = await request.json();
  await bot.handleUpdate(update);
  return new Response( 'ok')
}