from fastapi import APIRouter
from app.util.scrapper import scrapeData
from app.util.getLink import getLink
from app.util.database import ConnectDB
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from fastapi import Query


router = APIRouter()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["date", "code", "item_name", "unit", "quantity"] = "date"
    order: Literal["ASC", "DESC"] = "DESC"
    mask: list[str] = []

ALLOWED_COLUMNS = {"date", "code", "item_name", "quantity", "unit", "minimum", "maximum"}

@router.get("/")
async def rates(query: Annotated[FilterParams, Query()]):
    cursor, connection = ConnectDB()

    if query.mask:

        columns = [col for col in query.mask if col in ALLOWED_COLUMNS]
        if not columns:
            columns = list(ALLOWED_COLUMNS)
    else:
        columns = list(ALLOWED_COLUMNS)

    columns_sql = ", ".join(columns)

    order_by = query.order_by if query.order_by in ALLOWED_COLUMNS else "date"
    order = query.order if query.order in {"ASC", "DESC"} else "DESC"

    sql = f"SELECT {columns_sql} FROM rates ORDER BY {order_by} {order} LIMIT %s OFFSET %s;"
    cursor.execute(sql, (query.limit, query.offset))
    results = cursor.fetchall()

    return [dict(zip(columns, row)) for row in results]


@router.post("/refresh")
async def refresh():
    
    cursor,connection = ConnectDB()
    link,date,shouldUpdate = await getLink(cursor,connection)

    if(shouldUpdate):
        scrapeData(link,cursor,date)

    connection.commit()
    cursor.close()

    return {"message":"Database updated for today"}