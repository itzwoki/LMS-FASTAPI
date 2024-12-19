import fastapi

router = fastapi.APIRouter()

@router.get("/sections/{id}")
async def read_sections():
    return {"courses": []}


@router.get("/section/{id}/content-blocks")
async def read_section_content_block():
    return {"courses": []}

@router.get("/content-blocks/{id}")
async def read_content_block():
    return {"courses": []}


