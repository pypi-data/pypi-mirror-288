
/*
*  nestml_eab8ac23ecaa400a83d400775e1006e6_module.cpp
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
*  2024-03-20 10:29:17.561034
*/

// Include from NEST
#include "nest_extension_interface.h"

// include headers with your own stuff


#include "gl_expeab8ac23ecaa400a83d400775e1006e6_nestml.h"



class nestml_eab8ac23ecaa400a83d400775e1006e6_module : public nest::NESTExtensionInterface
{
  public:
    nestml_eab8ac23ecaa400a83d400775e1006e6_module() {}
    ~nestml_eab8ac23ecaa400a83d400775e1006e6_module() {}

    void initialize() override;
};

nestml_eab8ac23ecaa400a83d400775e1006e6_module nestml_eab8ac23ecaa400a83d400775e1006e6_module_LTX_module;

void nestml_eab8ac23ecaa400a83d400775e1006e6_module::initialize()
{
    // register neurons
    register_gl_expeab8ac23ecaa400a83d400775e1006e6_nestml("gl_expeab8ac23ecaa400a83d400775e1006e6_nestml");
}
