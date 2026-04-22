"""Modal deployment entrypoint.

Deploy from the **repo root** so the skill bundle and tokens.json
(which live outside `service/`) are reachable:

    cd /path/to/noba
    modal deploy service/modal_app.py

Secrets expected (create once per environment):
    modal secret create noba-deck-service-secrets \\
        NOBA_API_KEY=<team-key> \\
        ANTHROPIC_API_KEY=<anthropic-key>

The volume `noba-decks` stores generated .pptx files for 30 days
(decision D2). Lifecycle management is out-of-band; treat the volume
as ephemeral + bounded.

Inside the deployed image the layout is:

    /root/
    ├── app.py, auth.py, audit.py
    ├── routes/, services/, prompts/, models/
    ├── design/tokens.json
    └── .claude/skills/noba-presentation/
        ├── SKILL.md
        ├── references/*.md
        └── scripts/{build_deck.py, tokens.py}

That mirrors the repo so `prompts/system_prompt.py` and
`services/deck_builder.py` resolve paths identically to local dev.
"""
from __future__ import annotations

import modal

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi>=0.115",
        "pydantic>=2.9",
        "anthropic>=0.39",
        "python-pptx>=1.0",
        "structlog>=24.4",
    )
    # Service code — relative paths work because modal is invoked from
    # repo root (see docstring).
    .add_local_python_source("app", "auth", "audit", copy=True, from_dir="service")
    .add_local_dir("service/routes",   "/root/routes")
    .add_local_dir("service/services", "/root/services")
    .add_local_dir("service/prompts",  "/root/prompts")
    .add_local_dir("service/models",   "/root/models")
    # Skill bundle + design tokens — read at runtime by system_prompt.py
    # (SKILL.md + references/*.md) and by deck_builder.py (build_deck.py,
    # tokens.py, tokens.json).
    .add_local_dir(".claude/skills/noba-presentation",
                   "/root/.claude/skills/noba-presentation")
    .add_local_file("design/tokens.json", "/root/design/tokens.json")
)

volume = modal.Volume.from_name("noba-decks", create_if_missing=True)

app = modal.App("noba-deck-service", image=image)


@app.function(
    secrets=[modal.Secret.from_name("noba-deck-service-secrets")],
    volumes={"/data": volume},
    min_containers=0,
    max_containers=10,
    timeout=300,
)
@modal.asgi_app()
def fastapi_app():
    import os

    os.environ.setdefault("NOBA_STORAGE_ROOT", "/data")
    # NOBA_PUBLIC_BASE is injected from Modal's deployed URL post-deploy;
    # until then download links fall back to the local default in services/storage.py.

    from app import app as fastapi_instance

    return fastapi_instance
