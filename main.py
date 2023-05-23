import sys


from plot_x_col_scatter import plot_x_col_scatter
from plot_x_col_mesh_ckdtree import plot_x_col_mesh_ckdtree
from plot_x_col_mesh_kriging import plot_x_col_mesh_kriging


def main():
    pass

    print("Generating scatter plot ...")
    plot_x_col_scatter()

    print("Generating plots using spacial interpolation within 3 degrees ...")
    plot_x_col_mesh_ckdtree(max_distance_degrees=3.0)

    print("Generating plots using spacial interpolation within 4 degrees ...")
    plot_x_col_mesh_ckdtree(max_distance_degrees=4.0)

    print("Generating plots using spacial interpolation within 5 degrees ...")
    plot_x_col_mesh_ckdtree(max_distance_degrees=5.0)
    
    # this is very slow
    # plot_x_col_mesh_kriging()


if __name__ == "__main__":
    sys.exit(main())
