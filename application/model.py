from typing import Optional
from sqlmodel import Field, SQLModel


class SkiPass(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Add a unique constraint for this column
    # https://github.com/tiangolo/sqlmodel/issues/82
    serial_number: str = Field(..., index=True, sa_column_kwargs={"unique": True})
    # checkout_timestamp: str 
    # checkin_timestamp: str
    # is_reserved: bool = False
    is_invalidated: bool = False


# class Skier(SQLModel, table=True):
#     member_id: Optional[int] = Field(default=None, primary_key=True)
#     # skier_name: str 
#     # skier_email: str
#     # skier_mobile_number: str
#     skier_username: str = Field(..., index=True, sa_column_kwargs={"unique": True})
#     available_prime_passes: Optional(int) = 4 # limit 4 prime passes every month
#     rule_breaks: Optional[int] = 0 # maybe 3 strikes you get kicked out of ski club
#     is_invaliated_member: bool = False

"""
Following two(?) databases should handle:
    - SkiCalendar
    - SkiPassReservations
    This should look like a calendar where the number of passes available to reserve is shown on each day.
    User clicks on day to reserve or drop passes.
    Two types of pass reservation:
        - prime passes: reservations can be made as far as 1 month out and up to 1 week out, no reservation farther in advance than 1 month
        - non prime passes: reservation request made within 72 hours of requested ski date 
    Only 14 (for example) passes available per day. When all ski passes have been reserved for that day, additional requests go on waitlist. First on waitlist would be the first user who requested passes after all 14 had been already reserved.
"""

# class SkiCalendar(SQLModel, table=True):
#     date: str = Field(..., index=True, primary_key=True)
#     number_ski_passes_available: int
#     ski_passes_available: list[SkiPass.serial_number]
#     ski_passes_reserved: list[SkiPass.serial_number]
#     waitlist: dict[Skier][int] # dictionary of skiiers and number of passes requested


# class SkiPassReservations(SQLModel, table=True):
#     date: str = Field(..., index=True, primary_key=True)
#     number_ski_passes_available: int
#     ski_passes_available: list[SkiPass.serial_number]
#     ski_passes_reserved: list[SkiPass.serial_number]
#     date_request_sent: str 
#     skier_reserving_passes: Skier.skier_username
#     is_valid_reservation: bool = True
    