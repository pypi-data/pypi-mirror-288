import pytest

from milgeo import Geometry


@pytest.mark.parametrize("name, coordinates, sidc, fill_color, fill_opacity, "
                         "observation_datetime, quantity, expected_exception", [
                             ("Valid input", [(0, 0)], "12345678901234567890", "#ff0000", "0.5", None, None, None),
                             ("Invalid SIDC length", [(0, 0)], "123456", None, None, None, None, ValueError),
                             ("Invalid fill color", [(0, 0)], None, "not_a_color", None, None, None, ValueError),
                             ("Invalid fill opacity", [(0, 0)], None, "#ff0000", "2", None, None, ValueError),
                             ("Invalid observation datetime", [(0, 0)], None, None, None, "2020-13-01T00:00:00", None,
                              ValueError),
                             ("Invalid quantity", [(0, 0)], None, None, None, None, "12.5", ValueError),
                             ("Empty coordinates", [], None, None, None, None, None, ValueError),
                         ])
def test_geometry_post_init(name, coordinates, sidc, fill_color, fill_opacity,
                            observation_datetime, quantity, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            Geometry(
                name=name,
                coordinates=coordinates,
                sidc=sidc,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                observation_datetime=observation_datetime,
                quantity=quantity
            )
    else:
        geom = Geometry(
            name=name,
            coordinates=coordinates,
            sidc=sidc,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            observation_datetime=observation_datetime,
            quantity=quantity
        )
        assert geom.name == name
        assert geom.coordinates == coordinates
        assert geom.sidc == sidc
        assert geom.fill_color == fill_color
        assert geom.fill_opacity == fill_opacity
        assert geom.observation_datetime == observation_datetime
        assert geom.quantity == quantity
