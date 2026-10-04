from fastapi import APIRouter, Request, status
from ..core.llm import route_task, route_task_by_groq
from ..pydantic_models.task_router_models import TaskRouterResponse
from ..pydantic_models.llm_models.llm_models import LLMRequestModel

llm_prompt_router = APIRouter()


# Endpoint to generate the response from llm after receiving the prompt
@llm_prompt_router.post("/prompt", status_code=status.HTTP_200_OK)
def generate_response(request: LLMRequestModel, req: Request):
    data = None
    result = None
    try:
        if req.app.state.llm_mode == 'groq':
            data = route_task_by_groq(request.prompt)
        elif req.app.state.llm_mode == 'qwen':
            data = route_task(request.prompt)
        print(repr(data))

        data = TaskRouterResponse.model_validate(data)

        if len(data.acknowledgement_response.strip()) > 0:
            req.app.state.speaker.tts(data.acknowledgement_response.strip())

        result = req.app.state.ai.execute(data.tasks)
        print("result", result)

        for res in result:
            req.app.state.speaker.tts(res)

        if len(data.acknowledgement_response.strip()) > 0:
            result = [data.acknowledgement_response] + result
        else:
            result = result
            
        return {"response": result}

    except Exception as err:
        print("llm endpoint", repr(data))
        req.app.state.speaker.tts("Sorry, I couldn't process that request.")
        print(str(err))
        return {"response": ["Sorry, I couldn't process that request."]}
    finally:
        print("Data returned by llm", data)
        print("result", result)
