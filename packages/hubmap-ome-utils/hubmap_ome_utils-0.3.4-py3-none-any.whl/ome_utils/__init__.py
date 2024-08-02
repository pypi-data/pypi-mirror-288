import html
import re
import unicodedata
from functools import singledispatch
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, Optional, Union
from xml.etree import ElementTree as ET

import aicsimageio
import tifffile
from pint import Quantity, UnitRegistry

ome_tiff_pattern = re.compile(r"^(?P<basename>.+)\.ome\.tiff?$")

target_unit_default = "um"
spatial_dimensions = "XYZ"
reg = UnitRegistry()

Image = Union[tifffile.TiffFile, aicsimageio.AICSImage]


def find_ome_tiffs(directory: Path) -> Iterable[Path]:
    for entry in directory.iterdir():
        if ome_tiff_pattern.match(entry.name):
            yield entry


def strip_namespace_and_parse(xmlstr: str):
    it = ET.iterparse(StringIO(xmlstr))
    for _, el in it:
        _, _, el.tag = el.tag.rpartition("}")
    root = it.root
    return root


@singledispatch
def get_ome_xml_str(image):
    raise NotImplementedError(f"Unknown argument type: {type(image)}")


@get_ome_xml_str.register
def _(image: tifffile.TiffFile):
    return image.pages[0].tags["ImageDescription"].value


@get_ome_xml_str.register
def _(image: aicsimageio.AICSImage):
    return image.xarray_dask_data.unprocessed[270]


def physical_size_to_quantity(
    px_node: ET.Element,
    dimension: str,
) -> Optional[Quantity]:
    unit_str = px_node.get(f"PhysicalSize{dimension}Unit", target_unit_default)

    size_str = px_node.get(f"PhysicalSize{dimension}", None)
    if size_str is None:
        print("Could not find physical unit in OMEXML for dimension", dimension)
        return None

    unit_normalized = unicodedata.normalize("NFKC", html.unescape(unit_str))
    size = float(size_str) * reg(unit_normalized)
    return size


def convert_and_set_physical_size(
    px_node: ET.Element,
    sizes: Dict[str, Quantity],
    target_unit: str = target_unit_default,
):
    """
    Operates on px_node in place, setting PhysicalSize{dimension} and
    PhysicalSizeDimension{dimension}Unit attributes.
    """
    for dimension, size in sizes.items():
        size_converted = size.to(target_unit)
        px_node.set(f"PhysicalSize{dimension}Unit", target_unit)
        px_node.set(f"PhysicalSize{dimension}", str(size_converted.magnitude))


def get_physical_size_quantities(image: Image) -> Dict[str, Quantity]:
    xml_str = get_ome_xml_str(image)
    ome_xml: ET.Element = strip_namespace_and_parse(xml_str)
    px_node = ome_xml.find("Image").find("Pixels")
    dimensions = {}
    for dimension in spatial_dimensions:
        size = physical_size_to_quantity(px_node, dimension)
        if size is not None:
            dimensions[dimension] = size
    return dimensions


def get_converted_physical_size(
    image: Image, target_unit: str = target_unit_default
) -> Dict[str, Quantity]:
    dimensions = get_physical_size_quantities(image)
    return {dimension: size.to(target_unit) for dimension, size in dimensions.items()}
