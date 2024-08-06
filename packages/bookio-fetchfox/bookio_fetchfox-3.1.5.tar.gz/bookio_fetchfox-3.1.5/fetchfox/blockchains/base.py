import warnings
from abc import abstractmethod
from datetime import datetime
from typing import Iterable, Tuple, Optional

from fetchfox.apis import price
from fetchfox.dtos import (
    AssetDTO,
    CampaignDTO,
    FloorDTO,
    HoldingDTO,
    ListingDTO,
    RankDTO,
    SaleDTO,
    TransactionDTO,
)


class Blockchain:
    def __init__(self, name: str, currency: str, logo: str, preprod: bool = False):
        self.name: str = name
        self.currency: str = currency
        self.logo: str = logo
        self.preprod: bool = preprod

    @property
    def usd(self) -> float:
        return price.usd(self.currency)

    # checks
    @abstractmethod
    def check_account(self, account: str, exception: bool = True) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def check_collection_id(self, collection_id: str, exception: bool = True) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def check_asset_id(self, asset_id: str, exception: bool = True) -> bool:
        raise NotImplementedError()

    # url builders
    @abstractmethod
    def explorer_url(self, *, address: str = None, collection_id: str = None, asset_id: str = None, tx_hash: str = None) -> str:
        raise NotImplementedError()

    @abstractmethod
    def marketplace_url(self, *, collection_id: str = None, asset_id: str = None) -> str:
        raise NotImplementedError()

    # accounts
    @abstractmethod
    def get_account_main_address(self, account: str, exception: bool = False) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_account_name(self, account: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def resolve_account_name(self, account: str) -> str:
        raise NotImplementedError()

    def format_account(self, account: str) -> str:
        self.check_account(account, exception=True)

        name = self.get_account_name(account)

        if name:
            return name

        return f"{account[:5]}..{account[-5:]}"

    # account attributes
    @abstractmethod
    def get_account_assets(self, account: str, collection_id: str = None) -> Iterable[HoldingDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_account_balance(self, account: str) -> Tuple[float, str]:
        raise NotImplementedError()

    @abstractmethod
    def get_account_transactions(self, account: str, last: int = 10) -> Iterable[TransactionDTO]:
        raise NotImplementedError()

    def get_account_last_transaction(self, account: str) -> TransactionDTO:
        try:
            return next(self.get_account_transactions(account, last=1))
        except StopIteration:
            return None

    # assets
    @abstractmethod
    def get_asset(self, collection_id: str, asset_id: str, *args, **kwargs) -> AssetDTO:
        raise NotImplementedError()

    @abstractmethod
    def get_asset_holders(self, collection_id: str, asset_id: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        raise NotImplementedError()

    def get_asset_rank(self, collection_id: str, asset_id: str, *args, **kwargs) -> RankDTO:
        return None

    # collections
    @abstractmethod
    def get_collection_assets(self, collection_id: str, fetch_metadata: bool = True, *args, **kwargs) -> Iterable[AssetDTO]:
        raise NotImplementedError()

    def get_collection_lock_date(self, collection_id: str, *args, **kwargs) -> datetime:
        return None

    @abstractmethod
    def get_collection_floor(self, collection_id: str, *args, **kwargs) -> FloorDTO:
        raise NotImplementedError()

    @abstractmethod
    def get_collection_supply(self, collection_id: str, *args, **kwargs) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_collection_listings(self, collection_id: str, *args, **kwargs) -> Iterable[ListingDTO]:
        raise NotImplementedError()

    def get_collection_ranks(self, collection_id: str, *args, **kwargs) -> Iterable[RankDTO]:
        return []

    @abstractmethod
    def get_collection_sales(self, collection_id: str, *args, **kwargs) -> Iterable[SaleDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_collection_holders(self, collection_id: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        raise NotImplementedError()

    # campaigns
    def get_campaigns(self, starts_after: datetime = None) -> Iterable[CampaignDTO]:
        raise NotImplementedError()

    # tokens
    def get_token_exchange(self, collection_id: str, asset_id: str) -> Optional[float]:
        return None

    # others
    def verify_otp(self, account: str, otp: float) -> TransactionDTO:
        raise NotImplementedError

    # dunders
    def __repr__(self) -> str:
        return f"{self.name} / {self.currency} (preprod={self.preprod})"

    # deprecated
    def get_asset_owners(self, collection_id: str, asset_id: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        warnings.deprecated("Use get_asset_owners instead")

        yield from self.get_asset_holders(collection_id, asset_id, *args, **kwargs)

    def get_collection_snapshot(self, collection_id: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        warnings.deprecated("Use get_collection_holders instead")

        yield from self.get_collection_holders(collection_id, *args, **kwargs)
