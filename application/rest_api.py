import model
import schema
import crud
from custom_exceptions import AlreadyExistsException
from dependencies import get_engine, validate_token

from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.post("/ski_pass", dependencies=[Depends(validate_token)])
def create_ski_pass(ski_pass: schema.SkiPassCreate, engine: Engine = Depends(get_engine)) -> schema.SkiPassPublic:
    try:
        with Session(engine) as session:
            ski_pass_created = crud.create_ski_pass(session, ski_pass.serial_number)
            session.commit()
            session.refresh(ski_pass_created)
            return schema.SkiPassPublic(serial_number=ski_pass_created.serial_number, is_invalidated=ski_pass_created.is_invalidated)
    except IntegrityError:
        raise AlreadyExistsException


@router.get("/ski_pass")
def get_all_ski_passes(engine: Engine = Depends(get_engine)) -> list[model.SkiPass]:
    with Session(engine) as session:
        return crud.read_all_ski_passes(session)


@router.get("/ski_pass/{serial_number}")
def get_ski_pass(serial_number: str, engine: Engine = Depends(get_engine)) -> model.SkiPass:
    with Session(engine) as session:
        return crud.read_ski_pass(session, serial_number)


@router.put("/ski_pass/{serial_number}", dependencies=[Depends(validate_token)])
def invalidate_ski_pass(serial_number: str, engine: Engine = Depends(get_engine)) -> schema.SkiPassPublic:
    with Session(engine) as session:
        invalidated_ski_pass = crud.invalidate_ski_pass(session, serial_number)
        session.commit()
        session.refresh(invalidated_ski_pass)
    return schema.SkiPassPublic(
        serial_number=invalidated_ski_pass.serial_number, is_invalidated=invalidated_ski_pass.is_invalidated
    )


@router.delete("/ski_pass/{serial_number}", dependencies=[Depends(validate_token)])
def delete_ski_pass(serial_number: str, engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        crud.delete_ski_pass(session, serial_number)
        session.commit()
    return {"message": "Success"}