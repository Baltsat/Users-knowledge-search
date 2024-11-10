import { client } from "@chord-ts/rpc";
import type { Client } from "./+server";

export const rpc = client<Client>({endpoint: '/'})

