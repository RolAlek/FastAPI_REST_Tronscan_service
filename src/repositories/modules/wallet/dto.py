from dataclasses import dataclass

from domain.base import AbstractDTO


@dataclass
class CreateWalletDTO(AbstractDTO):
    address: str
    bandwidth: float
    energy: float
    trx_balance: float
