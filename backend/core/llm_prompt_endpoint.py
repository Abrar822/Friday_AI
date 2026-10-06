from fastapi import APIRouter, Request, status
from ..core.llm import route_task, route_task_by_groq
from ..pydantic_models.task_router_models import TaskRouterResponse
from ..pydantic_models.llm_models.llm_models import LLMRequestModel
from ..friday_modules.persistent_memory import storage_declarations

llm_prompt_router = APIRouter()


# Endpoint to generate the response from llm after receiving the prompt
@llm_prompt_router.post("/prompt", status_code=status.HTTP_200_OK)
def generate_response(request: LLMRequestModel, req: Request):
    data = None
    result = None
    try:
        llm_mode = storage_declarations.settings_details['llm_mode']
        api_key = storage_declarations.settings_details['api_key']
        if llm_mode == "groq":
            data = route_task_by_groq(request.prompt, api_key)
        elif llm_mode == "qwen":
            data = route_task(request.prompt)

        print('Taskrouter: ', llm_mode)
        data = TaskRouterResponse.model_validate(data)

        if len(data.acknowledgement_before_task.strip()) > 0:
            req.app.state.speaker.tts(data.acknowledgement_before_task.strip())

        result = req.app.state.ai.execute(data.tasks)

        for res in result:
            req.app.state.speaker.tts(res)

        if len(data.acknowledgement_before_task.strip()) > 0:
            result = [data.acknowledgement_before_task] + result
        else:
            result = result

        return {"response": result}

    except Exception as err:
        print("Response returned by llm: ", repr(data))
        print(str(err))
        import traceback
        traceback.print_exc()

        req.app.state.speaker.tts("Sorry, I couldn't process that request.")
        return {"response": ["Sorry, I couldn't process that request."]}
    finally:
        print("Response returned by llm: ", data)
        print("Result: ", result)
