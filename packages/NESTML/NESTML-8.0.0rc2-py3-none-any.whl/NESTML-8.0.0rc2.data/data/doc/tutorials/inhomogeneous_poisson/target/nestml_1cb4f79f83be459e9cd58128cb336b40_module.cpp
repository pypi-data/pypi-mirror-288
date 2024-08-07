
/*
*  nestml_1cb4f79f83be459e9cd58128cb336b40_module.cpp
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
*  2024-04-23 11:56:24.944832
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "inhomogeneous_poisson_neuron_nestml.h"



class nestml_1cb4f79f83be459e9cd58128cb336b40_module : public nest::NESTExtensionInterface
{
  public:
    nestml_1cb4f79f83be459e9cd58128cb336b40_module() {}
    ~nestml_1cb4f79f83be459e9cd58128cb336b40_module() {}

    void initialize() override;
};

nestml_1cb4f79f83be459e9cd58128cb336b40_module nestml_1cb4f79f83be459e9cd58128cb336b40_module_LTX_module;

void nestml_1cb4f79f83be459e9cd58128cb336b40_module::initialize()
{
    // register neurons
    register_inhomogeneous_poisson_neuron_nestml("inhomogeneous_poisson_neuron_nestml");
}
