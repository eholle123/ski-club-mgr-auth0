import model
from fastapi import HTTPException
from sqlmodel import Session, select


def create_ski_pass(session: Session, serial_number: str) -> model.SkiPass:
    ski_pass = model.SkiPass(serial_number=serial_number)
    session.add(ski_pass)
    return ski_pass
    

def read_all_ski_passes(session: Session) -> list[model.SkiPass]:
    statement = select(model.SkiPass)
    results = session.exec(statement)
    ski_passes = results.all()
    return ski_passes


def read_ski_pass(session: Session, serial_number: str) -> model.SkiPass:
    statement = select(model.SkiPass).where(model.SkiPass.serial_number == serial_number)
    results = session.exec(statement)
    ski_pass = results.first()
    return ski_pass


def invalidate_ski_pass(session: Session, serial_number: str) -> model.SkiPass:
    ski_pass = read_ski_pass(session, serial_number)

    if ski_pass is None:
        raise HTTPException(status_code=404, detail=f"No ski pass with serial number {serial_number}")
    
    ski_pass.is_invalidated = True
    return ski_pass

def delete_ski_pass(session: Session, serial_number: str) -> None:
    ski_pass = read_ski_pass(session, serial_number)
    session.delete(ski_pass)
