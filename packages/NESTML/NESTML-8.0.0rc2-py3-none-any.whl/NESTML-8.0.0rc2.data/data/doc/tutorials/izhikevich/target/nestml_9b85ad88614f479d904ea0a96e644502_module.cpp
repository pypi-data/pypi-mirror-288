
/*
*  nestml_9b85ad88614f479d904ea0a96e644502_module.cpp
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
*  2024-04-04 10:22:23.208746
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "izhikevich_tutorial_nestml.h"



class nestml_9b85ad88614f479d904ea0a96e644502_module : public nest::NESTExtensionInterface
{
  public:
    nestml_9b85ad88614f479d904ea0a96e644502_module() {}
    ~nestml_9b85ad88614f479d904ea0a96e644502_module() {}

    void initialize() override;
};

nestml_9b85ad88614f479d904ea0a96e644502_module nestml_9b85ad88614f479d904ea0a96e644502_module_LTX_module;

void nestml_9b85ad88614f479d904ea0a96e644502_module::initialize()
{
    // register neurons
    register_izhikevich_tutorial_nestml("izhikevich_tutorial_nestml");
}
