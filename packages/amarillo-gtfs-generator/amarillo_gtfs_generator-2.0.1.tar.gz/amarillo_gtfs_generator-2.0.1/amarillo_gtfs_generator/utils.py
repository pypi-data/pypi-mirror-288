import logging

from fastapi import HTTPException, status

from amarillo.models.Carpool import Region
from amarillo.services.regions import RegionService
from amarillo.utils.container import container

logger = logging.getLogger(__name__)

#TODO: move to amarillo/utils?
def _assert_region_exists(region_id: str) -> Region:
    regions: RegionService = container['regions']
    region = regions.get_region(region_id)
    region_exists = region is not None

    if not region_exists:
        message = f"Region with id {region_id} does not exist."
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return region

