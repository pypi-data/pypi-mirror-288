
/*
*  nestml_4e25f2bec0a14a48b0e86ed0d502e0ac_module.cpp
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
*  2024-04-04 08:52:41.794885
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "iaf_psc_delta_nestml.h"

#include "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml.h"


#include "neuromodulated_stdp_nestml__with_iaf_psc_delta_nestml.h"


class nestml_4e25f2bec0a14a48b0e86ed0d502e0ac_module : public nest::NESTExtensionInterface
{
  public:
    nestml_4e25f2bec0a14a48b0e86ed0d502e0ac_module() {}
    ~nestml_4e25f2bec0a14a48b0e86ed0d502e0ac_module() {}

    void initialize() override;
};

nestml_4e25f2bec0a14a48b0e86ed0d502e0ac_module nestml_4e25f2bec0a14a48b0e86ed0d502e0ac_module_LTX_module;

void nestml_4e25f2bec0a14a48b0e86ed0d502e0ac_module::initialize()
{
    // register neurons
    register_iaf_psc_delta_nestml("iaf_psc_delta_nestml");
    register_iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml("iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml");
    // register synapses
    nest::register_neuromodulated_stdp_nestml__with_iaf_psc_delta_nestml( "neuromodulated_stdp_nestml__with_iaf_psc_delta_nestml" );
}
