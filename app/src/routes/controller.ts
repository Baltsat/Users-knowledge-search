import {PUBLIC_BACKEND_HOST} from '$env/static/public'

async function search(query: string){
  return fetch(`${PUBLIC_BACKEND_HOST}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      accept: 'application/json'
    },
    body: JSON.stringify({query})
  }).then(r => r.json())
}
