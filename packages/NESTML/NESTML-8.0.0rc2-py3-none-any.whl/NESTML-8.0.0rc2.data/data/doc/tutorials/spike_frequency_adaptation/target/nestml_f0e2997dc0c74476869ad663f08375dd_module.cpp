
/*
*  nestml_f0e2997dc0c74476869ad663f08375dd_module.cpp
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
*  2024-04-04 08:47:52.316169
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "iaf_psc_alpha_nestml.h"



class nestml_f0e2997dc0c74476869ad663f08375dd_module : public nest::NESTExtensionInterface
{
  public:
    nestml_f0e2997dc0c74476869ad663f08375dd_module() {}
    ~nestml_f0e2997dc0c74476869ad663f08375dd_module() {}

    void initialize() override;
};

nestml_f0e2997dc0c74476869ad663f08375dd_module nestml_f0e2997dc0c74476869ad663f08375dd_module_LTX_module;

void nestml_f0e2997dc0c74476869ad663f08375dd_module::initialize()
{
    // register neurons
    register_iaf_psc_alpha_nestml("iaf_psc_alpha_nestml");
}
