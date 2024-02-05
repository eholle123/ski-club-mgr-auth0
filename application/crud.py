import model
from sqlmodel import Session, select

def read_all_ski_passes(session: Session) -> list[model.SkiPass]:
    statement = select(model.SkiPass)
    results = session.exec(statement)
    ski_passes = results.all()
    return ski_passes
