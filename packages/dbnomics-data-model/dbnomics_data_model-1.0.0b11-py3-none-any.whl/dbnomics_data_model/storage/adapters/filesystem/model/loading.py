from typing import cast

from typedload.dataloader import Loader

from dbnomics_data_model.json_utils.loading import create_default_loader


def create_loader() -> Loader:
    from .category_tree_json import CategoryTreeNodeJson

    loader = create_default_loader()
    loader.frefs = cast(dict[str, type], {"CategoryTreeNodeJson": CategoryTreeNodeJson})
    return loader


loader = create_loader()
