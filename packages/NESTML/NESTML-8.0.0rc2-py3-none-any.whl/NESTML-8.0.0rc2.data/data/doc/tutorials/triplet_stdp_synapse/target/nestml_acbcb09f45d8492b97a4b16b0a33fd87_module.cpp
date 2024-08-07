
/*
*  nestml_acbcb09f45d8492b97a4b16b0a33fd87_module.cpp
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
*  2024-04-04 09:02:26.870348
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "iaf_psc_delta_nestml.h"

#include "iaf_psc_delta_nestml__with_stdp_triplet_nn_nestml.h"


#include "stdp_triplet_nn_nestml__with_iaf_psc_delta_nestml.h"


class nestml_acbcb09f45d8492b97a4b16b0a33fd87_module : public nest::NESTExtensionInterface
{
  public:
    nestml_acbcb09f45d8492b97a4b16b0a33fd87_module() {}
    ~nestml_acbcb09f45d8492b97a4b16b0a33fd87_module() {}

    void initialize() override;
};

nestml_acbcb09f45d8492b97a4b16b0a33fd87_module nestml_acbcb09f45d8492b97a4b16b0a33fd87_module_LTX_module;

void nestml_acbcb09f45d8492b97a4b16b0a33fd87_module::initialize()
{
    // register neurons
    register_iaf_psc_delta_nestml("iaf_psc_delta_nestml");
    register_iaf_psc_delta_nestml__with_stdp_triplet_nn_nestml("iaf_psc_delta_nestml__with_stdp_triplet_nn_nestml");
    // register synapses
    nest::register_stdp_triplet_nn_nestml__with_iaf_psc_delta_nestml( "stdp_triplet_nn_nestml__with_iaf_psc_delta_nestml" );
}
