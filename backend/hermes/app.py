from esmerald import Esmerald, JSONResponse

app = Esmerald()


@app.get(path="test")
def welcome() -> JSONResponse:
    return JSONResponse({"message": "Welcome to Hermod"})
