// #define DEBUG 1
/*
 *  gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml.cpp
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
 *  Generated from NESTML at time: 2024-02-26 10:01:23.437028
**/

// C++ includes:
#include <limits>

// Includes from libnestutil:
#include "numerics.h"

// Includes from nestkernel:
#include "exceptions.h"
#include "kernel_manager.h"
#include "universal_data_logger_impl.h"

// Includes from sli:
#include "dict.h"
#include "dictutils.h"
#include "doubledatum.h"
#include "integerdatum.h"
#include "lockptrdatum.h"

#include "gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml.h"

// ---------------------------------------------------------------------------
//   Recordables map
// ---------------------------------------------------------------------------
nest::RecordablesMap<gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml> gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::recordablesMap_;
namespace nest
{

  // Override the create() method with one call to RecordablesMap::insert_()
  // for each quantity to be recorded.
template <> void RecordablesMap<gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml>::create()
  {
    // add state variables to recordables map
   insert_(gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml_names::_U, &gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::get_U);

    // Add vector variables  
  }
}

// ---------------------------------------------------------------------------
//   Default constructors defining default parameters and state
//   Note: the implementation is empty. The initialization is of variables
//   is a part of gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml's constructor.
// ---------------------------------------------------------------------------

gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::Parameters_::Parameters_()
{
}

gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::State_::State_()
{
}

// ---------------------------------------------------------------------------
//   Parameter and state extractions and manipulation functions
// ---------------------------------------------------------------------------

gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::Buffers_::Buffers_(gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::Buffers_::Buffers_(const Buffers_ &, gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

// ---------------------------------------------------------------------------
//   Default constructor for node
// ---------------------------------------------------------------------------

gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml():StructuralPlasticityNode(), P_(), S_(), B_(*this)
{
  init_state_internal_();
  recordablesMap_.create();
  pre_run_hook();
}

// ---------------------------------------------------------------------------
//   Copy constructor for node
// ---------------------------------------------------------------------------

gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml(const gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml& __n):
  StructuralPlasticityNode(), P_(__n.P_), S_(__n.S_), B_(__n.B_, *this) {

  // copy parameter struct P_
  P_.a = __n.P_.a;
  P_.alpha_over_N = __n.P_.alpha_over_N;
  P_.beta = __n.P_.beta;
  P_.reset_after_spike = __n.P_.reset_after_spike;

  // copy state struct S_
  S_.U = __n.S_.U;

  // copy internals V_
  V_.__h = __n.V_.__h;
  V_.__P__U__U = __n.V_.__P__U__U;
}

// ---------------------------------------------------------------------------
//   Destructor for node
// ---------------------------------------------------------------------------

gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::~gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml()
{
}

// ---------------------------------------------------------------------------
//   Node initialization functions
// ---------------------------------------------------------------------------
void gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::calibrate_time( const nest::TimeConverter& tc )
{
  LOG( nest::M_WARNING,
    "gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml",
    "Simulation resolution has changed. Internal state and parameters of the model have been reset!" );

  init_state_internal_();
}
void gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::init_state_internal_()
{
#ifdef DEBUG
  std::cout << "gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::init_state_internal_()" << std::endl;
#endif

  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  // initial values for parameters
    

    P_.a = 3.0; // as real
    

    P_.alpha_over_N = 1.0777744654743957; // as real
    

    P_.beta = 50; // as real
    

    P_.reset_after_spike = true; // as boolean

  recompute_internal_variables();
  // initial values for state variables
    

    S_.U = 0; // as real
}

void gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::init_buffers_()
{
#ifdef DEBUG
  std::cout << "gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::init_buffers_()" << std::endl;
#endif
  // spike input buffers
  get_spike_inputs_().clear();
  get_spike_inputs_grid_sum_().clear();

  B_.logger_.reset();


}

void gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::recompute_internal_variables(bool exclude_timestep) {
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  if (exclude_timestep) {    
      

      V_.__P__U__U = 1.0 * std::exp((-0.001) * V_.__h * P_.beta); // as real
  }
  else {    
      

      V_.__h = __resolution; // as ms
      

      V_.__P__U__U = 1.0 * std::exp((-0.001) * V_.__h * P_.beta); // as real
  }
}
void gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::pre_run_hook() {
  B_.logger_.init();

  // parameters might have changed -- recompute internals
  recompute_internal_variables();

  // buffers B_
  B_.spike_inputs_.resize(NUM_SPIKE_RECEPTORS);
  B_.spike_inputs_grid_sum_.resize(NUM_SPIKE_RECEPTORS);
}

// ---------------------------------------------------------------------------
//   Functions defined in the NESTML model
// ---------------------------------------------------------------------------

//
double gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::phi ( double U) const
{  
  if (U <= 0)
  {  
    return 0;
  }
  return (4 * P_.a) / (1 + std::exp(P_.a - U)) - (4 * P_.a) / (1 + std::exp(P_.a));
}

// ---------------------------------------------------------------------------
//   Update and spike handling functions
// ---------------------------------------------------------------------------


void gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::update(nest::Time const & origin,const long from, const long to)
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
  double U__tmp = S_.U * V_.__P__U__U;
  /* replace analytically solvable variables with precisely integrated values  */
  S_.U = U__tmp;
  S_.U += (P_.alpha_over_N / 1.0) * (0.001 * B_.spike_inputs_grid_sum_[INCOMING_SPIKES - MIN_SPIKE_RECEPTOR]) / (1 / 1000.0);
  if (((0) + (1) * nest::get_vp_specific_rng( get_thread() )->drand()) <= 0.001 * __resolution * phi(S_.U))
  {  
    set_spiketime(nest::Time::step(origin.get_steps()+lag+1));
    nest::SpikeEvent se;
    nest::kernel().event_delivery_manager.send(*this, se, lag);
    if (P_.reset_after_spike)
    {  
      S_.U = 0;
    }
  }
    // voltage logging
    B_.logger_.record_data(origin.get_steps() + lag);
  }
}

// Do not move this function as inline to h-file. It depends on
// universal_data_logger_impl.h being included here.
void gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::handle(nest::DataLoggingRequest& e)
{
  B_.logger_.handle(e);
}


void gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::handle(nest::SpikeEvent &e)
{
  assert(e.get_delay_steps() > 0);
  assert( e.get_rport() < B_.spike_inputs_.size() );

  double weight = e.get_weight();
  size_t nestml_buffer_idx = 0;
  B_.spike_inputs_[ nestml_buffer_idx - MIN_SPIKE_RECEPTOR ].add_value(
    e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin() ),
    weight * e.get_multiplicity() );
}

