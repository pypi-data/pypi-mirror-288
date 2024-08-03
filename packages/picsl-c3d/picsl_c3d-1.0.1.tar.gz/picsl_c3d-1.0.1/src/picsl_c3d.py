import picsl_c3d_internal as ci
import SimpleITK as sitk
import numpy as np

class Convert3D:

    def __init__(self, dim=3):
        """Construct a Convert3D (or 2D/4D) interface.

           Parameters:
               dim:   Number of image dimensions (default=3)
        """
        self.dim = dim
        if self.dim == 3:
            self.api = ci.Convert3D()

    def execute(self, command):
        self.api.execute(command)


    def add_image(self, variable, image:sitk.Image):
        arr = sitk.GetArrayFromImage(image).astype(np.float64, copy=False)
        md = { k : image.GetMetaData(k) for k in image.GetMetaDataKeys() }
        z = ci.ImageImport(arr, 1, image.GetSpacing(), image.GetOrigin(), image.GetDirection(), md)
        self.api.add_image(variable, z)



# if __name__ == "__main__":
#     pass
