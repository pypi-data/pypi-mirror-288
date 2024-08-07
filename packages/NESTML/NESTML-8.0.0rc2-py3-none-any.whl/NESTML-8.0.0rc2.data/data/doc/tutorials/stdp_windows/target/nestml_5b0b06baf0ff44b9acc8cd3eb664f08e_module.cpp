
/*
*  nestml_5b0b06baf0ff44b9acc8cd3eb664f08e_module.cpp
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
*  2024-04-04 10:26:56.555866
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "iaf_psc_delta_nestml.h"

#include "iaf_psc_delta_nestml__with_stdp_windowed_nestml.h"


#include "stdp_windowed_nestml__with_iaf_psc_delta_nestml.h"


class nestml_5b0b06baf0ff44b9acc8cd3eb664f08e_module : public nest::NESTExtensionInterface
{
  public:
    nestml_5b0b06baf0ff44b9acc8cd3eb664f08e_module() {}
    ~nestml_5b0b06baf0ff44b9acc8cd3eb664f08e_module() {}

    void initialize() override;
};

nestml_5b0b06baf0ff44b9acc8cd3eb664f08e_module nestml_5b0b06baf0ff44b9acc8cd3eb664f08e_module_LTX_module;

void nestml_5b0b06baf0ff44b9acc8cd3eb664f08e_module::initialize()
{
    // register neurons
    register_iaf_psc_delta_nestml("iaf_psc_delta_nestml");
    register_iaf_psc_delta_nestml__with_stdp_windowed_nestml("iaf_psc_delta_nestml__with_stdp_windowed_nestml");
    // register synapses
    nest::register_stdp_windowed_nestml__with_iaf_psc_delta_nestml( "stdp_windowed_nestml__with_iaf_psc_delta_nestml" );
}
