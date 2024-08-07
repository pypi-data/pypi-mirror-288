
/*
*  nestml_10398c41b2f148ba8d1959fb09850455_module.cpp
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
*  2024-04-04 10:21:11.543185
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "izhikevich_tutorial_nestml.h"



class nestml_10398c41b2f148ba8d1959fb09850455_module : public nest::NESTExtensionInterface
{
  public:
    nestml_10398c41b2f148ba8d1959fb09850455_module() {}
    ~nestml_10398c41b2f148ba8d1959fb09850455_module() {}

    void initialize() override;
};

nestml_10398c41b2f148ba8d1959fb09850455_module nestml_10398c41b2f148ba8d1959fb09850455_module_LTX_module;

void nestml_10398c41b2f148ba8d1959fb09850455_module::initialize()
{
    // register neurons
    register_izhikevich_tutorial_nestml("izhikevich_tutorial_nestml");
}
