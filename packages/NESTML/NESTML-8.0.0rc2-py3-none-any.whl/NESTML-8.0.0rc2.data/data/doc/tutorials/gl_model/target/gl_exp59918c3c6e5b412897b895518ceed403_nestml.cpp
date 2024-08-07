// #define DEBUG 1
/*
 *  gl_exp59918c3c6e5b412897b895518ceed403_nestml.cpp
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
 *  Generated from NESTML at time: 2024-02-26 09:58:49.387864
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

#include "gl_exp59918c3c6e5b412897b895518ceed403_nestml.h"

// ---------------------------------------------------------------------------
//   Recordables map
// ---------------------------------------------------------------------------
nest::RecordablesMap<gl_exp59918c3c6e5b412897b895518ceed403_nestml> gl_exp59918c3c6e5b412897b895518ceed403_nestml::recordablesMap_;
namespace nest
{

  // Override the create() method with one call to RecordablesMap::insert_()
  // for each quantity to be recorded.
template <> void RecordablesMap<gl_exp59918c3c6e5b412897b895518ceed403_nestml>::create()
  {
    // add state variables to recordables map
   insert_(gl_exp59918c3c6e5b412897b895518ceed403_nestml_names::_refr_spikes_buffer, &gl_exp59918c3c6e5b412897b895518ceed403_nestml::get_refr_spikes_buffer);
   insert_(gl_exp59918c3c6e5b412897b895518ceed403_nestml_names::_V_m, &gl_exp59918c3c6e5b412897b895518ceed403_nestml::get_V_m);

    // Add vector variables  
  }
}

// ---------------------------------------------------------------------------
//   Default constructors defining default parameters and state
//   Note: the implementation is empty. The initialization is of variables
//   is a part of gl_exp59918c3c6e5b412897b895518ceed403_nestml's constructor.
// ---------------------------------------------------------------------------

gl_exp59918c3c6e5b412897b895518ceed403_nestml::Parameters_::Parameters_()
{
}

gl_exp59918c3c6e5b412897b895518ceed403_nestml::State_::State_()
{
}

// ---------------------------------------------------------------------------
//   Parameter and state extractions and manipulation functions
// ---------------------------------------------------------------------------

gl_exp59918c3c6e5b412897b895518ceed403_nestml::Buffers_::Buffers_(gl_exp59918c3c6e5b412897b895518ceed403_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

gl_exp59918c3c6e5b412897b895518ceed403_nestml::Buffers_::Buffers_(const Buffers_ &, gl_exp59918c3c6e5b412897b895518ceed403_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

// ---------------------------------------------------------------------------
//   Default constructor for node
// ---------------------------------------------------------------------------

gl_exp59918c3c6e5b412897b895518ceed403_nestml::gl_exp59918c3c6e5b412897b895518ceed403_nestml():StructuralPlasticityNode(), P_(), S_(), B_(*this)
{
  init_state_internal_();
  recordablesMap_.create();
  pre_run_hook();
}

// ---------------------------------------------------------------------------
//   Copy constructor for node
// ---------------------------------------------------------------------------

gl_exp59918c3c6e5b412897b895518ceed403_nestml::gl_exp59918c3c6e5b412897b895518ceed403_nestml(const gl_exp59918c3c6e5b412897b895518ceed403_nestml& __n):
  StructuralPlasticityNode(), P_(__n.P_), S_(__n.S_), B_(__n.B_, *this) {

  // copy parameter struct P_
  P_.tau_m = __n.P_.tau_m;
  P_.C_m = __n.P_.C_m;
  P_.t_ref = __n.P_.t_ref;
  P_.tau_syn = __n.P_.tau_syn;
  P_.V_r = __n.P_.V_r;
  P_.V_reset = __n.P_.V_reset;
  P_.b = __n.P_.b;
  P_.a = __n.P_.a;
  P_.V_b = __n.P_.V_b;
  P_.with_refr_input = __n.P_.with_refr_input;
  P_.reset_after_spike = __n.P_.reset_after_spike;
  P_.I_e = __n.P_.I_e;

  // copy state struct S_
  S_.refr_spikes_buffer = __n.S_.refr_spikes_buffer;
  S_.refr_tick = __n.S_.refr_tick;
  S_.V_m = __n.S_.V_m;

  // copy internals V_
  V_.RefractoryCounts = __n.V_.RefractoryCounts;
  V_.__h = __n.V_.__h;
  V_.__P__V_m__V_m = __n.V_.__P__V_m__V_m;
}

// ---------------------------------------------------------------------------
//   Destructor for node
// ---------------------------------------------------------------------------

gl_exp59918c3c6e5b412897b895518ceed403_nestml::~gl_exp59918c3c6e5b412897b895518ceed403_nestml()
{
}

// ---------------------------------------------------------------------------
//   Node initialization functions
// ---------------------------------------------------------------------------
void gl_exp59918c3c6e5b412897b895518ceed403_nestml::calibrate_time( const nest::TimeConverter& tc )
{
  LOG( nest::M_WARNING,
    "gl_exp59918c3c6e5b412897b895518ceed403_nestml",
    "Simulation resolution has changed. Internal state and parameters of the model have been reset!" );

  init_state_internal_();
}
void gl_exp59918c3c6e5b412897b895518ceed403_nestml::init_state_internal_()
{
#ifdef DEBUG
  std::cout << "gl_exp59918c3c6e5b412897b895518ceed403_nestml::init_state_internal_()" << std::endl;
#endif

  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  // initial values for parameters
    

    P_.tau_m = 10; // as ms
    

    P_.C_m = 250; // as pF
    

    P_.t_ref = 2; // as ms
    

    P_.tau_syn = 0.5; // as ms
    

    P_.V_r = (-65); // as mV
    

    P_.V_reset = (-65); // as mV
    

    P_.b = 27; // as real
    

    P_.a = 5; // as mV
    

    P_.V_b = (-51.3); // as mV
    

    P_.with_refr_input = false; // as boolean
    

    P_.reset_after_spike = true; // as boolean
    

    P_.I_e = 0; // as pA

  recompute_internal_variables();
  // initial values for state variables
    

    S_.refr_spikes_buffer = 0; // as mV
    

    S_.refr_tick = 0; // as integer
    

    S_.V_m = P_.V_r; // as mV
}

void gl_exp59918c3c6e5b412897b895518ceed403_nestml::init_buffers_()
{
#ifdef DEBUG
  std::cout << "gl_exp59918c3c6e5b412897b895518ceed403_nestml::init_buffers_()" << std::endl;
#endif
  // spike input buffers
  get_spike_inputs_().clear();
  get_spike_inputs_grid_sum_().clear();

  // continuous time input buffers  

  get_I_stim().clear();
  B_.I_stim_grid_sum_ = 0;

  B_.logger_.reset();


}

void gl_exp59918c3c6e5b412897b895518ceed403_nestml::recompute_internal_variables(bool exclude_timestep) {
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  if (exclude_timestep) {    
      

      V_.RefractoryCounts = nest::Time(nest::Time::ms((double) (P_.t_ref))).get_steps(); // as integer
      

      V_.__P__V_m__V_m = std::exp((-V_.__h) / P_.tau_m); // as real
  }
  else {    
      

      V_.RefractoryCounts = nest::Time(nest::Time::ms((double) (P_.t_ref))).get_steps(); // as integer
      

      V_.__h = __resolution; // as ms
      

      V_.__P__V_m__V_m = std::exp((-V_.__h) / P_.tau_m); // as real
  }
}
void gl_exp59918c3c6e5b412897b895518ceed403_nestml::pre_run_hook() {
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
double gl_exp59918c3c6e5b412897b895518ceed403_nestml::phi ( double V_m) const
{  
  return ((1 / P_.b) * std::exp((V_m - P_.V_b) / P_.a));
}

// ---------------------------------------------------------------------------
//   Update and spike handling functions
// ---------------------------------------------------------------------------


void gl_exp59918c3c6e5b412897b895518ceed403_nestml::update(nest::Time const & origin,const long from, const long to)
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function



  for ( long lag = from ; lag < to ; ++lag )
  {
    auto get_t = [origin, lag](){ return nest::Time( nest::Time::step( origin.get_steps() + lag + 1) ).get_ms(); };

    for (long i = 0; i < NUM_SPIKE_RECEPTORS; ++i)
    {
        get_spike_inputs_grid_sum_()[i] = get_spike_inputs_()[i].get_value(lag);
    }
    B_.I_stim_grid_sum_ = get_I_stim().get_value(lag);

    // NESTML generated code for the update block
  if (S_.refr_tick == 0)
  {  
    double V_m__tmp = S_.V_m * V_.__P__V_m__V_m - P_.V_r * V_.__P__V_m__V_m + P_.V_r - P_.I_e * V_.__P__V_m__V_m * P_.tau_m / P_.C_m + P_.I_e * P_.tau_m / P_.C_m - B_.I_stim_grid_sum_ * V_.__P__V_m__V_m * P_.tau_m / P_.C_m + B_.I_stim_grid_sum_ * P_.tau_m / P_.C_m;
    /* replace analytically solvable variables with precisely integrated values  */
    S_.V_m = V_m__tmp;
    S_.V_m += (1.0 / 1.0) * (0.001 * B_.spike_inputs_grid_sum_[SPIKES - MIN_SPIKE_RECEPTOR]) / (1 / 1000.0);
    if (P_.with_refr_input && S_.refr_spikes_buffer != 0.0)
    {  
      S_.V_m += S_.refr_spikes_buffer;
      S_.refr_spikes_buffer = 0.0;
    }
  }
  else
  {  
    if (P_.with_refr_input)
    {  
      S_.refr_spikes_buffer += (0.001 * B_.spike_inputs_grid_sum_[SPIKES - MIN_SPIKE_RECEPTOR]) * std::exp((-S_.refr_tick) * 3600000.0 / P_.tau_m) * 1.0 * 1000.0;
    }
    S_.refr_tick -= 1;
  }
  if (((0) + (1) * nest::get_vp_specific_rng( get_thread() )->drand()) <= 0.001 * __resolution * phi(S_.V_m))
  {  
    S_.refr_tick = V_.RefractoryCounts;
    if (P_.reset_after_spike)
    {  
      S_.V_m = P_.V_reset;
    }
    set_spiketime(nest::Time::step(origin.get_steps()+lag+1));
    nest::SpikeEvent se;
    nest::kernel().event_delivery_manager.send(*this, se, lag);
  }
    // voltage logging
    B_.logger_.record_data(origin.get_steps() + lag);
  }
}

// Do not move this function as inline to h-file. It depends on
// universal_data_logger_impl.h being included here.
void gl_exp59918c3c6e5b412897b895518ceed403_nestml::handle(nest::DataLoggingRequest& e)
{
  B_.logger_.handle(e);
}


void gl_exp59918c3c6e5b412897b895518ceed403_nestml::handle(nest::SpikeEvent &e)
{
  assert(e.get_delay_steps() > 0);
  assert( e.get_rport() < B_.spike_inputs_.size() );

  double weight = e.get_weight();
  size_t nestml_buffer_idx = 0;
  B_.spike_inputs_[ nestml_buffer_idx - MIN_SPIKE_RECEPTOR ].add_value(
    e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin() ),
    weight * e.get_multiplicity() );
}

void gl_exp59918c3c6e5b412897b895518ceed403_nestml::handle(nest::CurrentEvent& e)
{
  assert(e.get_delay_steps() > 0);

  const double current = e.get_current();     // we assume that in NEST, this returns a current in pA
  const double weight = e.get_weight();
  get_I_stim().add_value(
               e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin()),
               weight * current );
}

