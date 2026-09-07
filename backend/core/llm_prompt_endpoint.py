from fastapi import APIRouter, Request
from ..core.llm import route_task
from ..pydantic_models.task_router_models import TaskRouterResponse
from ..pydantic_models.llm_models.llm_models import LLMRequestModel

llm_prompt_router = APIRouter()


# Endpoint to generate the response from llm after receiving the prompt
@llm_prompt_router.post("/prompt")
def generate_response(request: LLMRequestModel, req: Request):
    data = None
    result = None
    try:
        data = route_task(request.prompt)
        print(repr(data))

        data = TaskRouterResponse.model_validate(data)

        req.app.state.speaker.tts(data.response)

        result = req.app.state.ai.execute(data.tasks)
        print("result", result)

        for res in result:
            req.app.state.speaker.tts(res)

        return {"response": [data.response] + result}

    except Exception as err:
        print('llm endpoint', repr(data))
        req.app.state.speaker.tts("Sorry, I couldn't process that request.")
        print(str(err))
        return {"response": ["Sorry, I couldn't process that request."]}
    finally:
        print("Data returned by llm", data)
        print("result", result)

