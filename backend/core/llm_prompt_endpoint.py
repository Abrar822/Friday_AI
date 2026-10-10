from fastapi import APIRouter, Request, status, HTTPException
from ..core.llm import route_task, route_task_by_groq
from ..pydantic_models.task_router_models import TaskRouterResponse
from ..pydantic_models.llm_models.llm_models import LLMRequestModel
from ..friday_modules.persistent_memory import storage_declarations
from groq import AuthenticationError, RateLimitError

llm_prompt_router = APIRouter()


# Endpoint to generate the response from llm after receiving the prompt
@llm_prompt_router.post("/prompt", status_code=status.HTTP_200_OK)
def generate_response(request: LLMRequestModel, req: Request):
    data = None
    result = None
    try:
        llm_mode = storage_declarations.settings_details["llm_mode"]
        api_key = storage_declarations.settings_details["api_key"].strip()
        if llm_mode == "groq":
            if not api_key.strip():
                raise ValueError("Please Provide a Groq Api key.")
            data = route_task_by_groq(request.prompt, api_key)
        elif llm_mode == "qwen":
            data = route_task(request.prompt)

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

    except RateLimitError as err:
        retry_after = err.request.headers.get("retry-after")
        req.app.state.speaker.tts(
            f"Rate Limit Exceeded. Retry After {retry_after} seconds."
            if retry_after
            else "Groq rate limit exceeded. Please try again later."
        )
        return {
            "response": [
                (
                    f"Rate Limit Exceeded. Retry After {retry_after} seconds."
                    if retry_after
                    else "Groq rate limit exceeded. Please try again later."
                )
            ]
        }

    except AuthenticationError:
        req.app.state.speaker.tts("Invalid Groq Api Key.")
        return {"response": ["Invalid Groq Api Key."]}

    except ValueError as err:
        req.app.state.speaker.tts(str(err))
        return {"response": [str(err)]}

    except Exception as err:
        import traceback

        traceback.print_exc()

        req.app.state.speaker.tts("Sorry, I couldn't process that request.")
        return {"response": ["Sorry, I couldn't process that request."]}
