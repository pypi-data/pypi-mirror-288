/*=========================================================================

  Program:   C3D: Command-line companion tool to ITK-SNAP
  Module:    Convert3DMain.cxx
  Language:  C++
  Website:   itksnap.org/c3d
  Copyright (c) 2024 Paul A. Yushkevich

  This file is part of C3D, a command-line companion tool to ITK-SNAP

  C3D is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

=========================================================================*/
#include <ConvertAPI.h>
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include <iostream>
#include <itkImage.h>
#include <itkImportImageFilter.h>
#include <itkMetaDataObject.h>
namespace py=pybind11;

using Convert3D = ConvertAPI<double, 3>;
using namespace std;

template <typename TPixel, unsigned int VDim>
class ImageImport
{
public:
  using ImageType = itk::Image<TPixel, VDim>;
  using ImportFilterType = itk::ImportImageFilter<TPixel, VDim>;
  using RegionType = typename ImageType::RegionType;
  using SpacingType = typename ImageType::SpacingType;
  using PointType = typename ImageType::PointType;

  ImageImport(py::buffer b, unsigned int ncomp,
              const std::array<double, VDim> &spacing,
              const std::array<double, VDim> &origin,
              const std::array<double, VDim*VDim> &direction,
              const py::dict &metadata);

  std::string GetInfoString() {
    std::ostringstream oss;
    image->Print(oss);
    return oss.str();
  }

  ImageType* GetImage() const { return image; }

private:
  typename ImageType::Pointer image;
};


template <typename TPixel, unsigned int VDim>
ImageImport<TPixel, VDim>
  ::ImageImport(py::buffer b,
                unsigned int ncomp,
                const std::array<double, VDim> &spacing,
                const std::array<double, VDim> &origin,
                const std::array<double, VDim*VDim> &direction,
                const py::dict &metadata)
{
  if(ncomp != 1)
    throw std::runtime_error("Vector images are not supported!");

  py::buffer_info info = b.request();
  if(info.ndim != VDim)
    throw std::runtime_error("Incompatible array dimensions!");

  if (info.format != py::format_descriptor<TPixel>::format())
    throw std::runtime_error("Incompatible format");

  typename ImportFilterType::Pointer import = ImportFilterType::New();
  typename ImageType::RegionType itk_region;
  typename ImageType::SpacingType itk_spacing;
  typename ImageType::PointType itk_origin;
  typename ImageType::DirectionType itk_direction;
  int q = 0;
  for(unsigned int i = 0; i < info.ndim; i++)
  {
    itk_region.SetSize(i, info.shape[i]);
    itk_spacing[i] = spacing[i];
    itk_origin[i] = origin[i];
    for(unsigned int j = 0; j < VDim; j++)
      itk_direction[i][j] = direction[q++];
  }

  import->SetRegion(itk_region);
  import->SetOrigin(itk_origin);
  import->SetSpacing(itk_spacing);
  import->SetDirection(itk_direction);
  import->SetImportPointer(static_cast<TPixel *>(info.ptr), info.size, false);
  import->Update();
  this->image = import->GetOutput();

  // Assign the image metadata
  for (auto item : metadata)
  {
    auto key = std::string(py::str(item.first));
    auto value = std::string(py::str(item.first));
    itk::EncapsulateMetaData<std::string>(this->image->GetMetaDataDictionary(), key.c_str(), value);
  }
}

using MyImageImport = ImageImport<double, 3>;


PYBIND11_MODULE(picsl_c3d_internal, m) {
    py::class_<MyImageImport>(m, "ImageImport", py::buffer_protocol())
        .def(py::init<py::buffer, unsigned int, const std::array<double, 3>, const std::array<double, 3>, const std::array<double, 9>, const py::dict &>())
        .def("__repr__", &MyImageImport::GetInfoString);

    py::class_<Convert3D>(m, "Convert3D", py::buffer_protocol())
        .def(py::init<>())
        .def("execute", &Convert3D::ExecuteWrapper)
        .def("add_image", [](Convert3D &c, const string &var, const MyImageImport &img) {
            c.AddImage(var.c_str(), img.GetImage());
        });

};
