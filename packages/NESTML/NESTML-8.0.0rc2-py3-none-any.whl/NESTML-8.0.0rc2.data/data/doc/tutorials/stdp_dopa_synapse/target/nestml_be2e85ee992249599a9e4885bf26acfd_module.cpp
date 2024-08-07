
/*
*  nestml_be2e85ee992249599a9e4885bf26acfd_module.cpp
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
*  2024-04-04 08:53:10.484405
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "iaf_psc_exp_nestml.h"

#include "iaf_psc_exp_nestml__with_neuromodulated_stdp_nestml.h"


#include "neuromodulated_stdp_nestml__with_iaf_psc_exp_nestml.h"


class nestml_be2e85ee992249599a9e4885bf26acfd_module : public nest::NESTExtensionInterface
{
  public:
    nestml_be2e85ee992249599a9e4885bf26acfd_module() {}
    ~nestml_be2e85ee992249599a9e4885bf26acfd_module() {}

    void initialize() override;
};

nestml_be2e85ee992249599a9e4885bf26acfd_module nestml_be2e85ee992249599a9e4885bf26acfd_module_LTX_module;

void nestml_be2e85ee992249599a9e4885bf26acfd_module::initialize()
{
    // register neurons
    register_iaf_psc_exp_nestml("iaf_psc_exp_nestml");
    register_iaf_psc_exp_nestml__with_neuromodulated_stdp_nestml("iaf_psc_exp_nestml__with_neuromodulated_stdp_nestml");
    // register synapses
    nest::register_neuromodulated_stdp_nestml__with_iaf_psc_exp_nestml( "neuromodulated_stdp_nestml__with_iaf_psc_exp_nestml" );
}
