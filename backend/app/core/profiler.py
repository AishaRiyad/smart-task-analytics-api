from pyinstrument import Profiler
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse


class ProfilerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.query_params.get("profile") != "true":
            return await call_next(request)

        profiler = Profiler()
        profiler.start()

        response = await call_next(request)

        profiler.stop()

        html_report = profiler.output_html()

        return HTMLResponse(
            content=html_report,
            status_code=response.status_code
        )