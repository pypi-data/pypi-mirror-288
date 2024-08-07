
/*
*  nestml_4561330a8a084c6e9d8a8a9daa7b17a8_module.cpp
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
*  2024-06-03 15:14:04.859062
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "iaf_psc_delta_neuron_nestml.h"

#include "iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml.h"


#include "neuromodulated_stdp_synapse_nestml__with_iaf_psc_delta_neuron_nestml.h"


class nestml_4561330a8a084c6e9d8a8a9daa7b17a8_module : public nest::NESTExtensionInterface
{
  public:
    nestml_4561330a8a084c6e9d8a8a9daa7b17a8_module() {}
    ~nestml_4561330a8a084c6e9d8a8a9daa7b17a8_module() {}

    void initialize() override;
};

nestml_4561330a8a084c6e9d8a8a9daa7b17a8_module nestml_4561330a8a084c6e9d8a8a9daa7b17a8_module_LTX_module;

void nestml_4561330a8a084c6e9d8a8a9daa7b17a8_module::initialize()
{
    // register neurons
    register_iaf_psc_delta_neuron_nestml("iaf_psc_delta_neuron_nestml");
    register_iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml("iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml");
    // register synapses
    nest::register_neuromodulated_stdp_synapse_nestml__with_iaf_psc_delta_neuron_nestml( "neuromodulated_stdp_synapse_nestml__with_iaf_psc_delta_neuron_nestml" );
}
