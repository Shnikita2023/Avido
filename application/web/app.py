from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.web.views import router as router_v1

app = FastAPI(version="1.1.1", title="Avido", docs_url="/api/docs", debug=True)

app.include_router(router_v1, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
