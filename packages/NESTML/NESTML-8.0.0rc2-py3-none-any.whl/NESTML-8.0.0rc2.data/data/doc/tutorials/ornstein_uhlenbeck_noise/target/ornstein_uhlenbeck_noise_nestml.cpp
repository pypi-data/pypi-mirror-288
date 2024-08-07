// #define DEBUG 1
/*
 *  ornstein_uhlenbeck_noise_nestml.cpp
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
 *  Generated from NESTML at time: 2024-04-04 08:45:27.444262
**/

// C++ includes:
#include <limits>

// Includes from libnestutil:
#include "numerics.h"

// Includes from nestkernel:
#include "exceptions.h"
#include "kernel_manager.h"
#include "nest_impl.h"
#include "universal_data_logger_impl.h"

// Includes from sli:
#include "dict.h"
#include "dictutils.h"
#include "doubledatum.h"
#include "integerdatum.h"
#include "lockptrdatum.h"

#include "ornstein_uhlenbeck_noise_nestml.h"
void
register_ornstein_uhlenbeck_noise_nestml( const std::string& name )
{
  nest::register_node_model< ornstein_uhlenbeck_noise_nestml >( name );
}

// ---------------------------------------------------------------------------
//   Recordables map
// ---------------------------------------------------------------------------
nest::RecordablesMap<ornstein_uhlenbeck_noise_nestml> ornstein_uhlenbeck_noise_nestml::recordablesMap_;
namespace nest
{

  // Override the create() method with one call to RecordablesMap::insert_()
  // for each quantity to be recorded.
template <> void RecordablesMap<ornstein_uhlenbeck_noise_nestml>::create()
  {
    // add state variables to recordables map
   insert_(ornstein_uhlenbeck_noise_nestml_names::_U, &ornstein_uhlenbeck_noise_nestml::get_U);

    // Add vector variables  
  }
}

// ---------------------------------------------------------------------------
//   Default constructors defining default parameters and state
//   Note: the implementation is empty. The initialization is of variables
//   is a part of ornstein_uhlenbeck_noise_nestml's constructor.
// ---------------------------------------------------------------------------

ornstein_uhlenbeck_noise_nestml::Parameters_::Parameters_()
{
}

ornstein_uhlenbeck_noise_nestml::State_::State_()
{
}

// ---------------------------------------------------------------------------
//   Parameter and state extractions and manipulation functions
// ---------------------------------------------------------------------------

ornstein_uhlenbeck_noise_nestml::Buffers_::Buffers_(ornstein_uhlenbeck_noise_nestml &n):
  logger_(n)
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

ornstein_uhlenbeck_noise_nestml::Buffers_::Buffers_(const Buffers_ &, ornstein_uhlenbeck_noise_nestml &n):
  logger_(n)
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

// ---------------------------------------------------------------------------
//   Default constructor for node
// ---------------------------------------------------------------------------

ornstein_uhlenbeck_noise_nestml::ornstein_uhlenbeck_noise_nestml():StructuralPlasticityNode(), P_(), S_(), B_(*this)
{
  init_state_internal_();
  recordablesMap_.create();
  pre_run_hook();
}

// ---------------------------------------------------------------------------
//   Copy constructor for node
// ---------------------------------------------------------------------------

ornstein_uhlenbeck_noise_nestml::ornstein_uhlenbeck_noise_nestml(const ornstein_uhlenbeck_noise_nestml& __n):
  StructuralPlasticityNode(), P_(__n.P_), S_(__n.S_), B_(__n.B_, *this) {

  // copy parameter struct P_
  P_.mean_noise = __n.P_.mean_noise;
  P_.sigma_noise = __n.P_.sigma_noise;
  P_.tau_noise = __n.P_.tau_noise;

  // copy state struct S_
  S_.U = __n.S_.U;

  // copy internals V_
  V_.A_noise = __n.V_.A_noise;
}

// ---------------------------------------------------------------------------
//   Destructor for node
// ---------------------------------------------------------------------------

ornstein_uhlenbeck_noise_nestml::~ornstein_uhlenbeck_noise_nestml()
{
}

// ---------------------------------------------------------------------------
//   Node initialization functions
// ---------------------------------------------------------------------------
void ornstein_uhlenbeck_noise_nestml::calibrate_time( const nest::TimeConverter& tc )
{
  LOG( nest::M_WARNING,
    "ornstein_uhlenbeck_noise_nestml",
    "Simulation resolution has changed. Internal state and parameters of the model have been reset!" );

  init_state_internal_();
}
void ornstein_uhlenbeck_noise_nestml::init_state_internal_()
{
#ifdef DEBUG
  std::cout << "ornstein_uhlenbeck_noise_nestml::init_state_internal_()" << std::endl;
#endif

  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  // initial values for parameters
    

    P_.mean_noise = 500; // as real
    

    P_.sigma_noise = 50; // as real
    

    P_.tau_noise = 20; // as ms

  recompute_internal_variables();
  // initial values for state variables
    

    S_.U = P_.mean_noise; // as real
}

void ornstein_uhlenbeck_noise_nestml::init_buffers_()
{
#ifdef DEBUG
  std::cout << "ornstein_uhlenbeck_noise_nestml::init_buffers_()" << std::endl;
#endif

  B_.logger_.reset();


}

void ornstein_uhlenbeck_noise_nestml::recompute_internal_variables(bool exclude_timestep) {
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  if (exclude_timestep) {    
      

      V_.A_noise = P_.sigma_noise * pow(((1 - std::exp((-2) * __resolution / P_.tau_noise))), 0.5); // as real
  }
  else {    
      

      V_.A_noise = P_.sigma_noise * pow(((1 - std::exp((-2) * __resolution / P_.tau_noise))), 0.5); // as real
  }
}
void ornstein_uhlenbeck_noise_nestml::pre_run_hook() {
  B_.logger_.init();

  // parameters might have changed -- recompute internals
  recompute_internal_variables();

  // buffers B_
}

// ---------------------------------------------------------------------------
//   Update and spike handling functions
// ---------------------------------------------------------------------------


void ornstein_uhlenbeck_noise_nestml::update(nest::Time const & origin,const long from, const long to)
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function



  for ( long lag = from ; lag < to ; ++lag )
  {
    auto get_t = [origin, lag](){ return nest::Time( nest::Time::step( origin.get_steps() + lag + 1) ).get_ms(); };

    for (long i = 0; i < NUM_SPIKE_RECEPTORS; ++i)
    {
        get_spike_inputs_grid_sum_()[i] = get_spike_inputs_()[i].get_value(lag);
    }

    // NESTML generated code for the update block
  S_.U = P_.mean_noise + (S_.U - P_.mean_noise) * std::exp((-__resolution) / P_.tau_noise) + V_.A_noise * ((0) + (1) * normal_dev_( nest::get_vp_specific_rng( get_thread() ) ));
    // voltage logging
    B_.logger_.record_data(origin.get_steps() + lag);
  }
}

// Do not move this function as inline to h-file. It depends on
// universal_data_logger_impl.h being included here.
void ornstein_uhlenbeck_noise_nestml::handle(nest::DataLoggingRequest& e)
{
  B_.logger_.handle(e);
}



