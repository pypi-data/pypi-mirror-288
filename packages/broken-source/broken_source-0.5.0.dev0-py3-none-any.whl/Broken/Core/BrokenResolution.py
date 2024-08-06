import math
from numbers import Number
from typing import Tuple

from Broken import log


class BrokenResolution:

    @staticmethod
    def round_component(value: Number, *, scale: Number=1) -> int:
        return max(1, 2*round(scale*value/2))

    @staticmethod
    def round_resolution(width: Number, height: Number, *, scale: Number=1) -> Tuple[int, int]:
        return (BrokenResolution.round_component(width*scale), BrokenResolution.round_component(height*scale))

    @staticmethod
    def fit(
        old: Tuple[int, int]=None,
        new: Tuple[int, int]=None,
        max: Tuple[int, int]=None,
        scale: float=1.0,
        ar: float=None,
    ) -> Tuple[int, int]:
        """Fit, Scale and optionally force Aspect Ratio on a base to a (un)limited target resolution

        This method solves the following problem:
            "A window is at some initial size (ow, oh) and a resize was asked to (nw, nh); what
            final resolution the window should be, optionally enforcing an aspect ratio (ar),
            and limited by the monitor resolution (mw, mh)?"

        To which, the behavior is as follows in the two branches:
            No aspect ratio (ar=None) is send:
                - Returns the original resolution overrided by any new (nw, nh)

            Aspect ratio (ar!=None) is send:
                - If any of the new (nw, nh) is missing, find the other based on the aspect ratio
                - Else, prioritize width changes, and downscale/upscale accordingly;
                - Post-limits resolution to (mw, mh) by multiplying both components to max fit it

        Notes
        -----
            - The resolution is rounded to the nearest multiple of 2, so FFmpeg is happy

        Parameters
        ----------
        old
            Old resolution
        new
            New resolution
        max
            Maximum resolution
        scale
            Scale factor
        ar
            Force aspect ratio, if any

        Returns
        -------
        (int, int)
            The new best-fit width and height
        """

        # Unpack
        old_width, old_height = (old or (None, None))
        new_width, new_height = (new or (None, None))
        max_width, max_height = (max or (None, None))

        log.debug(f"Fit resolution: ({old_width}, {old_height}) -> ({new_width}, {new_height})^({max_width}, {max_height}), AR {ar}")

        # Force or keep either component
        (width, height) = ((new_width or old_width), (new_height or old_height))

        if not all((width, height)):
            raise ValueError("Can't build a resolution with missing component(s): ({width}, {height})")

        if (ar is None):
            pass

        else:
            # Build from width (W) or from height (H)
            from_width  = (width, width/ar)
            from_height = (height*ar, height)

            # Pick the non missing component's
            if (new_height is None):
                (width, height) = from_width
            elif (new_width is None):
                (width, height) = from_height

            # Based on upscale or downscale
            elif (new_width != old_width):
                (width, height) = from_width
            elif (new_height != old_height):
                (width, height) = from_height

        # Limit the resolution to (mw, mh) bounding box and keep aspect ratio
        # - The idea is to find the maximum reduce factor for either component so it normalizes
        #   to the respective (mw, mh), and apply it to both components to scale down
        if (ar is not None):
            reduce = __builtins__["max"](
                width/(min(width, max_width or math.inf) or 1),
                height/(min(height, max_height or math.inf) or 1)
            ) or 1

            width, height = (width/reduce, height/reduce)

        else:
            # Limit each component independently
            width  = min(width,  max_width or math.inf)
            height = min(height, max_height or math.inf)

        return BrokenResolution.round_resolution(width=width, height=height, scale=scale)

# -------------------------------------------------------------------------------------------------|
# Test

class _PyTest:
    def test_round_component(self):
        assert BrokenResolution.round_component(100) == 100
        assert BrokenResolution.round_component(2.5) == 2
        assert BrokenResolution.round_component(3.2) == 4

    def test_round_resolution(self):
        assert BrokenResolution.round_resolution(1920, 1080)   == (1920, 1080)
        assert BrokenResolution.round_resolution(1921, 1080.0) == (1920, 1080)
        assert BrokenResolution.round_resolution(1921.5, 1080) == (1922, 1080)
        assert BrokenResolution.round_resolution(1920, 1080, scale=2) == (3840, 2160)

    def test_keep_nothing(self):
        assert BrokenResolution.fit(old=(1920, 1080)) == (1920, 1080)

    def test_override_components(self):
        assert BrokenResolution.fit(old=(1920, 1080), new=(1280, None)) == (1280, 1080)
        assert BrokenResolution.fit(old=(1920, 1080), new=(None, 720))  == (1920, 720)

    def test_missing_components(self):
        import pytest
        with pytest.raises(ValueError):
            BrokenResolution.fit(old=(1920, None), new=(1280, None))
        with pytest.raises(ValueError):
            BrokenResolution.fit(old=(None, 1080), new=(None, None))

    def test_aspect_ratio(self):
        # Widescreen
        assert BrokenResolution.fit(old=(1920, 1080), new=(1280, None), ar=16/9) == (1280, 720)
        assert BrokenResolution.fit(old=(1920, 1080), new=(None, 720),  ar=16/9) == (1280, 720)
        # Univisium
        assert BrokenResolution.fit(old=(1920, 1080), new=(1000, None), ar=2.0) == (1000, 500)
        assert BrokenResolution.fit(old=(1920, 1080), new=(None, 500),  ar=2.0) == (1000, 500)

    def test_aspect_ratio_prioritize_width(self):
        assert BrokenResolution.fit(old=(1920, 1080), new=(1000, 720), ar=2) == (1000, 500)

    def test_limit_maximum_resolution(self):
        assert BrokenResolution.fit(old=(3840, 2160), new=(3800, 2100), max=(1920, 1080)) == (1920, 1080)
        assert BrokenResolution.fit(old=(3000, 3000), new=(2000, 2000), max=(6000, 720), ar=16/9) == (1280, 720)

