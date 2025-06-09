import httpx

from cachetools import TTLCache, cached
import google.auth


@cached(TTLCache(maxsize=1, ttl=3599))
def get_id_token() -> str:
    url = 'https://oauth2.googleapis.com/token'
    creds = google.auth.default()[0]
    params = {
        'grant_type': 'refresh_token',
        'client_id': creds._client_id,  # type: ignore
        'client_secret': creds._client_secret,  # type: ignore
        'refresh_token': creds.refresh_token,  # type: ignore
    }
    request = httpx.post(
        url=url,
        params=params,
    )
    request.raise_for_status()
    id_token = request.json()['id_token']
    return id_token


class GCPBearerAuth(httpx.Auth):
    def __init__(self):
        self.token = get_id_token()

    def auth_flow(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        response: httpx.Response = yield request
        if response.status_code == 401 or response.status_code == 403:
            self.token = get_id_token()
            request.headers['Authentication'] = f'Bearer {self.token}'
            yield request
