import amadeus

from amadeus import Client, ResponseError

amadeus = Client(
    client_id=AMADEUS_API_KEY,
    client_secret=AMADEUS_API_SECRET
)
