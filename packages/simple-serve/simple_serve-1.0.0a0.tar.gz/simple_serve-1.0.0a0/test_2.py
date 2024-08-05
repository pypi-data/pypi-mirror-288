import uvicorn
from pydantic import create_model
from sk_serve import serve, SimpleAPI

model = create_model(
    "Model", pclass=(int, None), name=(str, None), sex=(str, None), age=(float, None), sibsp=(int, None), parch=(int, None),
    ticket=(str, None), fare=(float, None), cabin=(str, None), embarked=(str, None), boat=(int, None), body=(float, None),
    home=(str, None)
)

api = SimpleAPI("pipeline.pkl", "model.pkl", model)

app = serve(api)

if __name__ == "__main__":
    uvicorn.run("test_2:app", host="localhost", port=8000, log_level="debug", reload=True)