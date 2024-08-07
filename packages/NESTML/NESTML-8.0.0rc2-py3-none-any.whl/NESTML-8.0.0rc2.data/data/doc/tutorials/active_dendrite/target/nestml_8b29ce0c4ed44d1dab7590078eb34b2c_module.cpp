
/*
*  nestml_8b29ce0c4ed44d1dab7590078eb34b2c_module.cpp
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
*  2024-04-04 10:25:00.194824
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "iaf_psc_exp_active_dendrite_nestml.h"



class nestml_8b29ce0c4ed44d1dab7590078eb34b2c_module : public nest::NESTExtensionInterface
{
  public:
    nestml_8b29ce0c4ed44d1dab7590078eb34b2c_module() {}
    ~nestml_8b29ce0c4ed44d1dab7590078eb34b2c_module() {}

    void initialize() override;
};

nestml_8b29ce0c4ed44d1dab7590078eb34b2c_module nestml_8b29ce0c4ed44d1dab7590078eb34b2c_module_LTX_module;

void nestml_8b29ce0c4ed44d1dab7590078eb34b2c_module::initialize()
{
    // register neurons
    register_iaf_psc_exp_active_dendrite_nestml("iaf_psc_exp_active_dendrite_nestml");
}
