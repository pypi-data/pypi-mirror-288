import requests
import json

from urllib.parse import quote

from arcgis.mapping import WebMap

from geometry.checks import is_bbox
from geometry.change_crs import change_box_crs

from .gets import get_map


def get_map_extent_aux(map_item, crs=4326):
    """
    Given a map, it returns the extent for it

    Parameters:
        map_item: WebMap item of the map to check
        crs (Optional): CRS in what to get the crs. By default in 4326
    """
    extent = map_item.item.extent
    min_x = min(extent[0][0], extent[1][0])
    max_x = max(extent[0][0], extent[1][0])
    min_y = min(extent[0][1], extent[1][1])
    max_y = max(extent[0][1], extent[1][1])
    extent = (min_x, min_y, max_x, max_y)

    base_url = map_item._gis.url
    token = map_item._gis._con.token
    if base_url.find("/home") >= 0:
        base_url = base_url.replace("/home", "")

    content_url = base_url + "sharing/rest/content/items/"
    content_url += map_item.item.id
    content_url += "/data"
    content_url += f"/?f=json&token={token}"

    data = requests.get(content_url)
    if data.status_code % 100 != 2:
        raise Exception("Couldn't Connect To The Item Information URL")

    data = data.json()
    crs = data.get("spatialReference", None)
    if crs is None:
        raise Exception("Spatial Reference Not Set")

    if "latestWkid" in crs:
        extent_crs = crs["latestWkid"]
    elif "wkid" in crs:
        extent_crs = crs["wkid"]
    else:
        raise Exception("Spatial Reference Not Set")
    
    return {'xmin': extent[0], 'ymin': extent[1], 'xmax': extent[2], 'ymax': extent[3], 'spatialReference': {'wkid': extent_crs}}


def get_map_extent(gis, map_id, crs=4326):
    """
    Given a map, it returns the extent for it

    Parameters:
        gis: GIS Item linked to the portal fo the map
        map_id: ID of the map where the map is saved
        crs (Optional): CRS in what to get the crs. By default in 4326
    """
    map_item = get_map(gis, map_id)

    return get_map_extent_aux(map_item, crs)


def set_map_extent_aux(map_item, extent_bbox, extent_crs, save=True):
    """
    Changes the home extent of a given map

    Parameters:
        - map_item: WebMap item of the map to check
        - extent_bbox: extent to set the map to (min_x, min_y, max_x, max_y).
        - extent_crs: CRS of the given extent_bbox.
        - save: If it should save on the real layer or just update the python item.
            By default in True.
    """    
    if not is_bbox(extent_bbox):
        raise Exception(f"{extent_bbox} Is Not A bbox")

    extent_bbox = change_box_crs(extent_bbox, extent_crs, 3857)
    extent_crs = 3857

    extent_degrees = change_box_crs(extent_bbox, extent_crs, 4326)

    base_url = map_item._gis.url
    token = map_item._gis._con.token
    if base_url.find("/home") >= 0:
        base_url = base_url.replace("/home", "")

    update_url = base_url + "sharing/rest/content/items/"
    update_url += map_item.item.id
    update_url += "/update"

    map_item.definition["initialState"] = {
        "viewpoint": {
            "targetGeometry": {
                "spatialReference": {
                    "latestWkid": 3857,
                    "wkid": 102100
                },
                "xmin": extent_bbox[0],
                "ymin": extent_bbox[1],
                "xmax": extent_bbox[2],
                "ymax": extent_bbox[3]
            }
        }
    }
    map_item.extent = [[extent_degrees[0], extent_degrees[1]],[extent_degrees[2], extent_degrees[3]]]
    map_item.item.update({"extent": [[extent_degrees[0], extent_degrees[1]],[extent_degrees[2], extent_degrees[3]]]})

    data = {}
    data["f"] = "json"
    data["token"] = token
    data["extent"] = f"{extent_degrees[0]}, {extent_degrees[1]}, {extent_degrees[2]}, {extent_degrees[3]}"
    data["text"] = quote(json.dumps(dict(map_item.definition)))

    print(data)
    data = requests.post(update_url, data=data)
    if data.status_code // 100 != 2:
        print(data.status_code % 100)
        raise Exception("Couldn't Connect To The Item Update URL ")

    return data.json()


def set_map_extent(gis, map_id, extent_bbox, extent_crs):
    """
    Given a map, it set the extent for it

    Parameters:
        gis: GIS Item linked to the portal fo the map
        map_id: ID of the map where the map is saved
        - extent_bbox: extent to set the map to (min_x, min_y, max_x, max_y).
        - extent_crs: CRS of the given extent_bbox.
    """
    map_item = get_map(gis, map_id)

    return set_map_extent_aux(map_item, extent_bbox, extent_crs)



def get_basemap_aux(map_item):
    """
    Given a map, it returns the basemap for it

    Parameters:
        - map_item: WebMap item of the map to check
    """
    return map_item.basemap.title


def get_basemap(gis, map_id):
    """
    Given a map, it returns the basemap for it

    Parameters:
        gis: GIS Item linked to the portal fo the map
        map_id: ID of the map where the map is saved
    """
    map_item = get_map(gis, map_id)

    return get_basemap_aux(map_item)


def create_map(gis, name, snippet=None, tags=None, extent_bbox=None, extent_crs=None):
    """
    Creates an empty map

    Parameters:
        - gis: GIS Item to use to store the map
        - name: Name to save the map with
        - snippet (Optional): Text used to describe the map. If None, none will be 
            set. By default in None.
        - tags (Optional): Tags to add to the map item. If None, none will be set. By 
            default in None.
        - extent_bbox (Optional): extent to set the map to (min_x, min_y, max_x, max_y).
            If none, full map it'll be used. By default in None.
        - extent_crs (Optional): CRS of the given extent_bbox. Must provide if extent_bbox set.
    """
    if extent_bbox and not extent_crs:
        raise Exception(f"Must Provide extent_crs [{extent_crs}] if an extent given")
    
    if not is_bbox(extent_bbox):
        raise Exception(f"{extent_bbox} Is Not A bbox")

    wm = WebMap()
    wm._gis = gis
    wm._con = gis._con

    if snippet is None:
        snippet = "Not Set"
    
    if tags is None:
        tags = []
    
    if extent_bbox is None:
        extent_bbox = [-180, -90, 180, 90]
    else:
        extent_bbox = change_box_crs(extent_bbox, extent_crs, 4326)

    extent_crs = 4326

    webmap_item_properties = {'title': name,
             'snippet': snippet,
             'tags': tags,
             'extent': {'xmin': extent_bbox[0], 'ymin': extent_bbox[1], 'xmax': extent_bbox[2], 'ymax': extent_bbox[3], 'spatialReference': {'wkid': extent_crs}}
             }

    wm.save(webmap_item_properties)

    return wm