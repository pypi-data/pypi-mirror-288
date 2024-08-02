import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Axes3D import has side effects, it enables using projection='3d' in add_subplot
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, PolyCollection

# import required typing classes
from typing import TYPE_CHECKING, List, Optional

from stem.mesh import Mesh
from stem.model_part import BodyModelPart, ModelPart

if TYPE_CHECKING:
    from stem.geometry import Geometry, Volume, Surface


class PlotUtils:

    @staticmethod
    def __add_2d_surface_to_plot(geometry: 'Geometry', surface: 'Surface', show_surface_ids, show_line_ids,
                                 show_point_ids, ax):
        """
        Adds a 2D surface to a plot

        Args:
            - geometry (stem.geometry.Geometry): geometry object
            - surface (stem.geometry.Surface): surface object
            - show_surface_ids (bool): flag to show surface ids
            - show_line_ids (bool): flag to show line ids
            - show_point_ids (bool): flag to show point ids
            - ax (matplotlib.axes.Axes): axes object to which the surface is added

        Returns:
            - NDArray[float]: surface centroid

        """
        # initialize list of surface point ids
        surface_point_ids: List[int] = []

        # calculate centroids of lines to show line ids
        line_centroids = []
        for line_k in surface.line_ids:

            # get current line
            line = geometry.lines[abs(line_k)]

            # copy line point ids as line_connectivities can be reversed
            line_connectivities = np.copy(line.point_ids)

            # reverse line connectivity if line is defined in opposite direction
            if line_k < 0:
                line_connectivities = line_connectivities[::-1]

            # calculate line centroid
            line_centroids.append(
                np.mean([
                    geometry.points[line_connectivities[0]].coordinates,
                    geometry.points[line_connectivities[1]].coordinates
                ],
                        axis=0))

            surface_point_ids.extend(line_connectivities)

        # get unique points within surface
        unique_points = []
        for point_id in surface_point_ids:

            if point_id not in unique_points:
                unique_points.append(point_id)

        # get coordinates of surface points
        surface_point_coordinates = np.array([geometry.points[point_id].coordinates for point_id in unique_points])

        # set vertices in format as required by Poly3DCollection
        vertices = [list(zip(surface_point_coordinates[:, 0], surface_point_coordinates[:, 1]))]

        # create Poly3DCollection
        poly = PolyCollection(vertices, facecolors='blue', linewidths=1, edgecolors='black', alpha=0.35)

        # calculate surface centroid and add to list of all surface centroids which are required to calculate
        # the volume centroid
        surface_centroid = np.mean(surface_point_coordinates, axis=0)

        # show surface ids
        if show_surface_ids:
            ax.text(surface_centroid[0],
                    surface_centroid[1],
                    f"s_{abs(surface.id)}",
                    color='black',
                    fontsize=14,
                    fontweight='bold')

        # show line ids
        if show_line_ids:
            for line_centroid, line_k in zip(line_centroids, surface.line_ids):
                ax.text(line_centroid[0],
                        line_centroid[1],
                        f"l_{abs(line_k)}",
                        color='black',
                        fontsize=14,
                        fontweight='bold')

        # show point ids
        if show_point_ids:
            for point_id, point in geometry.points.items():
                ax.text(point.coordinates[0],
                        point.coordinates[1],
                        f"p_{point_id}",
                        color='black',
                        fontsize=14,
                        fontweight='bold')

        # add PolyCollection to figure
        ax.add_collection(poly)

        return surface_centroid

    @staticmethod
    def __add_3d_surface_to_plot(geometry: 'Geometry', surface: 'Surface', show_surface_ids, show_line_ids,
                                 show_point_ids, ax):
        """
        Adds a 3D surface to a plot.

        Args:
            - geometry (stem.geometry.Geometry): geometry object
            - surface (stem.geometry.Surface): surface object
            - show_surface_ids (bool): flag to show surface ids
            - show_line_ids (bool): flag to show line ids
            - show_point_ids (bool): flag to show point ids
            - ax (mpl_toolkits.mplot3d.axes3d.Axes3D): axes object to which the surface is added

        Returns:
            - NDArray[float]: surface centroid

        """

        import plotly.graph_objects as go

        # initialize list of surface point ids
        surface_point_ids: List[int] = []

        # calculate centroids of lines to show line ids
        line_centroids = []
        for line_k in surface.line_ids:

            # get current line
            line = geometry.lines[abs(line_k)]

            # copy line point ids as line_connectivities can be reversed
            line_connectivities = np.copy(line.point_ids)

            # reverse line connectivity if line is defined in opposite direction
            if line_k < 0:
                line_connectivities = line_connectivities[::-1]

            # calculate line centroid
            line_centroids.append(
                np.mean([
                    geometry.points[line_connectivities[0]].coordinates,
                    geometry.points[line_connectivities[1]].coordinates
                ],
                        axis=0))

            surface_point_ids.extend(line_connectivities)

        # get unique points within surface
        unique_points = []
        for point_id in surface_point_ids:

            if point_id not in unique_points:
                unique_points.append(point_id)

        # get coordinates of surface points
        surface_point_coordinates = np.array([geometry.points[point_id].coordinates for point_id in unique_points])

        # set vertices in format as required by Poly3DCollection
        vertices = [
            list(zip(surface_point_coordinates[:, 0], surface_point_coordinates[:, 1], surface_point_coordinates[:, 2]))
        ]

        delaunayaxis = 'z'
        if np.allclose(surface_point_coordinates[:, 0], surface_point_coordinates[0, 0]):
            delaunayaxis = 'x'
        elif np.allclose(surface_point_coordinates[:, 1], surface_point_coordinates[0, 1]):
            delaunayaxis = 'y'
        data = go.Mesh3d(x=surface_point_coordinates[:, 0],
                         y=surface_point_coordinates[:, 1],
                         z=surface_point_coordinates[:, 2],
                         opacity=0.65,
                         showscale=False,
                         delaunayaxis=delaunayaxis,
                         color='blue')
        # surface = go.Surface(x=list(surface_point_coordinates[:, 0]), y=list(surface_point_coordinates[:, 1]),
        #                   z=list(surface_point_coordinates[:, 2]), opacity=0.9, showscale=False)
        surface = ""

        # fig = go.Figure(data=[go.Mesh3d(x=surface_point_coordinates[:, 0], y=surface_point_coordinates[:, 1],
        #                                 z=surface_point_coordinates[:, 2], color='lightpink', opacity=0.50)])

        # # create Poly3DCollection
        # poly = Poly3DCollection(vertices, facecolors='blue', linewidths=1, edgecolors='black', alpha=0.35)
        #
        # # calculate surface centroid and add to list of all surface centroids which are required to calculate
        # # the volume centroid
        # surface_centroid = np.mean(surface_point_coordinates, axis=0)
        #
        # # show surface ids
        # if show_surface_ids:
        #     ax.text(surface_centroid[0], surface_centroid[1], surface_centroid[2], f"s_{abs(surface.id)}",
        #             color='black', fontsize=14, fontweight='bold')
        #
        # # show line ids
        # if show_line_ids:
        #     for line_centroid, line_k in zip(line_centroids, surface.line_ids):
        #         ax.text(line_centroid[0], line_centroid[1], line_centroid[2], f"l_{abs(line_k)}",
        #                 color='black', fontsize=14, fontweight='bold')
        #
        # # show point ids
        # if show_point_ids:
        #     for point_id, point in geometry.points.items():
        #         ax.text(point.coordinates[0], point.coordinates[1], point.coordinates[2], f"p_{point_id}",
        #                 color='black', fontsize=14, fontweight='bold')
        #
        # # add Poly3DCollection to figure
        # ax.add_collection3d(poly)

        return data, surface
        # return surface_centroid

    @staticmethod
    def __add_3d_volume_to_plot(geometry: 'Geometry', volume: 'Volume', show_volume_ids, show_surface_ids,
                                show_line_ids, show_point_ids, ax):
        """
        Adds a 3D volume to a matplotlib figure.

        Args:
            - geometry (:class:`stem.geometry.Geometry`): Geometry object
            - volume (:class:`stem.geometry.Volume`): Volume object
            - show_volume_ids (bool): Show volume ids
            - show_surface_ids (bool): Show surface ids
            - show_line_ids (bool): Show line ids
            - show_point_ids (bool): Show point ids
            - ax (mpl_toolkits.mplot3d.axes3d.Axes3D): Axes object to which the volume is added

        """
        # initialize list of surface centroids which are required to plot the surface ids
        all_surface_centroids = []
        all_go_surfaces = []

        # loop over all surfaces within the volume
        for surface_k in volume.surface_ids:
            # get current surface
            surface = geometry.surfaces[abs(surface_k)]

            surface_centroid, go_surface = PlotUtils.__add_3d_surface_to_plot(geometry, surface, show_surface_ids,
                                                                              show_line_ids, show_point_ids, ax)
            all_surface_centroids.append(surface_centroid)
            all_go_surfaces.append(go_surface)

        return all_surface_centroids, all_go_surfaces

        # show volume ids
        if show_volume_ids:
            volume_centroid = np.mean(all_surface_centroids, axis=0)
            ax.text(volume_centroid[0],
                    volume_centroid[1],
                    volume_centroid[2],
                    f"v_{volume.id}",
                    color='black',
                    fontsize=14,
                    fontweight='bold')

    @staticmethod
    def create_geometry_figure(ndim: int,
                               geometry: 'Geometry',
                               show_volume_ids: bool = False,
                               show_surface_ids: bool = False,
                               show_line_ids: bool = False,
                               show_point_ids: bool = False) -> plt.Figure:
        """
        Creates the geometry of the model in a matplotlib plot.

        Args:
            - ndim (int): Number of dimensions of the geometry. Either 2 or 3.
            - geometry (:class:`stem.geometry.Geometry`): Geometry object.
            - show_volume_ids (bool): If True, the volume ids are shown in the plot.
            - show_surface_ids (bool): If True, the surface ids are shown in the plot.
            - show_line_ids (bool): If True, the line ids are shown in the plot.
            - show_point_ids (bool): If True, the point ids are shown in the plot.

        Returns:
            - plt.Figure: Figure object

        """

        import plotly.graph_objects as go

        # Initialize figure in 3D
        fig = plt.figure()

        if ndim == 2:
            ax = fig.add_subplot(111)
            for surface in geometry.surfaces.values():

                a = 1 + 1

                PlotUtils.__add_2d_surface_to_plot(geometry, surface, show_surface_ids, show_line_ids, show_point_ids,
                                                   ax)

        elif ndim == 3:
            all_data = []
            all_go_surfaces = []
            ax = fig.add_subplot(111, projection='3d')
            # loop over all volumes
            for volume_data in geometry.volumes.values():

                a = 1 + 1
                data, go_surfaces = PlotUtils.__add_3d_volume_to_plot(geometry, volume_data, show_volume_ids,
                                                                      show_surface_ids, show_line_ids, show_point_ids,
                                                                      ax)
                all_data.extend(data)
                all_go_surfaces.extend(go_surfaces)
        else:
            raise ValueError("Number of dimensions should be 2 or 3")

        fig.clear()
        # layout = go.Layout(scene=dict(aspectmode="cube"))
        fig = go.FigureWidget()

        for trace in all_data:
            fig.add_trace(trace)
            fig.add_trace(
                go.Scatter3d(x=trace.x, y=trace.y, z=trace.z, mode='text', text="<b>test</b>", textfont=dict(size=18)))
            help(fig.data[-1].on_click)  #(lambda x: print("click"))

        # f = go.FigureWidget([go.Scatter3d(x=[2.5], y=[5], z=[0], mode='text', text="<b>test_surf</b>")])
        # help(f.data[0].on_click)
        fig.add_trace(go.Scatter3d(x=[2.5], y=[5], z=[0], mode='text', text="<b>test_surf</b>"))

        # help(fig.data[0].on_click(lambda x: print("click"))
        # fig.layout

        # for go_surface in all_go_surfaces:
        #     fig.add_trace(go_surface)
        # fig.show()
        #
        # # set limits of plot
        # # extend limits with buffer, which is 10% of the difference between min and max
        # buffer = 0.1
        # all_coordinates = np.array([point.coordinates for point in geometry.points.values()])
        #
        # # calculate and set x and y limits
        # min_x, max_x = np.min(all_coordinates[:, 0]), np.max(all_coordinates[:, 0])
        # dx = max_x - min_x
        # min_y, max_y = np.min(all_coordinates[:, 1]), np.max(all_coordinates[:, 1])
        # dy = max_y - min_y
        #
        # xlim = [min_x - buffer * dx, max_x + buffer * dx]
        # ylim = [min_y - buffer * dy, max_y + buffer * dy]
        #
        # ax.set_xlim(xlim)
        # ax.set_ylim(ylim)
        #
        # # set x and y labels
        # ax.set_xlabel("x coordinates [m]")
        # ax.set_ylabel("y coordinates [m]")
        #
        # if ndim == 3:
        #     # calculate and set z limits
        #     min_z, max_z = np.min(all_coordinates[:, 2]), np.max(all_coordinates[:, 2])
        #     dz = max_z - min_z
        #
        #     zlim = [min_z - buffer * dz, max_z + buffer * dz]
        #
        #     ax.set_zlim(zlim)
        #
        #     # set z label
        #     ax.set_zlabel("z coordinates [m]")
        #
        # # set equal aspect ratio to equal axes
        # ax.set_aspect('equal')
        #
        # import plotly.graph_objs as go
        # from plotly.subplots import make_subplots
        # import plotly.tools as tls
        #
        # # Convert the Matplotlib figure to a Plotly figure
        # plotly_fig = tls.mpl_to_plotly(fig)
        # # plotly_fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'surface'}]])
        # # plotly_fig.add_trace(go.Scatter3d(x=ax.get_proj().proj3d.vertices[0],
        # #                                   y=ax.get_proj().proj3d.vertices[1],
        # #                                   z=ax.get_proj().proj3d.vertices[2],
        # #                                   mode='markers', marker=dict(size=0)),
        # #                      row=1, col=1)
        # #
        # # # Save the Plotly figure as an HTML file
        # # plotly_fig.update_layout(scene=dict(aspectmode='data'))
        # plotly_fig.write_html('3d_plot.html')

        return fig


if __name__ == '__main__':
    import plotly.graph_objects as go

    # Create data for your 3D mesh plot
    # Example data
    x = [0, 1, 2, 3]
    y = [0, 1, 2, 3]
    z = [[1, 2, 1, 2], [2, 3, 2, 3], [3, 4, 3, 4], [4, 5, 4, 5]]

    # Create the 3D mesh plot
    fig = go.Figure()

    # Add the 3D mesh plot
    fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.7))

    # # Add planes on the x-y, x-z, and y-z planes
    # fig.add_trace(go.Surface(x=x, y=y, z=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], colorscale='viridis',
    #                          showscale=False))
    # fig.add_trace(go.Surface(x=x, y=[0, 0, 0, 0], z=z, colorscale='viridis', showscale=False))
    # fig.add_trace(go.Surface(x=[0, 0, 0, 0], y=y, z=z, colorscale='viridis', showscale=False))

    # Customize the layout if needed
    fig.update_layout(scene=dict(
        xaxis=dict(nticks=4),
        yaxis=dict(nticks=4),
        zaxis=dict(nticks=4),
    ))

    # Show the figure
    fig.show()
