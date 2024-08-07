// #define DEBUG 1
/*
 *  inhomogeneous_poisson_neuron_nestml.cpp
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
 *  Generated from NESTML at time: 2024-04-23 11:56:24.526802
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

#include "inhomogeneous_poisson_neuron_nestml.h"
void
register_inhomogeneous_poisson_neuron_nestml( const std::string& name )
{
  nest::register_node_model< inhomogeneous_poisson_neuron_nestml >( name );
}

// ---------------------------------------------------------------------------
//   Recordables map
// ---------------------------------------------------------------------------
nest::RecordablesMap<inhomogeneous_poisson_neuron_nestml> inhomogeneous_poisson_neuron_nestml::recordablesMap_;
namespace nest
{

  // Override the create() method with one call to RecordablesMap::insert_()
  // for each quantity to be recorded.
template <> void RecordablesMap<inhomogeneous_poisson_neuron_nestml>::create()
  {
    // add state variables to recordables map
   insert_(inhomogeneous_poisson_neuron_nestml_names::_dt_next_spike, &inhomogeneous_poisson_neuron_nestml::get_dt_next_spike);
   insert_(inhomogeneous_poisson_neuron_nestml_names::_t_last_spike, &inhomogeneous_poisson_neuron_nestml::get_t_last_spike);

    // Add vector variables  
  }
}

// ---------------------------------------------------------------------------
//   Default constructors defining default parameters and state
//   Note: the implementation is empty. The initialization is of variables
//   is a part of inhomogeneous_poisson_neuron_nestml's constructor.
// ---------------------------------------------------------------------------

inhomogeneous_poisson_neuron_nestml::Parameters_::Parameters_()
{
}

inhomogeneous_poisson_neuron_nestml::State_::State_()
{
}

// ---------------------------------------------------------------------------
//   Parameter and state extractions and manipulation functions
// ---------------------------------------------------------------------------

inhomogeneous_poisson_neuron_nestml::Buffers_::Buffers_(inhomogeneous_poisson_neuron_nestml &n):
  logger_(n)
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

inhomogeneous_poisson_neuron_nestml::Buffers_::Buffers_(const Buffers_ &, inhomogeneous_poisson_neuron_nestml &n):
  logger_(n)
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

// ---------------------------------------------------------------------------
//   Default constructor for node
// ---------------------------------------------------------------------------

inhomogeneous_poisson_neuron_nestml::inhomogeneous_poisson_neuron_nestml():StructuralPlasticityNode(), P_(), S_(), B_(*this)
{
  init_state_internal_();
  recordablesMap_.create();
  pre_run_hook();
}

// ---------------------------------------------------------------------------
//   Copy constructor for node
// ---------------------------------------------------------------------------

inhomogeneous_poisson_neuron_nestml::inhomogeneous_poisson_neuron_nestml(const inhomogeneous_poisson_neuron_nestml& __n):
  StructuralPlasticityNode(), P_(__n.P_), S_(__n.S_), B_(__n.B_, *this)
{

  // copy parameter struct P_
  P_.N = __n.P_.N;
  P_.rate_times = __n.P_.rate_times;
  P_.rate_values = __n.P_.rate_values;

  // copy state struct S_
  S_.idx = __n.S_.idx;
  S_.dt_next_spike = __n.S_.dt_next_spike;
  S_.t_last_spike = __n.S_.t_last_spike;

  // copy internals V_
  V_.__h = __n.V_.__h;
}

// ---------------------------------------------------------------------------
//   Destructor for node
// ---------------------------------------------------------------------------

inhomogeneous_poisson_neuron_nestml::~inhomogeneous_poisson_neuron_nestml()
{
}

// ---------------------------------------------------------------------------
//   Node initialization functions
// ---------------------------------------------------------------------------
void inhomogeneous_poisson_neuron_nestml::calibrate_time( const nest::TimeConverter& tc )
{
  LOG( nest::M_WARNING,
    "inhomogeneous_poisson_neuron_nestml",
    "Simulation resolution has changed. Internal state and parameters of the model have been reset!" );

  init_state_internal_();
}
void inhomogeneous_poisson_neuron_nestml::init_state_internal_()
{
#ifdef DEBUG
  std::cout << "inhomogeneous_poisson_neuron_nestml::init_state_internal_()" << std::endl;
#endif

  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  pre_run_hook();
  // initial values for parameters
  P_.N = 1; // as integer
  P_.rate_times.resize(
  P_.N, 0);
  P_.rate_values.resize(
  P_.N, (0.001 * (pow(0 * 1000.0, (-1)))));

  V_.__h = nest::Time::get_resolution().get_ms();
  recompute_internal_variables();
  // initial values for state variables
  S_.idx = 0; // as integer
  S_.dt_next_spike = (-1); // as ms
  S_.t_last_spike = 0; // as ms
}

void inhomogeneous_poisson_neuron_nestml::init_buffers_()
{
#ifdef DEBUG
  std::cout << "inhomogeneous_poisson_neuron_nestml::init_buffers_()" << std::endl;
#endif

  B_.logger_.reset();


}

void inhomogeneous_poisson_neuron_nestml::recompute_internal_variables(bool exclude_timestep)
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  if (exclude_timestep)
  {    
  }
  else {    
    V_.__h = __resolution; // as ms
  }
}
void inhomogeneous_poisson_neuron_nestml::pre_run_hook()
{
  B_.logger_.init();

  // parameters might have changed -- recompute internals
  V_.__h = nest::Time::get_resolution().get_ms();
  recompute_internal_variables();

  // buffers B_
}

// ---------------------------------------------------------------------------
//   Update and spike handling functions
// ---------------------------------------------------------------------------


void inhomogeneous_poisson_neuron_nestml::update(nest::Time const & origin,const long from, const long to)
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  for ( long lag = from ; lag < to ; ++lag )
  {


    auto get_t = [origin, lag](){ return nest::Time( nest::Time::step( origin.get_steps() + lag + 1) ).get_ms(); };
    /**
     * buffer spikes from spiking input ports
    **/

    for (long i = 0; i < NUM_SPIKE_RECEPTORS; ++i)
    {
      get_spike_inputs_grid_sum_()[i] = get_spike_inputs_()[i].get_value(lag);
      get_spike_input_received_grid_sum_()[i] = get_spike_input_received_()[i].get_value(lag);
    }

    /**
     * subthreshold updates of the convolution variables
     *
     * step 1: regardless of whether and how integrate_odes() will be called, update variables due to convolutions
    **/


    /**
     * Begin NESTML generated code for the update block(s)
    **/

    if (P_.N > 0)
    {  
        while ( S_.idx < P_.N - 1 && get_t() >= P_.rate_times[S_.idx + 1])
        {
          S_.idx += 1;
        }
    }
    double rate = P_.rate_values[S_.idx];
    long n_spikes_in_this_timestep = ([&]() -> int { nest::poisson_distribution::param_type poisson_params(rate * __resolution * 0.001); int sample = poisson_dev_( nest::get_vp_specific_rng( get_thread() ), poisson_params); return sample; })();
    if (n_spikes_in_this_timestep > 0)
    {  

        /**
         * generated code for emit_spike() function
        **/

        set_spiketime(nest::Time::step(origin.get_steps() + lag + 1));
        nest::SpikeEvent se;
        nest::kernel().event_delivery_manager.send(*this, se, lag);


    }

    /**
     * Begin NESTML generated code for the onReceive block(s)
    **/


    /**
     * subthreshold updates of the convolution variables
     *
     * step 2: regardless of whether and how integrate_odes() was called, update variables due to convolutions. Set to the updated values at the end of the timestep.
    **/



    /**
     * spike updates due to convolutions
    **/


    /**
     * Begin NESTML generated code for the onCondition block(s)
    **/


    /**
     * handle continuous input ports
    **/
    // voltage logging
    B_.logger_.record_data(origin.get_steps() + lag);
  }
}

// Do not move this function as inline to h-file. It depends on
// universal_data_logger_impl.h being included here.
void inhomogeneous_poisson_neuron_nestml::handle(nest::DataLoggingRequest& e)
{
  B_.logger_.handle(e);
}



// -------------------------------------------------------------------------
//   Methods corresponding to event handlers
// -------------------------------------------------------------------------

