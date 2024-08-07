
/*
*  nestml_b280cf0e37cb42229a3d906ed76e4903_module.cpp
*
*  This file is part of NEST.
*
*  Copyright (C) 2004 The NEST Initiative
*
*  NEST is free software: you can redistribute it and/or modify
*  it under the terms of the GNU General Public License as published by
*  the Free Software Foundation, either version 2 of the License, or
*  (at your option) any later version.
*
*  NEST is distributed in the hope that it will be useful,
*  but WITHOUT ANY WARRANTY; without even the implied warranty of
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*  GNU General Public License for more details.
*
*  You should have received a copy of the GNU General Public License
*  along with NEST.  If not, see <http://www.gnu.org/licenses/>.
*
*  2024-04-04 08:45:27.768240
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "ornstein_uhlenbeck_noise_nestml.h"



class nestml_b280cf0e37cb42229a3d906ed76e4903_module : public nest::NESTExtensionInterface
{
  public:
    nestml_b280cf0e37cb42229a3d906ed76e4903_module() {}
    ~nestml_b280cf0e37cb42229a3d906ed76e4903_module() {}

    void initialize() override;
};

nestml_b280cf0e37cb42229a3d906ed76e4903_module nestml_b280cf0e37cb42229a3d906ed76e4903_module_LTX_module;

void nestml_b280cf0e37cb42229a3d906ed76e4903_module::initialize()
{
    // register neurons
    register_ornstein_uhlenbeck_noise_nestml("ornstein_uhlenbeck_noise_nestml");
}
