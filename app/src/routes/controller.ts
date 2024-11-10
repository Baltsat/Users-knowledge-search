import {PUBLIC_BACKEND_HOST} from '$env/static/public'

export async function submitSearch(query: string){
  return fetch(`${PUBLIC_BACKEND_HOST}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      accept: 'application/json'
    },
    body: JSON.stringify({query})
  }).then(r => r.json())
}
