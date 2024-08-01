"""
Readback and visualization methods for Grid class
"""
from typing import Any, TYPE_CHECKING

import numpy
from numpy.typing import NDArray

from . import GridError
from .position import GridPosMixin

if TYPE_CHECKING:
    import matplotlib.axes
    import matplotlib.figure


# .visualize_* uses matplotlib
# .visualize_isosurface uses skimage
# .visualize_isosurface uses mpl_toolkits.mplot3d


class GridReadMixin(GridPosMixin):
    def get_slice(
            self,
            cell_data: NDArray,
            surface_normal: int,
            center: float,
            which_shifts: int = 0,
            sample_period: int = 1
            ) -> NDArray:
        """
        Retrieve a slice of a grid.
        Interpolates if given a position between two planes.

        Args:
            cell_data: Cell data to slice
            surface_normal: Axis normal to the plane we're displaying. Integer in `range(3)`.
            center: Scalar specifying position along surface_normal axis.
            which_shifts: Which grid to display. Default is the first grid (0).
            sample_period: Period for down-sampling the image. Default 1 (disabled)

        Returns:
            Array containing the portion of the grid.
        """
        if numpy.size(center) != 1 or not numpy.isreal(center):
            raise GridError('center must be a real scalar')

        sp = round(sample_period)
        if sp <= 0:
            raise GridError('sample_period must be positive')

        if numpy.size(which_shifts) != 1 or which_shifts < 0:
            raise GridError('Invalid which_shifts')

        if surface_normal not in range(3):
            raise GridError('Invalid surface_normal direction')

        surface = numpy.delete(range(3), surface_normal)

        # Extract indices and weights of planes
        center3 = numpy.insert([0, 0], surface_normal, (center,))
        center_index = self.pos2ind(center3, which_shifts,
                                    round_ind=False, check_bounds=False)[surface_normal]
        centers = numpy.unique([numpy.floor(center_index), numpy.ceil(center_index)]).astype(int)
        if len(centers) == 2:
            fpart = center_index - numpy.floor(center_index)
            w = [1 - fpart, fpart]  # longer distance -> less weight
        else:
            w = [1]

        c_min, c_max = (self.xyz[surface_normal][i] for i in [0, -1])
        if center < c_min or center > c_max:
            raise GridError('Coordinate of selected plane must be within simulation domain')

        # Extract grid values from planes above and below visualized slice
        sliced_grid = numpy.zeros(self.shape[surface])
        for ci, weight in zip(centers, w, strict=True):
            s = tuple(ci if a == surface_normal else numpy.s_[::sp] for a in range(3))
            sliced_grid += weight * cell_data[which_shifts][tuple(s)]

        # Remove extra dimensions
        sliced_grid = numpy.squeeze(sliced_grid)

        return sliced_grid


    def visualize_slice(
            self,
            cell_data: NDArray,
            surface_normal: int,
            center: float,
            which_shifts: int = 0,
            sample_period: int = 1,
            finalize: bool = True,
            pcolormesh_args: dict[str, Any] | None = None,
            ) -> tuple['matplotlib.axes.Axes', 'matplotlib.figure.Figure']:
        """
        Visualize a slice of a grid.
        Interpolates if given a position between two planes.

        Args:
            surface_normal: Axis normal to the plane we're displaying. Integer in `range(3)`.
            center: Scalar specifying position along surface_normal axis.
            which_shifts: Which grid to display. Default is the first grid (0).
            sample_period: Period for down-sampling the image. Default 1 (disabled)
            finalize: Whether to call `pyplot.show()` after constructing the plot. Default `True`

        Returns:
            (Figure, Axes)
        """
        from matplotlib import pyplot

        if pcolormesh_args is None:
            pcolormesh_args = {}

        grid_slice = self.get_slice(cell_data=cell_data,
                                    surface_normal=surface_normal,
                                    center=center,
                                    which_shifts=which_shifts,
                                    sample_period=sample_period)

        surface = numpy.delete(range(3), surface_normal)

        x, y = (self.shifted_exyz(which_shifts)[a] for a in surface)
        xmesh, ymesh = numpy.meshgrid(x, y, indexing='ij')
        x_label, y_label = ('xyz'[a] for a in surface)

        fig, ax = pyplot.subplots()
        mappable = ax.pcolormesh(xmesh, ymesh, grid_slice, **pcolormesh_args)
        fig.colorbar(mappable)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        if finalize:
            pyplot.show()

        return fig, ax


    def visualize_isosurface(
            self,
            cell_data: NDArray,
            level: float | None = None,
            which_shifts: int = 0,
            sample_period: int = 1,
            show_edges: bool = True,
            finalize: bool = True,
            ) -> tuple['matplotlib.axes.Axes', 'matplotlib.figure.Figure']:
        """
        Draw an isosurface plot of the device.

        Args:
            cell_data: Cell data to visualize
            level: Value at which to find isosurface. Default (None) uses mean value in grid.
            which_shifts: Which grid to display. Default is the first grid (0).
            sample_period: Period for down-sampling the image. Default 1 (disabled)
            show_edges: Whether to draw triangle edges. Default `True`
            finalize: Whether to call `pyplot.show()` after constructing the plot. Default `True`

        Returns:
            (Figure, Axes)
        """
        from matplotlib import pyplot
        import skimage.measure
        # Claims to be unused, but needed for subplot(projection='3d')
        from mpl_toolkits.mplot3d import Axes3D
        del Axes3D      # imported for side effects only

        # Get data from cell_data
        grid = cell_data[which_shifts][::sample_period, ::sample_period, ::sample_period]
        if level is None:
            level = grid.mean()

        # Find isosurface with marching cubes
        verts, faces, _normals, _values = skimage.measure.marching_cubes(grid, level)

        # Convert vertices from index to position
        pos_verts = numpy.array([self.ind2pos(verts[i, :], which_shifts, round_ind=False)
                                 for i in range(verts.shape[0])], dtype=float)
        xs, ys, zs = (pos_verts[:, a] for a in range(3))

        # Draw the plot
        fig = pyplot.figure()
        ax = fig.add_subplot(111, projection='3d')
        if show_edges:
            ax.plot_trisurf(xs, ys, faces, zs)
        else:
            ax.plot_trisurf(xs, ys, faces, zs, edgecolor='none')

        # Add a fake plot of a cube to force the axes to be equal lengths
        max_range = numpy.array([xs.max() - xs.min(),
                                 ys.max() - ys.min(),
                                 zs.max() - zs.min()], dtype=float).max()
        mg = numpy.mgrid[-1:2:2, -1:2:2, -1:2:2]
        xbs = 0.5 * max_range * mg[0].flatten() + 0.5 * (xs.max() + xs.min())
        ybs = 0.5 * max_range * mg[1].flatten() + 0.5 * (ys.max() + ys.min())
        zbs = 0.5 * max_range * mg[2].flatten() + 0.5 * (zs.max() + zs.min())
        # Comment or uncomment following both lines to test the fake bounding box:
        for xb, yb, zb in zip(xbs, ybs, zbs, strict=True):
            ax.plot([xb], [yb], [zb], 'w')

        if finalize:
            pyplot.show()

        return fig, ax
