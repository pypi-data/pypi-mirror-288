
/*
 *  nestml_f63dc1278f7b473ca66e84e1fbfca8ee_module.h
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
 *  2024-02-22 12:54:35.049714
 */

#ifndef NESTML_F63DC1278F7B473CA66E84E1FBFCA8EE_MODULE_H
#define NESTML_F63DC1278F7B473CA66E84E1FBFCA8EE_MODULE_H

#include "slimodule.h"
#include "slifunction.h"

#include "nest.h"
#include "nest_impl.h"


/**
* Class defining your model.
* @note For each model, you must define one such class, with a unique name.
*/
class nestml_f63dc1278f7b473ca66e84e1fbfca8ee_module : public SLIModule
{
public:
  // Interface functions ------------------------------------------

  /**
   * @note The constructor registers the module with the dynamic loader.
   *       Initialization proper is performed by the init() method.
   */
  nestml_f63dc1278f7b473ca66e84e1fbfca8ee_module();

  /**
   * @note The destructor does not do much in modules.
   */
  ~nestml_f63dc1278f7b473ca66e84e1fbfca8ee_module();

  /**
   * Initialize module by registering models with the network.
   * @param SLIInterpreter* SLI interpreter
   */
  void init( SLIInterpreter* );

  /**
   * Return the name of your model.
   */
  const std::string name() const;

public:
  // Classes implementing your functions -----------------------------

};

#endif